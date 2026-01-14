# Getting Free API Credits 💰

Good news! You can run this app **for free** (or very cheap) using Anthropic Claude!

## Quick Answer: Use Anthropic Claude! 🎉

**Anthropic often provides $5 in FREE credits** for new accounts, which is enough for:
- **~5,000 meal logs** 
- **Several months of personal use**
- **Testing and development**

## Setup Steps (5 minutes)

### 1. Create Anthropic Account

1. Go to https://console.anthropic.com/
2. Click "Sign Up"
3. Create account with email
4. Verify your email
5. **Check if you have $5 free credits** in the dashboard

### 2. Get API Key

1. Click "API Keys" in the left sidebar
2. Click "Create Key"
3. Give it a name (e.g., "calorie-tracker")
4. **Copy the key** (starts with `sk-ant-api03-...`)
5. Save it somewhere safe (you won't see it again!)

### 3. Update Your .env File

```bash
# Copy the template
cp env.template .env

# Edit .env and add your key
nano .env
```

Add this line:
```env
ANTHROPIC_API_KEY=sk-ant-api03-YOUR_ACTUAL_KEY_HERE
LLM_PROVIDER=anthropic
```

### 4. Test It!

```bash
python3 test_local.py
```

You should see:
```
Using LLM provider: anthropic
✅ All tests passed!
```

## Cost Comparison

| Provider | Free Credits | Cost per 100 meals | Cost per 1000 meals |
|----------|--------------|-------------------|---------------------|
| **Anthropic Claude** | ✅ $5 | ~$0.10 | ~$1.00 |
| **OpenAI GPT** | ❌ None | ~$0.10 | ~$1.00 |

## Why Claude is Great for This Project

✅ **$5 free credits** = months of personal use  
✅ **Better at understanding context** (great for food names)  
✅ **Excellent with Indian food names**  
✅ **Fast and reliable**  
✅ **No credit card required** for testing  

## What If I Run Out of Free Credits?

After $5 in free credits:

1. **Add payment method** - costs are very low (~$1/month for personal use)
2. **Set usage limits** - protect yourself from unexpected charges
3. **Switch to OpenAI** - similar pricing, different model
4. **Use fallback parser** - app works without LLM (less accurate but free!)

## Alternative: OpenAI (If you prefer)

If you prefer OpenAI or already have an account:

1. Go to https://platform.openai.com/
2. Add payment method (required, no free tier)
3. Create API key
4. Set in .env:
   ```env
   OPENAI_API_KEY=sk-YOUR_KEY_HERE
   LLM_PROVIDER=openai
   ```
5. Set spending limit: https://platform.openai.com/settings/organization/limits

## Cost for Personal Use

**Typical personal usage** (2-3 meals/day for 30 days):
- Total API calls: ~90 per month
- **Cost: $0.08 - 0.15 per month**
- Less than a cup of chai! ☕

## Already Have Both Keys?

The app will use whichever one is set in `LLM_PROVIDER`:

```env
# Use Claude (default)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Or use OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=sk-...
```

## Troubleshooting

**"You exceeded your quota"**
- Check your credits at console.anthropic.com or platform.openai.com
- Add payment method if free credits are exhausted

**"API key not found"**
- Make sure .env file exists and has the correct key
- Check for typos in the key
- Ensure no extra spaces around the key

**"Rate limit exceeded"**
- You're making too many requests too fast
- Wait a minute and try again
- This is rare for personal use

## Summary

🎯 **Recommended**: Use Anthropic Claude with $5 free credits  
💰 **Cost**: Free for testing, ~$0.10/month for personal use  
⏱️ **Setup time**: 5 minutes  
🚀 **You're ready to go!**

---

Questions? Check the main README.md or QUICKSTART.md
