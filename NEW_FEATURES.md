# 🎉 New Features Added

## 1. Excel Export Feature 📊

Every meal logged is now automatically tracked and can be exported to Excel!

### What's Tracked:
- **Phone Number** - User identifier
- **Original Message** - Exact message sent by user
- **Timestamp** - When the meal was logged
- **Items Extracted** - Formatted list of foods (e.g., "2x roti, 1x dal")
- **Total Calories** - Calculated calories
- **Total Protein** - Calculated protein
- **Source** - Where it came from ("whatsapp" or "testing")

### How to Use:

**From WhatsApp:**
```
User: export
Bot: ✅ Exported 15 meals to meal_logs.xlsx
```

**From Code:**
```python
from database import MealDatabase

db = MealDatabase()
success, message = db.export_to_excel("my_meals.xlsx")
print(message)
```

### Excel File Features:
- ✅ Beautiful formatting with colored headers
- ✅ Auto-sized columns
- ✅ Clear data structure
- ✅ Ready for analysis in Excel/Google Sheets
- ✅ Can filter by user or export all

### Example Output:
| Phone Number | Original Message | Timestamp | Items Extracted | Total Calories | Total Protein | Source |
|--------------|------------------|-----------|-----------------|----------------|---------------|---------|
| whatsapp:+91... | I had 2 rotis and dal | 2026-01-12 10:30 | 2x roti, 1x dal | 246 kcal | 13.8g | whatsapp |

## 2. Better Error Messages ❌➡️✅

### Before:
```
Bot: I couldn't find any food items in your message.
```

### After:
```
Bot: ❌ Sorry, I couldn't find any food items from our database in your message.

📋 Common foods I can track:
roti, rice, dal, paneer, biryani, idli, dosa, samosa, curd, eggs, ...

💡 Try: '2 rotis and dal' or 'had chicken biryani'

Type 'list' to see all available foods.
```

### New Error Types:

#### 1. **No Food Found**
When the parser can't identify any foods at all:
```
User: I had xyz abc
Bot: ❌ Sorry, I couldn't find any food items...
     [Shows common foods and suggestions]
```

#### 2. **Not in Database**
When foods are identified but not in the database:
```
User: I had pizza and burger
Bot: ❌ These items are not in our database: pizza, burger

💡 Please try similar food items or add them to the database.

Type 'list' to see available foods.
```

#### 3. **Partial Match** (New!)
When some items match but others don't:
```
User: I had 2 rotis and pizza
Bot: ✅ Meal Logged Successfully!

• 2x Roti
  Calories: 142 kcal | Protein: 6.2g

📊 TOTAL:
🔥 Calories: 142 kcal
💪 Protein: 6.2g

⚠️ Note: These items were not found in database: pizza
```

## 3. Food List Feature 📋

Users can now see all available foods organized by category!

### How to Use:

**From WhatsApp:**
```
User: list
```
or
```
User: menu
```
or
```
User: foods
```

**Response:**
```
📋 *Available Foods:*

☕ Beverages
coffee, tea

🍞 Breads
dosa, idli, naan, paratha, puri, roti, uttapam

🍛 Curries
butter chicken, chicken curry, egg curry, palak paneer

🥛 Dairy
curd, lassi, milk, paneer, raita

🥚 Eggs
boiled egg, omelette

🍎 Fruits
apple, banana

🫘 Lentils & Beans
chana masala, dal, rajma, sambar

🍚 Rice & Grains
biryani, khichdi, poha, rice, upma

🍘 Snacks & Sweets
gulab jamun, jalebi, samosa, vada

💡 *Usage:* Send '2 rotis and dal' or 'had biryani'
```

## 4. Source Tracking 🔍

Every meal now tracks where it came from:

- **`whatsapp`** - Messages from WhatsApp users
- **`testing`** - From test scripts
- **`api`** - From direct API calls (if you add API endpoints)

### Why This Matters:
- Filter test data from real data
- Analyze usage patterns
- Debug issues
- Generate user reports

### In Database:
```sql
SELECT * FROM meals WHERE source = 'whatsapp';
```

### In Excel:
The "Source" column lets you filter in Excel/Google Sheets

## 5. Enhanced Database Schema 🗄️

### Updated Meals Table:
```sql
CREATE TABLE meals (
    id INTEGER PRIMARY KEY,
    phone_number TEXT,
    meal_description TEXT,          -- Original user message
    timestamp TIMESTAMP,
    total_calories REAL,
    total_protein REAL,
    parsed_items TEXT,              -- JSON of parsed items
    items_extracted TEXT,           -- Human-readable: "2x roti, 1x dal"
    source TEXT DEFAULT 'whatsapp'  -- NEW: whatsapp/testing/api
)
```

## Updated Commands

### Available Commands:

| Command | Description |
|---------|-------------|
| `help` | Show help message |
| `list`, `menu`, `foods` | Show all available foods |
| `summary`, `stats`, `today` | Show daily summary |
| `export`, `download`, `excel` | Download Excel file |
| Any meal description | Log a meal |

## Testing the New Features

### 1. Test Excel Export:
```bash
python3 test_excel_export.py
```

### 2. Test Error Messages:
```python
from food_parser import FoodParser

parser = FoodParser('data/indian_foods.json', use_llm=False)

# Test 1: No food found
result = parser.process_message("I had xyz abc")
print(result['message'])

# Test 2: Not in database
result = parser.process_message("I had pizza")
print(result['message'])

# Test 3: Partial match
result = parser.process_message("2 rotis and pizza")
print(result)
```

### 3. Test Food List:
```python
from food_parser import FoodParser

parser = FoodParser('data/indian_foods.json', use_llm=False)
food_list = parser.get_food_list()
print(food_list)
```

## Usage Examples

### Scenario 1: Normal Meal Logging
```
User: I had 2 rotis and dal
Bot: ✅ Meal Logged Successfully!
     • 2x Roti - 142 kcal, 6.2g protein
     • 1x Dal - 104 kcal, 7.6g protein
     📊 TOTAL: 246 kcal, 13.8g protein

[Saved to database with source='whatsapp']
```

### Scenario 2: Unknown Food
```
User: I had burger and fries  
Bot: ❌ These items are not in our database: burger, fries
     💡 Please try similar food items...
     Type 'list' to see available foods.

[NOT saved to database]
```

### Scenario 3: Partial Match
```
User: 2 rotis and pizza
Bot: ✅ Meal Logged Successfully!
     • 2x Roti - 142 kcal, 6.2g protein
     ⚠️ Note: These items were not found: pizza

[Saved with matched items + warning in items_extracted]
```

### Scenario 4: Export Data
```
User: export
Bot: ✅ Exported 25 meals to meal_logs.xlsx
     [File ready for download]

[Excel file created in data/exports/ folder]
```

### Scenario 5: Check Available Foods
```
User: list
Bot: 📋 *Available Foods:*
     [Shows all 35+ foods organized by category]
```

## API Changes

### Updated `log_meal()`:
```python
db.log_meal(
    phone_number="whatsapp:+1234567890",
    meal_description="2 rotis and dal",
    total_calories=246,
    total_protein=13.8,
    parsed_items='[{"food": "roti", "quantity": 2}]',
    items_extracted="2x roti, 1x dal",  # NEW
    source="whatsapp"                     # NEW
)
```

### New Methods:

```python
# Export to Excel
success, message = db.export_to_excel("meals.xlsx", phone_number=None)

# Get food list
food_list = food_parser.get_food_list(category="all")

# Process message (now returns more types)
result = food_parser.process_message("user message")
# result['type'] can be:
#   - 'meal_logged'
#   - 'partial_match' (NEW)
#   - 'no_food_found'
#   - 'not_in_database' (NEW)
#   - 'summary_request'
#   - 'export_request' (NEW)
```

## Benefits

### For Users:
✅ **Better feedback** when foods aren't found  
✅ **See available foods** easily  
✅ **Export data** for personal tracking  
✅ **Partial logging** - don't lose data if one food is unknown

### For Developers:
✅ **Track data source** (whatsapp/testing/api)  
✅ **Easy data analysis** with Excel export  
✅ **Better error handling** and user experience  
✅ **Cleaner database** with formatted items_extracted

### For Analysis:
✅ **Excel-ready data** for charts and graphs  
✅ **Filter by source** to separate test vs real data  
✅ **Human-readable items** in items_extracted column  
✅ **Complete audit trail** with timestamps and sources

## Backward Compatibility

✅ **Old database records** will work (source defaults to 'whatsapp')  
✅ **Existing code** continues to work  
✅ **Optional parameters** for new features  
✅ **Graceful degradation** if openpyxl not installed

## Next Steps

1. ✅ Save the updated files (database.py, food_parser.py, app.py)
2. ✅ Test with `python3 test_excel_export.py`
3. ✅ Deploy to your server
4. ✅ Try the new commands in WhatsApp!

---

**Questions or issues? Check the test files for examples!**
