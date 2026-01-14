# 🚀 Complete Setup Guide - WhatsApp Calorie Tracker

Get your WhatsApp Calorie Tracker running in **10-15 minutes**!

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Local Testing](#local-testing)
5. [Production Deployment](#production-deployment)
6. [UptimeRobot Setup](#uptimerobot-setup)
7. [WhatsApp Configuration](#whatsapp-configuration)
8. [Usage Examples](#usage-examples)
9. [Troubleshooting](#troubleshooting)
10. [Cost Breakdown](#cost-breakdown)

---

## Overview

### 🆓 GOOD NEWS: 100% FREE VERSION AVAILABLE!

You **don't need** OpenAI or Anthropic API keys! The app works perfectly with **FREE regex-based parsing**.

**Monthly Cost: ~$0.71-0.79** (only Twilio WhatsApp fees)

### ✨ What You Get

- ✅ **FREE Parser** - No API costs (90-95% accuracy)
- ✅ **Meal Tags** - Auto-categorize by time (breakfast, lunch, dinner)
- ✅ **Manual Entry** - Add exact calories & protein values
- ✅ **Total Command** - Quick daily summary
- ✅ **Excel Export** - Download your meal logs
- ✅ **Food List** - 35+ Indian foods included
- ✅ **24/7 Uptime** - Never sleeps with UptimeRobot
- ✅ **Better Errors** - Helpful feedback

---

## Prerequisites

### Required
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **WhatsApp account** - Any WhatsApp number
- **Twilio account** - Free tier works! ($15 free credit)

### Optional (Better Accuracy)
- **OpenAI API key** - For 95-99% accuracy (~$0.10/month)
- **Anthropic API key** - Alternative to OpenAI (~$0.10/month)

### Recommended
- **GitHub account** - For deployment
- **Render account** - Free hosting
- **UptimeRobot account** - Keep app awake 24/7

---

## Setup Steps

### Step 1: Get Twilio Account (5 minutes) ⚡ REQUIRED

**Why Twilio?** It provides WhatsApp integration for messaging.

1. **Sign up**
   - Visit: https://www.twilio.com/try-twilio
   - Sign up (free trial gives **$15 credit** ≈ 1,900 messages!)

2. **Get credentials**
   - Go to **Console Dashboard**
   - Note down:
     - `Account SID` (starts with AC...)
     - `Auth Token`

3. **Setup WhatsApp Sandbox**
   - Go to **Messaging → Try it out → Try WhatsApp**
   - Note down the **WhatsApp sandbox number**
   - Example: `whatsapp:+14155238886`

---

### Step 2: Setup Project (2 minutes)

```bash
# Navigate to project directory
cd whatsapp-calorie-tracker

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask twilio python-dotenv openai anthropic openpyxl...
```

---

### Step 3: Configure Environment (2 minutes)

**Create `.env` file** (copy from `env.example`):

```bash
cp env.example .env
nano .env  # Or use any text editor
```

**For FREE version** (Recommended - No API costs!):

```env
# Twilio Credentials (REQUIRED)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Database (REQUIRED)
DATABASE_PATH=../data/user_meals.db

# Flask Secret Key (REQUIRED)
FLASK_SECRET_KEY=your-random-secret-key-here

# That's it! FREE parser is default (no API keys needed)
```

**Optional: Enable LLM for better accuracy** (+$0.10/month):

```env
# Add these ONLY if you want 95-99% accuracy
USE_LLM=true
LLM_PROVIDER=anthropic  # or "openai"

# Choose ONE:
ANTHROPIC_API_KEY=sk-ant-api03-...  # For Claude
# OR
OPENAI_API_KEY=sk-...  # For ChatGPT
```

---

### Step 4: Test Locally (2 minutes)

```bash
# Test without running server
python test_local.py
```

**Expected output:**
```
🆓 Using FREE regex-based parsing (no API costs!)

Testing: "I had 2 rotis and dal"
✅ Result: 246 kcal, 13.8g protein

Testing: "Had chicken biryani"
✅ Result: 280 kcal, 12g protein

✅ All tests passed!
```

---

## Local Testing

### Option A: Run Flask Server Locally

```bash
cd src
python app.py
```

Server runs on: `http://localhost:5000`

**Test endpoints:**
- Home: http://localhost:5000
- Health: http://localhost:5000/health
- Ping: http://localhost:5000/ping

---

### Option B: Test with ngrok (Connect WhatsApp Locally)

**Why ngrok?** Allows Twilio to reach your local server.

1. **Install ngrok**
   - Download: https://ngrok.com/download
   - Extract and add to PATH

2. **Run ngrok**
   ```bash
   ngrok http 5000
   ```

3. **Copy HTTPS URL**
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:5000
   ```

4. **Configure Twilio webhook** (see [WhatsApp Configuration](#whatsapp-configuration))

5. **Join sandbox and test!**
   - Send join code to Twilio number
   - Send: "I had 2 rotis and dal"
   - Get instant response!

---

## Production Deployment

### Recommended: Render.com (Free Tier)

**Why Render?** Free hosting with automatic deployments from GitHub.

#### Step 1: Push to GitHub (if not done)

```bash
git init
git add .
git commit -m "Initial commit - WhatsApp Calorie Tracker"
git branch -M main
git remote add origin https://github.com/yourusername/whatsapp-calorie-tracker.git
git push -u origin main
```

#### Step 2: Create Render Account

1. Visit: https://render.com
2. Sign up with GitHub account
3. Authorize Render to access your repositories

#### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   ```
   Name: whatsapp-calorie-tracker
   Region: Oregon (US West) or closest
   Branch: main
   Root Directory: (leave empty)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: cd src && python app.py
   ```

#### Step 4: Add Environment Variables

Click **"Environment"** → **"Add Environment Variable"**

Add these (copy from your `.env` file):

```
TWILIO_ACCOUNT_SID = ACxxxxxxxxxxxx
TWILIO_AUTH_TOKEN = your_token
TWILIO_WHATSAPP_NUMBER = whatsapp:+14155238886
DATABASE_PATH = ../data/user_meals.db
FLASK_SECRET_KEY = your-secret-key
```

**Optional** (for LLM):
```
USE_LLM = true
LLM_PROVIDER = anthropic
ANTHROPIC_API_KEY = sk-ant-api03-...
```

#### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait 2-3 minutes for deployment
3. Note your app URL: `https://your-app.onrender.com`

#### Step 6: Verify Deployment

Visit: `https://your-app.onrender.com/health`

Should see:
```json
{
  "status": "healthy",
  "message": "WhatsApp Calorie Tracker is running",
  "timestamp": "2026-01-14T10:30:00",
  "database": "connected",
  "parser_mode": "FREE regex-based",
  "uptime": "ready"
}
```

---

## UptimeRobot Setup

**Problem:** Render free tier sleeps after 15 minutes of inactivity.
**Solution:** UptimeRobot pings your app every 5 minutes to keep it awake!

**Cost:** FREE forever (50 monitors included)

### Step 1: Register (1 minute)

1. Visit: https://uptimerobot.com
2. Click **"Register for FREE"**
3. Sign up with email or Google
4. Verify your email

### Step 2: Add Monitor (2 minutes)

1. Click **"+ Add New Monitor"**
2. Fill in:
   ```
   Monitor Type: HTTP(s)
   Friendly Name: WhatsApp Calorie Tracker
   URL: https://your-app.onrender.com/health
   Monitoring Interval: 5 minutes
   ```
3. Click **"Create Monitor"**

### Step 3: Done! ✅

Your app will now:
- 🔄 Be pinged every 5 minutes
- 🚀 Stay awake 24/7
- ⚡ Respond instantly (no cold starts)
- 📧 Alert you via email if down

**Test it:** Send a WhatsApp message - should respond in < 1 second!

---

## WhatsApp Configuration

### Step 1: Configure Twilio Webhook

1. Go to **Twilio Console** → **Messaging** → **Try it out** → **Try WhatsApp**
2. Click **"Sandbox Settings"**
3. Set **"WHEN A MESSAGE COMES IN"** to:
   ```
   Production: https://your-app.onrender.com/webhook
   Local: https://abc123.ngrok.io/webhook
   ```
4. Click **"Save"**

### Step 2: Join WhatsApp Sandbox

1. From Twilio Console, find your join code (e.g., "join happy-dog")
2. Send this message from your WhatsApp to the Twilio number:
   ```
   join happy-dog
   ```
3. You should receive a confirmation message

### Step 3: Test! 🎉

Send to Twilio WhatsApp number:
```
I had 2 rotis and dal
```

**Expected response:**
```
✅ Meal Logged Successfully!

• 2x Roti (1 medium (30g))
  Calories: 142 kcal | Protein: 6.2g
• 1x Dal (1 bowl (150g))
  Calories: 104 kcal | Protein: 7.6g

📊 TOTAL:
🔥 Calories: 246 kcal
💪 Protein: 13.8g
```

---

## Usage Examples

### Basic Meal Logging

```
You: I had 2 rotis and dal
Bot: ✅ Meal Logged! 246kcal, 13.8g protein

You: Ate chicken biryani
Bot: ✅ Meal Logged! 280kcal, 12g protein

You: 3 idlis with sambar
Bot: ✅ Meal Logged! 207kcal, 9.5g protein
```

### Manual Entry (Exact Values)

```
You: protein 30g and calories 200
Bot: ✅ Manual Entry Logged!
     🔥 Calories: 200 kcal
     💪 Protein: 30g

You: 150 calories and 10g protein
Bot: ✅ Manual Entry Logged!
```

### Quick Total Check

```
You: total
Bot: 📊 Today's Total

     🔥 Calories: 446 kcal
     💪 Protein: 43.8g
     🍽️ Meals: 2
```

### Detailed Summary

```
You: summary
Bot: 📅 Daily Summary - 2026-01-14

     🍽️ Meals logged: 3
     🔥 Total Calories: 850 kcal
     💪 Total Protein: 45.2g

     📝 Recent Meals:
     1. Evening snack: 2 samosas
        200 kcal | 5g protein
     2. Lunch: chicken curry and rice
        450 kcal | 20g protein
     ... (and more)
```

### See Available Foods

```
You: list
Bot: 📋 Available Foods:

     ☕ Beverages
     coffee, tea

     🍞 Breads
     dosa, idli, naan, paratha, puri, roti, uttapam

     🍛 Curries
     butter chicken, chicken curry, egg curry, palak paneer

     ... (35+ foods)
```

### Export to Excel

```
You: export
Bot: ✅ Exported 25 meals to meal_logs.xlsx
```

### Get Help

```
You: help
Bot: 👋 Welcome to Calorie Tracker!
     ... (shows all commands)
```

---

## Troubleshooting

### ❌ Tests Failing

**Issue:** `python test_local.py` shows errors

**Solutions:**
- Make sure you have Twilio credentials in `.env`
- Check Python version: `python --version` (must be 3.11+)
- Reinstall dependencies: `pip install -r requirements.txt`
- Run from project root directory

---

### ❌ "No food items found"

**Issue:** Bot says it can't find any food items

**Solutions:**
- Try simpler messages: "I had roti and dal"
- Check available foods: Send "list" command
- Use food names from the database
- Or use manual entry: "protein 20g and calories 300"

---

### ❌ No Response on WhatsApp

**Issue:** Bot doesn't respond to messages

**Solutions:**
1. **Check webhook URL**
   - Twilio Console → Messaging → WhatsApp → Sandbox Settings
   - Verify webhook is correct

2. **Check app is running**
   - Visit: `https://your-app.onrender.com/health`
   - Should show "healthy"

3. **Check Twilio logs**
   - Twilio Console → Monitor → Logs → Errors
   - Look for webhook errors

4. **Verify sandbox joined**
   - Send join code again: "join [your-code]"

5. **Check UptimeRobot**
   - Is app being pinged every 5 minutes?
   - Any downtime alerts?

---

### ❌ App Sleeping / Slow Responses

**Issue:** First message takes 5-10 seconds

**Solution:** Setup UptimeRobot (see [UptimeRobot Setup](#uptimerobot-setup))

---

### ❌ LLM Error (if using optional LLM)

**Issue:** "LLM error" or "API key invalid"

**Solutions:**
- Check your API key in `.env` file
- Verify you have API credits (check OpenAI/Anthropic dashboard)
- Make sure `USE_LLM=true` is set
- Try the FREE version instead (remove `USE_LLM` or set to `false`)

---

### ❌ Database Error

**Issue:** "Database error" or "Could not log meal"

**Solutions:**
- Check `DATABASE_PATH` in `.env` is correct
- Verify `data/` directory exists
- Check file permissions
- Delete and recreate database: `rm data/user_meals.db`

---

### ❌ Deployment Failed on Render

**Issue:** Build or deployment fails

**Solutions:**
1. **Check build logs** in Render dashboard
2. **Verify requirements.txt** includes all dependencies
3. **Check Start Command**: `cd src && python app.py`
4. **Verify Python version** matches (3.11+)
5. **Check environment variables** are set correctly

---

## Cost Breakdown

### FREE Version (Recommended) 🆓

**Personal Use (2-3 meals/day, ~90 messages/month):**

| Component | Cost |
|-----------|------|
| Parser | $0.00 (FREE!) |
| Database | $0.00 (SQLite) |
| Hosting | $0.00 (Render free tier) |
| Uptime Monitoring | $0.00 (UptimeRobot free) |
| WhatsApp (90 msgs) | $0.71 |
| **TOTAL** | **$0.71/month** |

**Heavy Use (5-6 meals/day, ~180 messages/month):**

| Component | Cost |
|-----------|------|
| WhatsApp (180 msgs) | $1.42 |
| Everything else | $0.00 |
| **TOTAL** | **$1.42/month** |

---

### With LLM (Optional - Better Accuracy)

**Personal Use:**

| Component | Cost |
|-----------|------|
| Parser (LLM) | $0.10 |
| Database | $0.00 |
| Hosting | $0.00 |
| Uptime | $0.00 |
| WhatsApp (90 msgs) | $0.71 |
| **TOTAL** | **$0.81/month** |

**Heavy Use:**

| Component | Cost |
|-----------|------|
| Parser (LLM) | $0.20 |
| WhatsApp (180 msgs) | $1.42 |
| **TOTAL** | **$1.62/month** |

---

### Comparison

| Use Case | FREE Version | LLM Version |
|----------|--------------|-------------|
| **Personal (90 msgs/month)** | $0.71 | $0.81 |
| **Heavy (180 msgs/month)** | $1.42 | $1.62 |
| **Accuracy** | 90-95% | 95-99% |
| **Setup** | Easiest | Requires API key |
| **Speed** | Instant | ~1 second |

**Recommendation:** Start with FREE version! It works great for 95% of use cases.

---

## What Foods Can I Track?

The app comes with **35+ Indian foods**:

### Breads & Grains
roti, naan, paratha, puri, dosa, idli, uttapam

### Rice Dishes
rice, biryani, khichdi, poha, upma

### Curries & Lentils
dal, rajma, chana masala, sambar, butter chicken, chicken curry, egg curry, palak paneer

### Snacks
samosa, vada, pakora

### Dairy
curd, paneer, milk, lassi, raita

### Eggs
boiled egg, omelette, egg curry

### Drinks
chai (tea), coffee, lassi

### Fruits
apple, banana

### Sweets
gulab jamun, jalebi

**Want more?** Edit `data/indian_foods.json` to add your own foods!

---

## Accuracy Comparison

### FREE Version (90-95% accuracy)

```
✅ "Had 2 rotis and dal" → 246 kcal, 13.8g protein
✅ "Ate butter chicken and 2 naans" → 759 kcal, 33.2g protein
✅ "3 idlis with sambar" → 207 kcal, 9.5g protein
✅ "4 boiled eggs" → 272 kcal, 22g protein
✅ "Lunch was 3 chapatis, rajma and curd" → 351 kcal, 26.3g protein
```

**Works great for:**
- Common meal descriptions
- Simple phrasings
- Standard food items
- Personal use

### LLM Version (95-99% accuracy)

```
✅ All above examples
✅ "Had a big plate of biryani with raita" → Accurate
✅ "Ate some rotis (maybe 3?) with dal and paneer" → Handles uncertainty
✅ "Breakfast: poha, banana, and coffee with milk" → Complex meals
```

**Better for:**
- Complex descriptions
- Unusual phrasings
- Mixed foods
- Maximum accuracy

---

## Next Steps

### 1. ✅ You're Set Up! Now What?

**Week 1: Get Comfortable**
- Track every meal for 7 days
- Use "total" command throughout the day
- Use "summary" command at night
- Get familiar with the 35+ foods

**Week 2: Optimize**
- Add more foods to `data/indian_foods.json`
- Use manual entry for packaged foods
- Export to Excel and analyze patterns
- Setup meal goals

**Week 3: Advanced**
- Analyze meal timing with tags
- Track protein goals
- Identify high-calorie meals
- Optimize your nutrition

---

### 2. 📚 Read More Documentation

- **ALL_NEW_FEATURES.md** - Complete feature guide (8 major features)
- **README.md** - Full project documentation
- **FREE_VERSION.md** - Detailed FREE version guide
- **SWITCH_TO_CLAUDE.md** - How to enable LLM (optional)
- **DEPLOYMENT_GUIDE.md** - Other deployment options

---

### 3. 🎯 Add More Foods

Edit `data/indian_foods.json`:

```json
{
  "name": "my_food",
  "serving_size": "1 serving (100g)",
  "calories": 200,
  "protein": 15.0,
  "category": "custom"
}
```

Restart app and start tracking!

---

### 4. 📊 Export and Analyze

```
You: export
```

Open Excel file and analyze:
- Total calories by day/week/month
- Protein intake trends
- Meal timing patterns (breakfast, lunch, dinner)
- High-calorie meals to optimize

---

## Quick Command Reference

| Command | Description |
|---------|-------------|
| `I had 2 rotis and dal` | Log a meal (auto-parsed) |
| `protein 30g calories 200` | Manual entry (exact values) |
| `total` | Quick daily summary |
| `summary` | Detailed summary with meals |
| `list` | Show all available foods |
| `export` | Download Excel file |
| `help` | Show help message |

---

## Summary

### ⏱️ Total Setup Time
- **Basic Setup**: 10 minutes
- **With UptimeRobot**: 15 minutes
- **With Testing**: 20 minutes

### 💰 Monthly Cost
- **FREE Version**: $0.71-0.79
- **With LLM**: $0.81-0.89
- **Less than a samosa!** 🥟

### ✨ What You Built
- 📱 WhatsApp-based calorie tracker
- 🆓 FREE regex parser (90-95% accuracy)
- 🏷️ Auto meal tags (breakfast, lunch, dinner)
- ✍️ Manual entry support
- 📊 Daily summaries
- 📈 Excel exports
- 🚀 24/7 uptime
- 🍛 35+ Indian foods

---

## Need Help?

- 📖 Read **ALL_NEW_FEATURES.md** for feature details
- 📘 Read **README.md** for complete docs
- 🐛 Check troubleshooting section above
- 💬 Open an issue on GitHub
- 📧 Check Twilio/Render/UptimeRobot docs

---

## Visual Setup Summary

```
┌─────────────────────────────────────────────────┐
│  Step 1: Get Twilio Account (5 min)             │
│  → Sign up, get SID, token, WhatsApp number     │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Step 2: Setup Project (2 min)                  │
│  → Install dependencies, create .env            │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Step 3: Test Locally (2 min)                   │
│  → Run tests, verify everything works           │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Step 4: Deploy to Render (5 min)               │
│  → Push to GitHub, deploy on Render             │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Step 5: Setup UptimeRobot (2 min)              │
│  → Keep app awake 24/7                          │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Step 6: Configure Twilio Webhook (1 min)       │
│  → Connect WhatsApp to your app                 │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  ✅ DONE! Start tracking meals! 🎉              │
└─────────────────────────────────────────────────┘
```

---

**🎉 Congratulations! Your WhatsApp Calorie Tracker is ready!**

**Start tracking:** Send "I had 2 rotis and dal" to your WhatsApp bot!

---

**Last Updated:** January 14, 2026
**Version:** 2.0 (All Features Integrated)
