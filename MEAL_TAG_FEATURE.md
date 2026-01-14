# Meal Tag Feature

## Overview

The meal tag feature automatically categorizes meals based on their timestamp. This helps users track and analyze their eating patterns throughout the day.

## Meal Tag Categories

Meals are automatically tagged based on the following time ranges:

| Meal Tag | Time Range | Description |
|----------|------------|-------------|
| **Breakfast** | 5:00 AM - 10:59 AM | Morning meal |
| **Brunch** | 11:00 AM - 11:59 AM | Late morning meal |
| **Lunch** | 12:00 PM - 2:59 PM | Midday meal |
| **Evening Snack** | 3:00 PM - 5:59 PM | Afternoon snack |
| **Dinner** | 6:00 PM - 9:59 PM | Evening meal |
| **Midnight Snack** | 10:00 PM - 4:59 AM | Late night meal |

## How It Works

### 1. Automatic Tagging

When a meal is logged, the system automatically:
- Captures the current timestamp
- Determines the appropriate meal tag based on the hour
- Saves the tag along with the meal data

### 2. Database Storage

The meal tag is stored in the `meals` table in the `meal_tag` column:

```sql
CREATE TABLE meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone_number TEXT,
    meal_description TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_calories REAL,
    total_protein REAL,
    parsed_items TEXT,
    items_extracted TEXT,
    source TEXT DEFAULT 'whatsapp',
    meal_tag TEXT,  -- New column for meal tag
    FOREIGN KEY (phone_number) REFERENCES users(phone_number)
);
```

### 3. Excel Export

When exporting meals to Excel, the meal tag is included as a separate column:

- **Column Name**: "Meal Tag"
- **Format**: Display-friendly format (e.g., "Evening Snack" instead of "evening_snack")
- **Position**: Column D (after Timestamp, before Items Extracted)

## Usage Examples

### Python Code

```python
from database import MealDatabase, get_meal_tag
from datetime import datetime

# Initialize database
db = MealDatabase()

# Log a meal (timestamp defaults to now)
db.log_meal(
    phone_number="whatsapp:+1234567890",
    meal_description="Had 2 rotis and dal",
    total_calories=450,
    total_protein=15,
    parsed_items='[{"name": "roti", "quantity": 2}]',
    items_extracted="2x roti, 1x dal"
)

# Log a meal with specific timestamp
breakfast_time = datetime.now().replace(hour=8, minute=0)
db.log_meal(
    phone_number="whatsapp:+1234567890",
    meal_description="Had 2 parathas for breakfast",
    total_calories=400,
    total_protein=12,
    parsed_items='[{"name": "paratha", "quantity": 2}]',
    items_extracted="2x paratha",
    timestamp=breakfast_time
)

# Get meal tag for a specific time
tag = get_meal_tag(datetime.now().replace(hour=13, minute=30))
print(tag)  # Output: "lunch"
```

### Query Meals with Tags

```python
# Get all meals for a user (includes meal_tag)
meals = db.get_all_meals(phone_number="whatsapp:+1234567890")
for meal in meals:
    print(f"{meal['timestamp']}: {meal['meal_tag']} - {meal['description']}")

# Get recent meals (includes meal_tag)
recent = db.get_recent_meals(phone_number="whatsapp:+1234567890", limit=5)
for meal in recent:
    tag_display = meal['meal_tag'].replace('_', ' ').title()
    print(f"{tag_display}: {meal['description']}")
```

### Export with Tags

```python
# Export to Excel with meal tags
success, message = db.export_to_excel(
    output_file="data/meals_with_tags.xlsx",
    phone_number="whatsapp:+1234567890"
)
```

## Benefits

1. **Automatic Categorization**: No need for users to manually specify meal type
2. **Pattern Analysis**: Users can see their eating patterns throughout the day
3. **Excel Reports**: Meal tags are included in Excel exports for easy analysis
4. **Flexible Queries**: Filter and analyze meals by tag
5. **Backwards Compatible**: Existing code continues to work without modifications

## Implementation Details

### Files Modified

1. **src/database.py**
   - Added `get_meal_tag()` helper function
   - Updated `init_database()` to add `meal_tag` column
   - Updated `log_meal()` to calculate and save meal tag
   - Updated `export_to_excel()` to include meal tag column
   - Updated `get_all_meals()` to return meal tag
   - Updated `get_recent_meals()` to return meal tag

2. **src/export_utils.py**
   - Updated `export_to_excel()` to include meal tag in exports

### Database Migration

The `init_database()` function includes automatic migration:

```python
# Add meal_tag column if it doesn't exist (for existing databases)
try:
    cursor.execute('ALTER TABLE meals ADD COLUMN meal_tag TEXT')
    conn.commit()
except sqlite3.OperationalError:
    # Column already exists
    pass
```

This ensures that existing databases are automatically updated without data loss.

## Testing

Run the test suite to verify the meal tag feature:

```bash
python test_meal_tags.py
```

The test suite validates:
- ✅ Meal tag function with various timestamps
- ✅ Meal logging with automatic tag assignment
- ✅ Excel export with meal tags
- ✅ Database queries returning meal tags

## Future Enhancements

Potential improvements for the meal tag feature:

1. **Custom Time Ranges**: Allow users to configure their own meal time ranges
2. **Tag-based Analytics**: Add summary reports grouped by meal tag
3. **Meal Tag Filtering**: Add API endpoints to filter meals by tag
4. **Visualization**: Charts showing calorie/protein distribution by meal tag
5. **Timezone Support**: Handle different timezones for international users

## Troubleshooting

### Issue: Meal tag showing as "N/A"

**Solution**: This occurs for meals logged before the meal tag feature was added. The system only tags new meals. Old meals will show "N/A" in the meal tag column.

### Issue: Wrong meal tag assigned

**Solution**: The tag is based on the timestamp when the meal was logged. If logging a past meal, provide the `timestamp` parameter to `log_meal()`.

### Issue: Excel export fails

**Solution**: Ensure `openpyxl` is installed:
```bash
pip install openpyxl==3.1.2
```
