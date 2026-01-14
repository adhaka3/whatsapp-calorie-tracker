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
# By default, uses FREE regex-based parsing (no API costs!)
# Set USE_LLM=true in .env to enable LLM parsing (requires API key)
use_llm = os.getenv("USE_LLM", "false").lower() == "true"
llm_provider = os.getenv("LLM_PROVIDER", "anthropic") if use_llm else None

food_parser = FoodParser(
    food_database_path="../data/indian_foods.json",
    llm_provider=llm_provider,
    use_llm=use_llm
)

if use_llm:
    print(f"🤖 Using LLM-powered parsing with {llm_provider}")
else:
    print("🆓 Using FREE regex-based parsing (no API costs!)")
db = MealDatabase(db_path=os.getenv('DATABASE_PATH', '../data/user_meals.db'))

# Twilio client (for sending messages)
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)


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


def get_help_message() -> str:
    """Return help message"""
    return """👋 *Welcome to Calorie Tracker!*

I help you track your Indian meals and nutrition.

*How to use:*
• Simply message me what you ate, e.g.:
  - "I had 2 rotis and dal"
  - "Ate chicken curry and rice"
  - "Had 3 idlis for breakfast"

*Commands:*
• "summary" or "stats" - See today's totals
• "list" or "menu" - See all available foods
• "export" - Download your meal log as Excel
• "help" - Show this message

*Available foods:*
35+ Indian foods including roti, rice, dal, paneer, chicken curry, biryani, idli, dosa, and many more!

*Example:*
"Had 2 rotis, dal, and paneer"

Type "list" to see all available foods! 🍛"""


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
        
        # Handle help/start commands
        if incoming_msg.lower() in ['hi', 'hello', 'help', 'start']:
            msg.body(get_help_message())
            return str(resp)
        
        # Check for food list request
        if incoming_msg.lower() in ['list', 'foods', 'menu', 'available']:
            food_list = food_parser.get_food_list()
            msg.body(food_list)
            return str(resp)
        
        # Check for export request
        if any(word in incoming_msg.lower() for word in ['export', 'download', 'excel']):
            success, message = db.export_to_excel(f"data/exports/meals_{sender.replace(':', '_')}.xlsx", sender)
            msg.body(message)
            return str(resp)
        
        # Check if it's a summary request
        if any(word in incoming_msg.lower() for word in ['summary', 'total', 'today', 'stats']):
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
