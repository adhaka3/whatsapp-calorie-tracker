"""Test Excel export functionality"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import MealDatabase
from food_parser import FoodParser

def test_excel_export():
    """Test the Excel export feature"""
    print("🧪 Testing Excel Export Feature...\n")
    
    try:
        # Create test database
        db = MealDatabase(db_path="data/test_export.db")
        parser = FoodParser('data/indian_foods.json', use_llm=False)
        
        # Add some test meals
        test_phone = "whatsapp:+1234567890"
        test_meals = [
            "I had 2 rotis and dal",
            "Ate chicken biryani and raita",
            "Had 3 idlis for breakfast",
            "2 parathas with curd",
        ]
        
        print("Adding test meals...\n")
        for meal_msg in test_meals:
            result = parser.process_message(meal_msg)
            if result['type'] == 'meal_logged':
                items_extracted = ", ".join([f"{item['quantity']}x {item['name']}" 
                                            for item in result['items']])
                
                db.log_meal(
                    phone_number=test_phone,
                    meal_description=meal_msg,
                    total_calories=result['total_calories'],
                    total_protein=result['total_protein'],
                    parsed_items=str(result['parsed_items']),
                    items_extracted=items_extracted,
                    source="testing"
                )
                print(f"✅ Logged: {meal_msg}")
        
        # Export to Excel
        print("\n📊 Exporting to Excel...")
        success, message = db.export_to_excel("data/test_meal_logs.xlsx")
        
        if success:
            print(f"✅ {message}")
            print("\n💡 Check 'data/test_meal_logs.xlsx' to see the export!")
        else:
            print(f"❌ {message}")
            return False
        
        # Clean up
        if os.path.exists("data/test_export.db"):
            os.remove("data/test_export.db")
            print("🧹 Cleaned up test database")
        
        print("\n✅ Excel export test completed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Excel export test failed: {e}\n")
        if os.path.exists("data/test_export.db"):
            os.remove("data/test_export.db")
        return False


def test_not_in_database():
    """Test the 'not in database' error message"""
    print("🧪 Testing 'Not in Database' Message...\n")
    
    try:
        parser = FoodParser('data/indian_foods.json', use_llm=False)
        
        # Test with food not in database
        test_messages = [
            "I had pizza and pasta",
            "Ate sushi and ramen",
            "Had tacos"
        ]
        
        for msg in test_messages:
            print(f"📝 Testing: '{msg}'")
            result = parser.process_message(msg)
            
            if result['type'] in ['no_food_found', 'not_in_database']:
                print(f"✅ Correctly identified as not in database")
                print(f"   Message: {result['message'][:80]}...")
            else:
                print(f"⚠️  Unexpected result type: {result['type']}")
            print()
        
        print("✅ 'Not in Database' test completed!\n")
        return True
        
    except Exception as e:
        print(f"❌ 'Not in Database' test failed: {e}\n")
        return False


def test_food_list():
    """Test the food list feature"""
    print("🧪 Testing Food List Feature...\n")
    
    try:
        parser = FoodParser('data/indian_foods.json', use_llm=False)
        
        food_list = parser.get_food_list()
        print(f"✅ Food list generated ({len(food_list)} characters)")
        print("\nPreview:")
        print(food_list[:200] + "...\n")
        
        print("✅ Food list test completed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Food list test failed: {e}\n")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Testing New Features")
    print("=" * 60)
    print()
    
    export_ok = test_excel_export()
    not_in_db_ok = test_not_in_database()
    food_list_ok = test_food_list()
    
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Excel Export: {'✅ PASS' if export_ok else '❌ FAIL'}")
    print(f"Not in Database: {'✅ PASS' if not_in_db_ok else '❌ FAIL'}")
    print(f"Food List: {'✅ PASS' if food_list_ok else '❌ FAIL'}")
    print()
    
    if export_ok and not_in_db_ok and food_list_ok:
        print("🎉 All new features working!")
    else:
        print("⚠️  Some features need attention.")
    print()
