# WhatsApp Calorie Tracker

> Track your meals and nutrition effortlessly through WhatsApp. Simple, smart, and always with you.

## What is This?

An intelligent calorie tracking bot that works through WhatsApp. Send messages like "I had 2 rotis and dal" and get instant nutrition tracking with calorie and protein information. Built specifically for Indian foods with 35+ pre-loaded items.

## V2 Features

**Version 2.0** brings powerful new capabilities:

1. **Custom Food Addition** - Add any food to the database instantly
2. **Delete Last Meal** - Undo mistakes with one command
3. **Weekly Breakdown** - 7-day nutrition overview with daily stats
4. **Improved Help System** - User-friendly guidance and commands
5. **Quick Total Command** - Fast daily stats without detailed breakdown

## Core Features

- 🆓 **100% FREE Parser** - Advanced regex + fuzzy matching (no API costs!)
- 🍛 **Indian Food Database** - Pre-loaded with 35+ common Indian foods
- 📊 **Automatic Tracking** - Logs all meals with timestamps and meal tags
- 📈 **Daily & Weekly Summaries** - Instant summaries of your nutrition intake
- 💬 **Natural Language** - Chat naturally via WhatsApp
- 💾 **Persistent Storage** - SQLite database tracks your meal history
- 📥 **Excel Export** - Download your meal logs for analysis
- ⚡ **Fast & Offline** - Parsing works instantly without internet

## Quick Start

### 1. Installation

```bash
git clone <your-repo-url>
cd whatsapp-calorie-tracker
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create `.env` file:

```bash
# Required: Twilio WhatsApp
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Optional: LLM for better accuracy (defaults to FREE parser)
# ANTHROPIC_API_KEY=your_key  # Recommended: $5 free credits
# OPENAI_API_KEY=your_key

# Optional: Configuration
DATABASE_PATH=data/user_meals.db
USE_LLM=false  # Set to true to use LLM parser
```

### 3. Set Up Twilio

1. Create account at https://www.twilio.com/try-twilio
2. Get WhatsApp Sandbox: Console → Messaging → Try WhatsApp
3. Join sandbox by sending the join code from your phone
4. Configure webhook URL: `https://your-domain.com/webhook`

### 4. Run Locally (Testing)

```bash
cd src
python app.py
```

For local webhook testing, use ngrok:
```bash
ngrok http 5000
# Use ngrok URL as Twilio webhook
```

## Deployment (Render.com)

**Recommended hosting: Render.com free tier**

### Deploy Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Create Web Service on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd src && gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment Variables**: Add all variables from `.env`

4. **Update Twilio Webhook**
   - Copy your Render URL (e.g., `https://your-app.onrender.com`)
   - Update Twilio webhook to: `https://your-app.onrender.com/webhook`

5. **Test It!**
   - Send WhatsApp message: "I had 2 rotis and dal"
   - You should receive a response with nutrition info

## Usage Commands

### Track Meals
```
I had 2 rotis and dal
Ate chicken curry and rice
Had 3 idlis for breakfast
```

### View Stats
```
total              → Quick daily summary
total week         → 7-day breakdown
summary / stats    → Detailed daily stats with recent meals
```

### Manage Foods
```
add protein shake 120 30 1 scoop   → Add custom food
list / menu                         → Show all available foods
```

### Utilities
```
delete / undo      → Remove last meal entry
export             → Download Excel file
help / commands    → Show all commands
```

### Manual Entry
```
protein 20g and calories 300
150 calories and 10g protein
```

## Example Conversation

```
You: hi
Bot: 👋 Welcome to Calorie Tracker!
     Type help to see what I can do.

You: I had 2 rotis and dal
Bot: ✅ Meal Logged Successfully!
     • 2x Roti
     • 1x Dal
     Calories: 246 kcal | Protein: 13.8g

You: total
Bot: 📊 Today's Total
     🔥 Calories: 246 kcal
     💪 Protein: 13.8g
     🍽️ Meals: 1

You: total week
Bot: 📅 Weekly Breakdown - Last 7 Days
     [Shows 7-day overview with daily stats]
```

## Customization

### Add Foods to Database

Edit `data/indian_foods.json`:

```json
{
  "name": "food_name",
  "aliases": ["alternate names"],
  "calories": 150,
  "protein": 8.5,
  "serving_size": "1 serving (150g)"
}
```

Or use the `add` command via WhatsApp:
```
add protein shake 120 30 1 scoop
```

### Switch to LLM Parser

Set in `.env`:
```bash
USE_LLM=true
ANTHROPIC_API_KEY=your_key  # or OPENAI_API_KEY
```

LLM parser provides higher accuracy (95-99%) vs FREE parser (90-95%).

## Testing

Run comprehensive test suite:

```bash
# Test all V2 features (~3 seconds)
python test_v2_features.py

# Test all core features (~5-10 seconds)
python test_all.py

# Test everything (~7-13 seconds)
python test_v2_features.py && python test_all.py
```

All tests: **21 tests, ~98% coverage**

See **TESTING_GUIDE.md** for detailed testing documentation.

## Cost Estimation

**Monthly costs for moderate use (100 messages):**

- **Twilio WhatsApp**: $0.79/month
- **LLM Parser** (optional): $0 (FREE parser) or ~$0.10/month (Anthropic)
- **Hosting** (Render free tier): $0
- **Total**: ~$0.79/month or **$0** (using FREE parser + Render trial)

## Documentation

- **TESTING_GUIDE.md** - Comprehensive testing guide
- **V2_RELEASE.md** - Complete V2 feature documentation
- **SETUP_GUIDE.md** - Detailed setup instructions
- **ADD_FOOD_FEATURE.md** - Custom food addition guide
- **DELETE_MEAL_FEATURE.md** - Delete meal documentation
- **WEEKLY_BREAKDOWN_FEATURE.md** - Weekly breakdown guide
- **HELP_SYSTEM_UPDATE.md** - Help system documentation

## Troubleshooting

**WhatsApp not responding?**
- Verify webhook URL in Twilio console
- Check server is running and accessible
- Review Twilio debugger logs

**Parser not working correctly?**
- Check if food exists in database (`list` command)
- Try LLM parser for higher accuracy (set `USE_LLM=true`)
- Add custom food with `add` command

**Database errors?**
- Ensure `data/` directory exists
- Check file permissions
- Delete and recreate database if corrupted

## Project Structure

```
whatsapp-calorie-tracker/
├── src/
│   ├── app.py              # Flask webhook handler
│   ├── database.py         # SQLite database operations
│   └── food_parser.py      # Meal parsing (FREE/LLM)
├── data/
│   ├── indian_foods.json   # Food database
│   └── user_meals.db       # SQLite database
├── test_v2_features.py     # V2 feature tests
├── test_all.py             # Core feature tests
└── requirements.txt
```

## Security

- Never commit `.env` file (use `.gitignore`)
- Use strong secret keys in production
- Enable HTTPS for webhook URLs
- Rotate API keys periodically
- Consider rate limiting for production use

## Version History

- **V2.4** (Jan 2026) - Improved help system with separate greeting/commands
- **V2.3** (Jan 2026) - Weekly breakdown feature
- **V2.2** (Jan 2026) - Delete last meal feature
- **V2.1** (Jan 2026) - Custom food addition
- **V2.0** (Jan 2026) - Quick total command, data storage docs
- **V1.0** (2025) - Initial release with core tracking features

## License

**Note**: This project does not currently have a license file. All rights reserved by default. If you intend to allow use and modification, please add an appropriate LICENSE file (e.g., MIT License).

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Run tests (`python test_v2_features.py && python test_all.py`)
4. Submit a pull request

## Support

For issues or questions:
- Check **TESTING_GUIDE.md** and **V2_RELEASE.md**
- Review Twilio and API documentation
- Open an issue on GitHub

---

**Start tracking your meals today!** 🍛

Built with ❤️ for healthy eating habits.
