# Total Command Feature

## Overview

Added a new **"total"** command that provides a quick view of daily calories and protein totals.

## What's New

### Two Command Options

**1. `total` - Quick Format (NEW!)**
```
📊 *Today's Total*

🔥 Calories: 539.0 kcal
💪 Protein: 24.2g
🍽️ Meals: 3
```
- Fast, concise response
- Shows just the numbers
- Perfect for quick checks

**2. `summary` - Detailed Format**
```
📅 *Daily Summary - 2026-01-14*

🍽️ Meals logged: 3
🔥 Total Calories: 539.0 kcal
💪 Total Protein: 24.2g

📝 *Recent Meals:*
1. Had chicken biryani for dinner
   280.0 kcal | 12.0g protein
2. Ate 3 idlis for breakfast
   117.0 kcal | 6.0g protein
3. I had 2 rotis and dal for lunch
   142.0 kcal | 6.2g protein
```
- Detailed information
- Includes list of recent meals
- Shows timestamps and meal details

## Usage Examples

### Quick Total Check
```
You: total
Bot: 📊 *Today's Total*

🔥 Calories: 1250 kcal
💪 Protein: 45g
🍽️ Meals: 4
```

### Detailed Summary
```
You: summary
Bot: 📅 *Daily Summary - 2026-01-14*

🍽️ Meals logged: 4
🔥 Total Calories: 1250 kcal
💪 Total Protein: 45g

📝 *Recent Meals:*
1. Evening snack: 2 samosas
   200 kcal | 5g protein
2. Lunch: chicken curry and rice
   450 kcal | 20g protein
... (and more)
```

## Commands Comparison

| Command | Length | Shows | Best For |
|---------|--------|-------|----------|
| `total` | Short (~70 chars) | Calories, protein, meal count | Quick checks |
| `summary` | Long (~300+ chars) | Everything + recent meals | Detailed review |
| `stats` | Long | Same as summary | Alternative |
| `today` | Long | Same as summary | Alternative |

## Code Changes

### 1. Added `format_total()` function (app.py:90-97)
```python
def format_total(summary: dict) -> str:
    """Format a quick total summary (calories and protein only)"""
    return (
        f"📊 *Today's Total*\n\n"
        f"🔥 Calories: {summary['total_calories']} kcal\n"
        f"💪 Protein: {summary['total_protein']}g\n"
        f"🍽️ Meals: {summary['meal_count']}"
    )
```

### 2. Updated webhook handler (app.py:163-176)
- Separate handling for `total` (quick)
- Separate handling for `summary/stats/today` (detailed)

### 3. Updated help message (app.py:113)
- Added "total" command description
- Clarified difference between commands

## When to Use Each Command

### Use `total`:
- ✅ Quick check during the day
- ✅ Just want the numbers
- ✅ Making decisions about next meal
- ✅ Checking if you're on track

### Use `summary`:
- ✅ End of day review
- ✅ Want to see what you ate
- ✅ Detailed meal breakdown
- ✅ Planning tomorrow's meals

## Testing

Run the test suite:
```bash
python test_total_command.py
```

Expected output:
```
✅ Total command test completed successfully!
✅ All triggers mapped correctly!
🎉 All tests passed!
```

## Deployment

### Step 1: Commit Changes
```bash
git add src/app.py test_total_command.py
git commit -m "Add 'total' command for quick daily summary"
git push origin main
```

### Step 2: Wait for Render Deploy
Render will automatically detect and deploy (2-3 minutes).

### Step 3: Test on WhatsApp
```
You: total
Bot: 📊 *Today's Total* ...
```

## Examples in Action

### Scenario 1: Morning Check
```
You: total
Bot: 📊 *Today's Total*

🔥 Calories: 350 kcal
💪 Protein: 12g
🍽️ Meals: 1

You: I'll have a big lunch then!
```

### Scenario 2: End of Day
```
You: summary
Bot: 📅 *Daily Summary - 2026-01-14*

🍽️ Meals logged: 5
🔥 Total Calories: 1850 kcal
💪 Total Protein: 78g

📝 *Recent Meals:*
... (detailed list)

You: Great, on target!
```

### Scenario 3: Before Dinner
```
You: total
Bot: 📊 *Today's Total*

🔥 Calories: 1200 kcal
💪 Protein: 45g
🍽️ Meals: 3

You: I can have 600 more calories for dinner
```

## Benefits

1. **Faster Responses**
   - `total` returns ~70 characters vs ~300+ for `summary`
   - Less data to transfer over WhatsApp

2. **User Choice**
   - Quick check: `total`
   - Detailed review: `summary`

3. **Better UX**
   - Sometimes you just want the numbers
   - No need to scroll through meal list

4. **Backwards Compatible**
   - Old `summary` command still works
   - `stats` and `today` still work
   - No breaking changes

## Future Enhancements

Potential additions:
- Weekly totals: `week`
- Monthly averages: `month`
- Calorie goals: `goal`
- Meal breakdown by type: `meals breakfast`
- Nutrition comparison: `compare today yesterday`

## Troubleshooting

**Command not working?**
- Make sure you type just "total" (lowercase or uppercase is fine)
- Check you're connected to WhatsApp

**Getting old format?**
- Wait for Render to deploy the update
- Clear your WhatsApp chat and try again

**Still shows summary format?**
- You might be typing "total" with extra words
- Try just: `total` (nothing else)

## Summary

✅ Added quick `total` command
✅ Kept detailed `summary` command
✅ Updated help message
✅ All tests passing
✅ Ready to deploy

**Users can now choose:**
- Fast: `total`
- Detailed: `summary`

Perfect for quick calorie checks throughout the day! 🎯
