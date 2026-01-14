# WhatsApp Calorie Tracker 🥗📱

## 🆓 100% FREE Version Available! No API Costs!

An intelligent calorie tracking agent that works through WhatsApp. Track your Indian meals and get instant nutrition information!

**NEW**: Now works completely FREE with advanced regex-based parsing! No OpenAI or Anthropic API keys needed!  
**Cost**: Only ~$0.71/month for Twilio WhatsApp (100 messages)

## Features

- 🆓 **100% FREE Parser**: Advanced regex + fuzzy matching (no API costs!)
- 🤖 **Optional LLM**: Add OpenAI/Anthropic for even better accuracy (optional)
- 🍛 **Indian Food Database**: Pre-loaded with 35+ common Indian foods and their nutritional values
- 📊 **Automatic Tracking**: Logs all meals with timestamps
- 📈 **Daily Summaries**: Get instant summaries of your daily calorie and protein intake
- 💬 **WhatsApp Integration**: Chat naturally via WhatsApp
- 💾 **Persistent Storage**: SQLite database tracks your meal history
- ⚡ **Fast & Offline**: Parsing works instantly without internet

## How It Works

Simply send a WhatsApp message like:
- "I had 2 rotis and dal"
- "Ate chicken biryani and raita"
- "Had 3 idlis and sambar"

The bot will:
1. Parse your message using LLM
2. Calculate calories and protein
3. Save to your personal history
4. Reply with detailed breakdown

## WhatsApp Integration Options

### Option 1: Twilio (Recommended for Getting Started) ⭐

**Pros:**
- Quick setup (~15 minutes)
- Great documentation and support
- Free sandbox for testing
- Reliable infrastructure
- Works globally

**Cons:**
- Costs money after free trial ($0.0079 per message)
- Sandbox has "Join" message requirement for testing
- Need Twilio-approved business account for production

**Cost:** ~$0.0079 per message sent/received

### Option 2: WhatsApp Business API (Direct)

**Pros:**
- Direct from Meta/WhatsApp
- No middleman fees after setup
- Official integration
- Better for large scale

**Cons:**
- Complex setup process
- Requires business verification
- Takes longer to get approved
- More technical requirements

**Cost:** Varies by region, conversation-based pricing

### Option 3: Other Providers (360Dialog, MessageBird, Vonage)

Similar to Twilio but with different pricing models. Shop around based on your usage.

## Recommendation

**For this project, I recommend Twilio because:**
1. Fastest to set up and test
2. Well-documented
3. Perfect for personal projects and MVPs
4. Can always migrate later if costs become an issue
5. Easy webhook integration with Flask

## Deployment Options

### Option 1: Render.com (Recommended) ⭐

**Pros:**
- Free tier available
- Easy deployment from Git
- Auto-deploys on push
- Good for small projects
- Built-in environment variables

**Steps:**
1. Push code to GitHub
2. Connect Render to your repo
3. Add environment variables
4. Deploy!

**Cost:** Free tier, then $7/month for hobby

### Option 2: Railway.app

**Pros:**
- Very developer-friendly
- Free $5 credit monthly
- Simple deployment
- Fast

**Cost:** Pay-as-you-go after $5 credit

### Option 3: Heroku

**Pros:**
- Classic choice
- Well-documented
- Lots of add-ons

**Cons:**
- No free tier anymore
- More expensive

**Cost:** $5-7/month minimum

### Option 4: DigitalOcean App Platform

**Pros:**
- Good performance
- Predictable pricing
- Full control

**Cost:** $5/month basic

### Option 5: Self-hosted (VPS)

**Pros:**
- Full control
- Cheaper at scale
- Can run multiple projects

**Cons:**
- Need to manage server
- More complex setup

**Providers:** DigitalOcean Droplet ($4/mo), Linode, AWS Lightsail

## Quick Start Guide

### 1. Clone and Setup

```bash
cd whatsapp-calorie-tracker
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file:

```bash
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# LLM API Key (choose one)
OPENAI_API_KEY=your_openai_api_key_here
# OR
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Flask Configuration
FLASK_SECRET_KEY=your_random_secret_key
FLASK_ENV=production

# Database
DATABASE_PATH=data/user_meals.db
```

### 3. Set Up Twilio

1. **Create Twilio Account**: https://www.twilio.com/try-twilio
2. **Get WhatsApp Sandbox**: Console → Messaging → Try it out → Try WhatsApp
3. **Join Sandbox**: Send the join code from your phone to the sandbox number
4. **Configure Webhook**: Set webhook URL to `https://your-domain.com/webhook`

### 4. Get LLM API Key (FREE Option Available! 🎉)

**Option A: Anthropic Claude (RECOMMENDED - $5 FREE Credits!)**
- Go to https://console.anthropic.com
- Sign up and get **$5 in free credits** (usually!)
- Create API key
- Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`
- Set `LLM_PROVIDER=anthropic`
- **Cost**: FREE for ~5000 meal logs!

**Option B: OpenAI GPT**
- Go to https://platform.openai.com
- Add payment method (required, no free tier)
- Create API key
- Add to `.env`: `OPENAI_API_KEY=sk-...`
- Set `LLM_PROVIDER=openai`
- **Cost**: ~$0.10 per 100 meals

📖 See **FREE_API_SETUP.md** for detailed instructions!

### 5. Run Locally (for testing)

```bash
cd src
python app.py
```

Use ngrok for local webhook testing:
```bash
ngrok http 5000
# Use the ngrok URL as your Twilio webhook
```

### 6. Deploy to Render (Recommended)

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Deploy on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Configure:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `cd src && gunicorn app:app --bind 0.0.0.0:$PORT`
   - Add environment variables from `.env`
   - Click "Create Web Service"

3. **Update Twilio Webhook**
   - Copy your Render URL (e.g., `https://your-app.onrender.com`)
   - Go to Twilio Console
   - Set webhook to: `https://your-app.onrender.com/webhook`

### 7. Test It!

Send a WhatsApp message to your Twilio number:
```
I had 2 rotis and dal
```

You should get a response with calories and protein!

## Usage Examples

**Log a meal:**
```
Had 2 rotis, dal, and paneer
```

**Get daily summary:**
```
summary
```
or
```
today's total
```

**Get help:**
```
help
```

## Customization

### Add More Foods

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

### Change LLM Provider

In `src/app.py`, change:
```python
food_parser = FoodParser(
    food_database_path="../data/indian_foods.json",
    llm_provider="anthropic"  # or "openai"
)
```

### Add More Features

Ideas for enhancement:
- Add macros (carbs, fats)
- Weekly/monthly reports
- Goal setting and tracking
- Export data as CSV
- Integration with fitness apps
- Photo recognition of meals
- Voice message support

## Cost Estimation

**Monthly costs for moderate use (100 messages/month):**

- **Twilio WhatsApp**: $0.79/month
- **Anthropic Claude** (with $5 free credits): $0 for first ~5000 logs, then ~$0.10/month
- **Hosting** (Render free tier): $0
- **Total**: ~$0.79/month (or FREE during trial!)

**For heavy use (1000 messages/month):**
- **Total**: ~$8-10/month

💡 **Tip**: Start with Anthropic's free credits, then switch to paid only if needed!

## Troubleshooting

### LLM not parsing correctly?
- Check API key is set correctly
- Verify you have credits in your OpenAI/Anthropic account
- Check logs for error messages

### WhatsApp not responding?
- Verify webhook URL is correct in Twilio
- Check your server is running and accessible
- Look at Twilio debugger logs

### Database errors?
- Ensure `data/` directory exists
- Check file permissions
- Delete and recreate database if corrupted

## Security Notes

- Never commit `.env` file
- Use strong secret keys
- Enable HTTPS in production
- Rotate API keys periodically
- Consider rate limiting for production

## License

MIT License - feel free to use and modify!

## Contributing

Have ideas for improvement? Feel free to:
1. Fork the repo
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions:
- Check Twilio documentation
- Review OpenAI/Anthropic API docs
- Open an issue on GitHub

---

**Built with ❤️ for healthy eating tracking!**

Start tracking your meals today! 🍛
