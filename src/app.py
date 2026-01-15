"""Main Flask application with Twilio WhatsApp integration"""
import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
from food_parser import FoodParser
from database import MealDatabase
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize components
# Initialize database first (needed for custom foods)
db = MealDatabase(db_path=os.getenv('DATABASE_PATH', '../data/user_meals.db'))

# By default, uses FREE regex-based parsing (no API costs!)
# Set USE_LLM=true in .env to enable LLM parsing (requires API key)
use_llm = os.getenv("USE_LLM", "false").lower() == "true"
llm_provider = os.getenv("LLM_PROVIDER", "anthropic") if use_llm else None

# Initialize food parser with database instance for custom foods
food_parser = FoodParser(
    food_database_path="../data/indian_foods.json",
    llm_provider=llm_provider,
    use_llm=use_llm,
    meal_db=db  # Pass database instance to load/save custom foods
)

if use_llm:
    print(f"🤖 Using LLM-powered parsing with {llm_provider}")
else:
    print("🆓 Using FREE regex-based parsing (no API costs!")

# Twilio client (for sending messages)
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)


def parse_manual_entry(message: str) -> dict:
    """Parse manual calorie and protein entry"""
    import re

    message_lower = message.lower()

    # Check if this is a manual entry (contains both "calorie" and "protein" keywords)
    if ('calorie' in message_lower or 'cal' in message_lower) and ('protein' in message_lower):
        # Extract calories
        cal_patterns = [
            r'(\d+\.?\d*)\s*(?:calories?|cals?|kcals?)',
            r'(?:calories?|cals?|kcals?)\s*[:\s]*(\d+\.?\d*)',
        ]
        calories = 0
        for pattern in cal_patterns:
            match = re.search(pattern, message_lower)
            if match:
                calories = float(match.group(1))
                break

        # Extract protein
        protein_patterns = [
            r'protein\s*[:\s]+(\d+\.?\d*)\s*g?',  # protein: 30g or protein 30g
            r'(\d+\.?\d*)\s*g?\s*protein',         # 30g protein or 30 protein
        ]
        protein = 0
        for pattern in protein_patterns:
            match = re.search(pattern, message_lower)
            if match:
                protein = float(match.group(1))
                break

        if calories > 0 or protein > 0:
            return {
                'type': 'manual_entry',
                'calories': calories,
                'protein': protein,
                'original_message': message
            }

    return {'type': 'not_manual_entry'}


def format_meal_response(result: dict) -> str:
    """Format the meal logging result as a WhatsApp message"""
    if result['type'] == 'meal_logged':
        response_lines = ["✅ *Meal Logged Successfully!*\n"]

        # List each item
        for item in result['items']:
            response_lines.append(
                f"• {item['quantity']}x {item['name'].title()} "
                f"({item['serving_size']})\n"
                f"  Calories: {item['calories']} kcal | Protein: {item['protein']}g"
            )

        response_lines.append(
            f"\n📊 *TOTAL:*\n"
            f"🔥 Calories: {result['total_calories']} kcal\n"
            f"💪 Protein: {result['total_protein']}g"
        )

        return "\n".join(response_lines)

    elif result['type'] == 'no_food_found':
        return result['message']

    return "I couldn't process your message. Please try again."


def format_manual_entry_response(calories: float, protein: float) -> str:
    """Format manual entry confirmation message"""
    return (
        f"✅ *Manual Entry Logged!*\n\n"
        f"🔥 Calories: {calories} kcal\n"
        f"💪 Protein: {protein}g\n\n"
        f"Added to today's total."
    )


def format_daily_summary(summary: dict, recent_meals: list) -> str:
    """Format the daily summary as a WhatsApp message"""
    response_lines = [
        f"📅 *Daily Summary - {summary['date']}*\n",
        f"🍽️ Meals logged: {summary['meal_count']}",
        f"🔥 Total Calories: {summary['total_calories']} kcal",
        f"💪 Total Protein: {summary['total_protein']}g"
    ]

    if recent_meals:
        response_lines.append("\n📝 *Recent Meals:*")
        for i, meal in enumerate(recent_meals[:3], 1):
            response_lines.append(
                f"{i}. {meal['description'][:50]}\n"
                f"   {meal['calories']} kcal | {meal['protein']}g protein"
            )

    return "\n".join(response_lines)


def format_total(summary: dict) -> str:
    """Format a quick total summary (calories and protein only)"""
    return (
        f"📊 *Today's Total*\n\n"
        f"🔥 Calories: {summary['total_calories']} kcal\n"
        f"💪 Protein: {summary['total_protein']}g\n"
        f"🍽️ Meals: {summary['meal_count']}"
    )


def format_weekly_breakdown(breakdown: dict) -> str:
    """Format the weekly breakdown as a WhatsApp message"""
    response_lines = [
        "📅 *Weekly Breakdown - Last 7 Days*\n"
    ]

    # Add daily breakdown
    for day in breakdown['daily_breakdown']:
        # Use emoji indicators for data presence
        if day['meal_count'] == 0:
            indicator = "⚪"
            cal_str = "-"
            pro_str = "-"
        else:
            indicator = "🟢"
            cal_str = f"{day['calories']} kcal"
            pro_str = f"{day['protein']}g"

        response_lines.append(
            f"{indicator} *{day['day_label']}* ({day['full_date']})\n"
            f"   🔥 {cal_str} | 💪 {pro_str} | 🍽️ {day['meal_count']} meals"
        )

    # Add summary
    response_lines.append(
        f"\n📊 *Week Summary:*\n"
        f"🔥 Total Calories: {breakdown['total_calories']} kcal\n"
        f"💪 Total Protein: {breakdown['total_protein']}g\n"
        f"🍽️ Total Meals: {breakdown['total_meals']}\n"
        f"📈 Daily Average: {breakdown['avg_daily_calories']} kcal | {breakdown['avg_daily_protein']}g\n"
        f"📆 Active Days: {breakdown['days_with_meals']}/7"
    )

    return "\n".join(response_lines)


def get_greeting_message() -> str:
    """Return greeting message for hi/hello"""
    return """👋 *Welcome to Calorie Tracker!*

I'm here to help you track your meals and nutrition effortlessly.

✨ *Quick Start:*
Just tell me what you ate, and I'll track it for you!

Example: "I had 2 rotis and dal"

💡 *Want to know more?*
Type *help* or *commands* to see everything I can do.

Let's get started! 🍛"""


def get_help_message() -> str:
    """Return comprehensive help/commands message"""
    return """📚 *Calorie Tracker - Commands Guide*

*🍽️ TRACK MEALS*
Just message what you ate naturally:
• "I had 2 rotis and dal"
• "Ate chicken curry and rice"

*📊 VIEW STATS*
• *total* - Today's calories & protein summary
• *total week* - 7-day breakdown with daily stats
• *summary* or *stats* - Detailed today's stats with recent meals

*➕ ADD CUSTOM FOOD*
• *add <name> <cal> <protein> <serving>*
  Example: "add protein shake 120 30 1 scoop"
• Food is immediately available for tracking!

*✏️ MANUAL ENTRY*
• Know exact values? Send:
  "protein 20g and calories 300"

*🗑️ DELETE LAST MEAL*
• *delete* or *undo* - Remove your last meal entry
• Made a mistake? Just undo it instantly!

*📋 FOOD DATABASE*
• *list* or *menu* - See all 35+ available foods
• Includes roti, rice, dal, paneer, chicken curry, biryani, and more!

*📥 EXPORT DATA*
• *export* - Download your meal log as Excel file
• Get all your data for detailed analysis

*❓ HELP*
• *help* or *commands* - Show this message

Need assistance? Just send a message and I'll guide you! 😊"""


@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Handle incoming WhatsApp messages"""
    try:
        # Get the message details
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        
        print(f"Received message from {sender}: {incoming_msg}")
        
        # Prepare response
        resp = MessagingResponse()
        msg = resp.message()
        
        # Handle empty messages
        if not incoming_msg:
            msg.body("Please send me a message about what you ate!")
            return str(resp)

        # Handle greeting messages (hi, hello, good morning, etc.)
        greeting_triggers = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'start']
        if incoming_msg.lower() in greeting_triggers or incoming_msg.lower().startswith(tuple(greeting_triggers)):
            msg.body(get_greeting_message())
            return str(resp)

        # Handle help/commands request
        if incoming_msg.lower() in ['help', 'commands', 'command', '?', 'info']:
            msg.body(get_help_message())
            return str(resp)
        
        # Check for food list request
        if incoming_msg.lower() in ['list', 'foods', 'menu', 'available']:
            food_list = food_parser.get_food_list()
            msg.body(food_list)
            return str(resp)

        # Check for add food command
        if incoming_msg.lower().startswith('add '):
            parse_result = food_parser.parse_add_food_command(incoming_msg)

            if parse_result['type'] == 'parse_error':
                msg.body(parse_result['message'])
                return str(resp)

            elif parse_result['type'] == 'add_food':
                # Add the food to database
                add_result = food_parser.add_custom_food(
                    name=parse_result['name'],
                    calories=parse_result['calories'],
                    protein=parse_result['protein'],
                    serving_size=parse_result['serving_size']
                )
                msg.body(add_result['message'])
                return str(resp)

        # Check for delete last meal request
        if any(phrase in incoming_msg.lower() for phrase in ['delete last', 'delete meal', 'undo', 'remove last', 'delete']):
            result = db.delete_last_meal(sender)
            msg.body(result['message'])
            return str(resp)

        # Check for export request
        if any(word in incoming_msg.lower() for word in ['export', 'download', 'excel']):
            success, message = db.export_to_excel(f"data/exports/meals_{sender.replace(':', '_')}.xlsx", sender)
            msg.body(message)
            return str(resp)
        
        # Check for manual entry (calories and protein)
        manual_entry = parse_manual_entry(incoming_msg)
        if manual_entry['type'] == 'manual_entry':
            # Log manual entry to database
            db.log_meal(
                phone_number=sender,
                meal_description=manual_entry['original_message'],
                total_calories=manual_entry['calories'],
                total_protein=manual_entry['protein'],
                parsed_items='[]',
                items_extracted='Manual entry',
                source="whatsapp"
            )
            response_text = format_manual_entry_response(
                manual_entry['calories'],
                manual_entry['protein']
            )
            msg.body(response_text)
            return str(resp)

        # Check if it's a total week request (weekly breakdown)
        if 'total week' in incoming_msg.lower() or 'week total' in incoming_msg.lower() or 'weekly' in incoming_msg.lower():
            weekly_breakdown = db.get_weekly_breakdown(sender)
            response_text = format_weekly_breakdown(weekly_breakdown)
            msg.body(response_text)
            return str(resp)

        # Check if it's a total request (quick format)
        if incoming_msg.lower().strip() == 'total':
            daily_summary = db.get_daily_summary(sender)
            response_text = format_total(daily_summary)
            msg.body(response_text)
            return str(resp)

        # Check if it's a summary request (detailed format)
        if any(word in incoming_msg.lower() for word in ['summary', 'today', 'stats']):
            daily_summary = db.get_daily_summary(sender)
            recent_meals = db.get_recent_meals(sender, limit=3)
            response_text = format_daily_summary(daily_summary, recent_meals)
            msg.body(response_text)
            return str(resp)

        # Process the meal
        result = food_parser.process_message(incoming_msg)
        
        if result['type'] == 'meal_logged':
            # Prepare items for storage
            items_extracted = ", ".join([f"{item['quantity']}x {item['name']}" for item in result['items']])
            
            # Log to database
            db.log_meal(
                phone_number=sender,
                meal_description=incoming_msg,
                total_calories=result['total_calories'],
                total_protein=result['total_protein'],
                parsed_items=json.dumps(result['parsed_items']),
                items_extracted=items_extracted,
                source="whatsapp"
            )
            
            # Format and send response
            response_text = format_meal_response(result)
            msg.body(response_text)
        
        elif result['type'] == 'partial_match':
            # Log the matched items
            items_extracted = ", ".join([f"{item['quantity']}x {item['name']}" for item in result['items']])
            items_extracted += f" (unmatched: {', '.join(result['unmatched_items'])})"
            
            db.log_meal(
                phone_number=sender,
                meal_description=incoming_msg,
                total_calories=result['total_calories'],
                total_protein=result['total_protein'],
                parsed_items=json.dumps(result['parsed_items']),
                items_extracted=items_extracted,
                source="whatsapp"
            )
            
            # Format response with warning
            response_text = format_meal_response(result) + "\n\n" + result['warning']
            msg.body(response_text)
        
        elif result['type'] == 'no_food_found':
            msg.body(result['message'])
        
        elif result['type'] == 'not_in_database':
            msg.body(result['message'])
        
        elif result['type'] == 'export_request':
            success, message = db.export_to_excel(f"data/exports/meals_{sender.replace(':', '_')}.xlsx", sender)
            msg.body(message)
        
        elif result['type'] == 'summary_request':
            daily_summary = db.get_daily_summary(sender)
            recent_meals = db.get_recent_meals(sender, limit=3)
            response_text = format_daily_summary(daily_summary, recent_meals)
            msg.body(response_text)
        
        else:
            msg.body("I couldn't process your message. Please try again or type 'list' to see available foods.")
        
        return str(resp)
    
    except Exception as e:
        print(f"Error processing message: {e}")
        resp = MessagingResponse()
        msg = resp.message()
        msg.body("Sorry, I encountered an error. Please try again later.")
        return str(resp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for UptimeRobot monitoring"""
    import datetime

    # Check database connectivity
    try:
        db.get_daily_summary("health_check", datetime.datetime.now())
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "message": "WhatsApp Calorie Tracker is running",
        "timestamp": datetime.datetime.now().isoformat(),
        "database": db_status,
        "parser_mode": "LLM-powered" if use_llm else "FREE regex-based",
        "uptime": "ready"
    }, 200


@app.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint for keep-alive services"""
    return "pong", 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    parser_mode = "🤖 LLM-powered" if use_llm else "🆓 FREE regex-based"
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WhatsApp Calorie Tracker</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            .container {{
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }}
            h1 {{ margin-top: 0; font-size: 2em; }}
            .status {{
                background: rgba(76, 175, 80, 0.3);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 4px solid #4CAF50;
            }}
            .endpoint {{
                background: rgba(0, 0, 0, 0.2);
                padding: 10px;
                border-radius: 8px;
                margin: 10px 0;
                font-family: monospace;
            }}
            .badge {{
                display: inline-block;
                background: rgba(255, 255, 255, 0.2);
                padding: 5px 12px;
                border-radius: 15px;
                font-size: 0.9em;
                margin: 5px 5px 5px 0;
            }}
            a {{
                color: #fff;
                text-decoration: none;
                border-bottom: 2px solid rgba(255, 255, 255, 0.5);
            }}
            a:hover {{ border-bottom-color: #fff; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🥗 WhatsApp Calorie Tracker</h1>

            <div class="status">
                <strong>✅ Status: Running</strong><br>
                <small>Last checked: Just now</small>
            </div>

            <p><strong>📊 Configuration:</strong></p>
            <div class="badge">{parser_mode}</div>
            <div class="badge">💾 SQLite Database</div>
            <div class="badge">📱 WhatsApp Ready</div>

            <p><strong>🔗 Monitoring Endpoints:</strong></p>
            <div class="endpoint">
                <strong>Health:</strong> <a href="/health">/health</a><br>
                <small>Use this URL for UptimeRobot monitoring</small>
            </div>
            <div class="endpoint">
                <strong>Ping:</strong> <a href="/ping">/ping</a><br>
                <small>Lightweight keep-alive endpoint</small>
            </div>

            <p><strong>📱 How to Use:</strong></p>
            <ol>
                <li>Connect your WhatsApp to Twilio sandbox</li>
                <li>Send: "I had 2 rotis and dal"</li>
                <li>Get instant nutrition info!</li>
            </ol>

            <p><strong>🔔 Setup Monitoring:</strong></p>
            <ol>
                <li>Go to <a href="https://uptimerobot.com" target="_blank">UptimeRobot.com</a></li>
                <li>Add monitor with URL: <code style="background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px;">/health</code></li>
                <li>Set interval to 5 minutes</li>
                <li>Keep app awake 24/7!</li>
            </ol>
        </div>
    </body>
    </html>
    """


if __name__ == '__main__':
    # For development
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
