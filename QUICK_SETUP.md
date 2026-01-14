# 🚀 Quick Setup - UptimeRobot (5 Minutes)

## ✅ What Was Changed

Your app now has **2 monitoring endpoints**:

1. **`/health`** - Detailed health check (for UptimeRobot)
2. **`/ping`** - Simple keep-alive (returns "pong")

## 📝 Step-by-Step Setup

### 1️⃣ Deploy Updated Code (2 minutes)

```bash
cd /Users/adhaka/Desktop/ayush_personal/llm_agents/whatsapp-calorie-tracker

git add .
git commit -m "Add monitoring endpoints for UptimeRobot"
git push origin main
```

Wait for Render to redeploy (automatic).

### 2️⃣ Test Endpoints (1 minute)

Visit in browser:
```
https://whatsapp-calorie-tracker-1.onrender.com/health
```

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

### 3️⃣ Setup UptimeRobot (2 minutes)

**A. Register**
- Go to: https://uptimerobot.com
- Click: "Register for FREE"
- Sign up with email or Google

**B. Add Monitor**
- Click: "+ Add New Monitor"
- Fill in:
  ```
  Monitor Type: HTTP(s)
  Friendly Name: WhatsApp Calorie Tracker
  URL: https://whatsapp-calorie-tracker-1.onrender.com/health
  Interval: 5 minutes
  ```
- Click: "Create Monitor"

### 4️⃣ Done! ✅

Your app will now:
- 🔄 Be pinged every 5 minutes
- 🚀 Stay awake 24/7
- ⚡ Respond instantly (no cold starts)
- 📧 Alert you if down

## 📊 Visual Setup Guide

```
Step 1: Deploy
┌─────────────────────────────────┐
│ $ git add .                     │
│ $ git commit -m "Add monitoring"│
│ $ git push origin main          │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│  Render auto-deploys (2-3 min)  │
└─────────────────────────────────┘

Step 2: Verify
┌─────────────────────────────────┐
│ Visit: /health endpoint         │
│ See: JSON status response       │
└─────────────────────────────────┘

Step 3: UptimeRobot
┌─────────────────────────────────┐
│ 1. Register at uptimerobot.com  │
│ 2. Add New Monitor              │
│ 3. Enter your /health URL       │
│ 4. Set interval to 5 minutes    │
│ 5. Create Monitor               │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│    ✅ App stays awake 24/7!     │
└─────────────────────────────────┘
```

## 🎯 Quick Links

- **Your App:** https://whatsapp-calorie-tracker-1.onrender.com
- **Health Check:** https://whatsapp-calorie-tracker-1.onrender.com/health
- **UptimeRobot:** https://uptimerobot.com
- **Full Guide:** See UPTIMEROBOT_SETUP.md

## ⚡ Test It Now

Send WhatsApp message:
```
I had 2 rotis and dal
```

Should respond **instantly** (no delay)!

---

**Need detailed instructions?** → Read **UPTIMEROBOT_SETUP.md**
