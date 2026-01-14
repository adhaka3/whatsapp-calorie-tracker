# How to Switch to Anthropic Claude (Free Credits Available!)

Anthropic Claude often provides **$5 in free credits** for new accounts, which is enough for thousands of meal logs!

## Step 1: Get Anthropic API Key

1. Go to https://console.anthropic.com/
2. Sign up for a free account
3. Check if you have free credits (usually $5)
4. Go to "API Keys" section
5. Create a new API key
6. Copy the key (starts with `sk-ant-...`)

## Step 2: Update Your .env File

Replace or add this line in your `.env` file:

```env
# Comment out or remove OpenAI key
# OPENAI_API_KEY=sk-...

# Add Anthropic key
ANTHROPIC_API_KEY=sk-ant-api03-...
```

## Step 3: Update app.py to Use Claude

Edit `src/app.py`, find this line:

```python
food_parser = FoodParser(
    food_database_path="../data/indian_foods.json",
    llm_provider="openai"  # Change this
)
```

Change it to:

```python
food_parser = FoodParser(
    food_database_path="../data/indian_foods.json",
    llm_provider="anthropic"  # Use Claude!
)
```

## Step 4: Test It

```bash
cd whatsapp-calorie-tracker
python3 test_local.py
```

## Claude vs GPT Comparison

| Feature | Claude 3.5 Sonnet | GPT-4o-mini |
|---------|-------------------|-------------|
| **Free Credits** | ✅ $5 for new accounts | ❌ None |
| **Quality** | Excellent | Excellent |
| **Cost per 1M tokens** | $3 input / $15 output | $0.15 input / $0.60 output |
| **Speed** | Very fast | Very fast |
| **Context** | 200K tokens | 128K tokens |

For your use case (short meal descriptions), both work great!

## Benefits of Claude

- ✅ $5 free credits = ~5000 meal logs
- ✅ Better at understanding context
- ✅ More accurate parsing in my experience
- ✅ Great for Indian food names

That's it! Your app will now use Claude instead of GPT.
