# UptimeRobot Setup Guide

## 🎯 What This Does

UptimeRobot will ping your app every 5 minutes to:
- ✅ Keep your Render app awake 24/7 (no more cold starts!)
- 📧 Alert you if your app goes down
- 📊 Track uptime statistics
- ⚡ Ensure instant WhatsApp responses

## Code Changes Made

### 1. Enhanced Health Endpoint (`/health`)
Now returns detailed status information:
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

### 2. Added Ping Endpoint (`/ping`)
Simple lightweight endpoint for keep-alive:
- URL: `/ping`
- Response: `pong`
- Use this if you want faster responses

### 3. Improved Home Page
Visit your Render URL to see:
- Current status
- Monitoring endpoints
- Setup instructions
- Configuration details

## 📋 Complete Setup Steps

### Step 1: Deploy Updated Code to Render (5 minutes)

```bash
# Navigate to your project
cd /Users/adhaka/Desktop/ayush_personal/llm_agents/whatsapp-calorie-tracker

# Stage changes
git add src/app.py

# Commit
git commit -m "Add enhanced health monitoring endpoints"

# Push to GitHub
git push origin main
```

Render will automatically detect the push and redeploy (takes 2-3 minutes).

### Step 2: Verify Endpoints are Working (1 minute)

Once Render finishes deploying, test the endpoints:

**Method A: Browser**
1. Visit: `https://whatsapp-calorie-tracker-1.onrender.com/health`
2. You should see JSON response with status info
3. Visit: `https://whatsapp-calorie-tracker-1.onrender.com/ping`
4. You should see: `pong`

**Method B: Terminal**
```bash
curl https://whatsapp-calorie-tracker-1.onrender.com/health
curl https://whatsapp-calorie-tracker-1.onrender.com/ping
```

### Step 3: Register on UptimeRobot (2 minutes)

1. **Go to:** https://uptimerobot.com

2. **Click:** "Register for FREE" (top right corner)

3. **Sign up with:**
   - Email address and password
   - OR use Google/GitHub login

4. **Verify email** (check your inbox)

5. **Login** to your dashboard

### Step 4: Create Monitor (2 minutes)

1. **Click:** Big green button **"+ Add New Monitor"**

2. **Fill in the form:**

   ```
   Monitor Type: HTTP(s)
   ↓ Select from dropdown

   Friendly Name: WhatsApp Calorie Tracker
   ↓ Just a label for you

   URL (or IP): https://whatsapp-calorie-tracker-1.onrender.com/health
   ↓ Your Render URL + /health

   Monitoring Interval: 5 minutes
   ↓ Free tier minimum
   ```

3. **Leave defaults for:**
   - Monitor Timeout: 30 seconds ✅
   - HTTP Method: GET (HEAD) ✅
   - Post Value: (empty) ✅

4. **Click:** Green **"Create Monitor"** button at bottom

### Step 5: Verify It's Working (2 minutes)

Within 5 minutes you should see:

```
Monitor Dashboard:
├── Name: WhatsApp Calorie Tracker
├── Status: ✓ Up (green)
├── Response Time: ~200-500ms
└── Uptime: 100%
```

**Click on your monitor** to see:
- 📈 Response time graph
- ⏰ Last 24 hours uptime
- 📊 Detailed logs

### Step 6: Test Your WhatsApp Bot

Send a message to verify everything works:
```
You: I had 2 rotis and dal
Bot: ✅ Meal Logged Successfully! ...
```

Should respond **instantly** (no 5-10 second delay!)

## 🎉 You're Done!

Your app is now:
- ✅ Running 24/7 on Render
- ✅ Monitored by UptimeRobot
- ✅ Never sleeps (no cold starts)
- ✅ Alerts you if it goes down
- ✅ Responds instantly to WhatsApp messages

## 📊 What to Expect

### UptimeRobot Dashboard
- **Status:** Always "Up" with green checkmark
- **Response Time:** ~200-500ms (normal)
- **Uptime:** Should be 99.9%+
- **Checks:** Every 5 minutes (288 times/day)

### Email Alerts
You'll receive emails when:
- 🔴 App goes down (Render issue, deployment problem)
- 🟢 App comes back up

## 🔧 Advanced Configuration (Optional)

### Add Status Page
Share your uptime publicly:

1. Go to **"Status Pages"** tab in UptimeRobot
2. Click **"Add Status Page"**
3. Select "WhatsApp Calorie Tracker" monitor
4. Click **"Create Status Page"**
5. Get public URL: `https://stats.uptimerobot.com/xyz123`

Share this URL to show your app's uptime!

### Add More Alert Channels

1. Go to **"My Settings"** → **"Alert Contacts"**
2. Click **"Add Alert Contact"**
3. Choose from:
   - 📧 Email (already added)
   - 💬 Slack
   - 🎮 Discord
   - 📱 Telegram
   - 🪝 Webhook
   - 📞 SMS (paid)
   - ☎️ Voice Call (paid)

### Install Mobile App

Download UptimeRobot mobile app:
- **iOS:** https://apps.apple.com/app/uptimerobot/id1105342076
- **Android:** https://play.google.com/store/apps/details?id=com.uptimerobot

Get push notifications on your phone!

### Customize Monitoring Interval

Free tier options:
- 5 minutes (recommended) ✅
- 10 minutes
- 15 minutes
- 30 minutes

Paid plans ($7/month) offer:
- 1 minute
- 2 minutes
- 3 minutes

## 🔍 Monitoring Endpoints Comparison

| Endpoint | Use Case | Response Size | Speed |
|----------|----------|---------------|-------|
| `/health` | **UptimeRobot (Recommended)** | ~150 bytes | Normal |
| `/ping` | Lightweight monitoring | 4 bytes | Fastest |
| `/` | Human-friendly status | ~3KB | Normal |

**Recommendation:** Use `/health` for UptimeRobot

## ❓ Troubleshooting

### Monitor shows "Down"

**Check these:**
1. Is Render app deployed successfully?
   - Go to Render dashboard
   - Check deployment logs
2. Are the endpoints accessible?
   - Visit `/health` in browser
   - Should see JSON response
3. Is the URL correct in UptimeRobot?
   - Must be: `https://your-app.onrender.com/health`
   - NOT: `http://` or missing `/health`

### High Response Time (>2 seconds)

**Possible causes:**
1. First request after sleep (cold start)
   - Normal for first ping if app was sleeping
   - After 5 minutes of monitoring, should stabilize
2. Render free tier spinning up
   - Happens less often with UptimeRobot
   - Upgrade to Starter ($7/mo) for instant responses
3. Database slow
   - Check Render logs
   - May need to optimize queries

### Not Receiving Email Alerts

**Fix:**
1. Check spam/junk folder
2. Verify email in UptimeRobot settings:
   - My Settings → Alert Contacts
   - Make sure email is verified (green checkmark)
3. Check alert settings on monitor:
   - Edit monitor → Alert Contacts
   - Make sure your email is selected

### Monitor Pauses Automatically

**Reason:** UptimeRobot pauses monitors if they're down for too long (50+ checks)

**Fix:**
1. Go to monitor settings
2. Click **"Resume Monitoring"**
3. Fix the underlying issue (check Render deployment)

## 💰 Cost Breakdown

| Service | Cost | What You Get |
|---------|------|--------------|
| **UptimeRobot** | FREE | 50 monitors, 5-min intervals, email alerts |
| **Render** | FREE | 750 hrs/month (stays awake with UptimeRobot) |
| **Twilio** | ~$0.79/100 msgs | WhatsApp messaging |
| **Parser** | FREE | Regex-based parsing (no API costs) |
| **TOTAL** | **~$0.79/month** | Full working app! |

## 🎯 Next Steps

Now that your app is always awake:

1. ✅ Test WhatsApp bot (should respond instantly)
2. 📊 Check UptimeRobot dashboard daily
3. 📧 Make sure you receive email alerts
4. 🚀 Start tracking your meals!
5. 📱 Optional: Install UptimeRobot mobile app

## 📚 Additional Resources

- **UptimeRobot Docs:** https://uptimerobot.com/help
- **Render Docs:** https://render.com/docs
- **This Project:** See README.md for full documentation

---

**Questions?** Open an issue on GitHub or check the troubleshooting section above!

**Happy tracking! 🥗💪**
