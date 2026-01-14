"""Demo script showing Excel export functionality"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import MealDatabase
from food_parser import FoodParser

def demo_export():
    """Demonstrate Excel export feature"""
    print("=" * 60)
    print("📊 Excel Export Demo")
    print("=" * 60)
    print()
    
    # Initialize
    db = MealDatabase(db_path="data/meals.db")
    parser = FoodParser('data/indian_foods.json', use_llm=False)
    
    # Add some demo meals
    test_user = "whatsapp:+919876543210"
    demo_meals = [
        "Had 2 rotis and dal for lunch",
        "Breakfast: 3 idlis with sambar",
        "Dinner was chicken biryani",
        "Evening snack: 2 samosas and chai"
    ]
    
    print("📝 Adding demo meals...\n")
    for msg in demo_meals:
        result = parser.process_message(msg)
        if result['type'] == 'meal_logged':
            items_extracted = ", ".join([f"{item['quantity']}x {item['name']}" 
                                        for item in result['items']])
            
            db.log_meal(
                phone_number=test_user,
                meal_description=msg,
                total_calories=result['total_calories'],
                total_protein=result['total_protein'],
                parsed_items=str(result['parsed_items']),
                items_extracted=items_extracted,
                source="demo"
            )
            print(f"✅ Logged: {msg}")
            print(f"   → {items_extracted}")
            print(f"   → {result['total_calories']}kcal, {result['total_protein']}g protein\n")
    
    # Export all meals
    print("\n📊 Exporting all meals to Excel...")
    success, message = db.export_to_excel("data/all_meals.xlsx")
    print(f"{'✅' if success else '❌'} {message}")
    
    # Export for specific user
    print("\n📊 Exporting meals for specific user...")
    success, message = db.export_to_excel("data/user_meals.xlsx", phone_number=test_user)
    print(f"{'✅' if success else '❌'} {message}")
    
    # Show daily summary
    print("\n📈 Daily Summary:")
    summary = db.get_daily_summary(test_user)
    print(f"   Meals: {summary['meal_count']}")
    print(f"   Total Calories: {summary['total_calories']} kcal")
    print(f"   Total Protein: {summary['total_protein']}g")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete!")
    print("=" * 60)
    print()
    print("📁 Files created:")
    print("   - data/all_meals.xlsx (all users)")
    print("   - data/user_meals.xlsx (specific user)")
    print()
    print("💡 Open these files in Excel/Google Sheets!")
    print()


if __name__ == "__main__":
    demo_export()
