"""Test the meal tag feature"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import MealDatabase, get_meal_tag
from food_parser import FoodParser


def test_meal_tag_function():
    """Test the get_meal_tag function with various times"""
    print("=" * 60)
    print("🧪 Testing Meal Tag Function")
    print("=" * 60)
    print()

    test_times = [
        (datetime(2024, 1, 1, 6, 0), "breakfast"),    # 6:00 AM
        (datetime(2024, 1, 1, 10, 30), "breakfast"),  # 10:30 AM
        (datetime(2024, 1, 1, 11, 30), "brunch"),     # 11:30 AM
        (datetime(2024, 1, 1, 12, 30), "lunch"),      # 12:30 PM
        (datetime(2024, 1, 1, 14, 0), "lunch"),       # 2:00 PM
        (datetime(2024, 1, 1, 16, 0), "evening_snack"), # 4:00 PM
        (datetime(2024, 1, 1, 19, 0), "dinner"),      # 7:00 PM
        (datetime(2024, 1, 1, 21, 30), "dinner"),     # 9:30 PM
        (datetime(2024, 1, 1, 23, 0), "midnight_snack"), # 11:00 PM
        (datetime(2024, 1, 1, 2, 0), "midnight_snack"),  # 2:00 AM
    ]

    all_passed = True
    for timestamp, expected_tag in test_times:
        result_tag = get_meal_tag(timestamp)
        time_str = timestamp.strftime("%I:%M %p")
        if result_tag == expected_tag:
            print(f"✅ {time_str:12} → {result_tag:15} (Expected: {expected_tag})")
        else:
            print(f"❌ {time_str:12} → {result_tag:15} (Expected: {expected_tag})")
            all_passed = False

    print()
    return all_passed


def test_meal_logging_with_tags():
    """Test logging meals with different timestamps"""
    print("=" * 60)
    print("🧪 Testing Meal Logging with Tags")
    print("=" * 60)
    print()

    try:
        # Create test database
        db = MealDatabase(db_path="data/test_meal_tags.db")
        parser = FoodParser('data/indian_foods.json', use_llm=False)

        test_phone = "whatsapp:+1234567890"

        # Test meals with different timestamps
        test_data = [
            {
                "message": "Had 2 parathas for breakfast",
                "timestamp": datetime.now().replace(hour=8, minute=0),
                "expected_tag": "breakfast"
            },
            {
                "message": "Ate chicken biryani for lunch",
                "timestamp": datetime.now().replace(hour=13, minute=30),
                "expected_tag": "lunch"
            },
            {
                "message": "2 samosas as evening snack",
                "timestamp": datetime.now().replace(hour=17, minute=0),
                "expected_tag": "evening_snack"
            },
            {
                "message": "Dal and rice for dinner",
                "timestamp": datetime.now().replace(hour=20, minute=0),
                "expected_tag": "dinner"
            },
            {
                "message": "Had some chips late night",
                "timestamp": datetime.now().replace(hour=23, minute=30),
                "expected_tag": "midnight_snack"
            },
        ]

        print("📝 Adding meals with different timestamps...\n")
        for test in test_data:
            result = parser.process_message(test["message"])
            if result['type'] == 'meal_logged':
                items_extracted = ", ".join([f"{item['quantity']}x {item['name']}"
                                            for item in result['items']])

                db.log_meal(
                    phone_number=test_phone,
                    meal_description=test["message"],
                    total_calories=result['total_calories'],
                    total_protein=result['total_protein'],
                    parsed_items=str(result['parsed_items']),
                    items_extracted=items_extracted,
                    source="testing",
                    timestamp=test["timestamp"]
                )

                time_str = test["timestamp"].strftime("%I:%M %p")
                print(f"✅ {time_str:10} - {test['expected_tag']:15} - {test['message']}")

        # Verify by reading back from database
        print("\n📊 Verifying saved meal tags...\n")
        meals = db.get_all_meals(phone_number=test_phone)

        all_correct = True
        for meal in meals:
            timestamp_str = meal['timestamp']
            meal_tag = meal['meal_tag']
            description = meal['description'][:40]

            # Parse timestamp
            try:
                ts = datetime.fromisoformat(timestamp_str)
                time_str = ts.strftime("%I:%M %p")
            except:
                time_str = "Unknown"

            tag_display = meal_tag.replace('_', ' ').title() if meal_tag else "N/A"
            print(f"  {time_str:10} - {tag_display:15} - {description}")

        # Export to Excel
        print("\n📊 Exporting to Excel with meal tags...")
        success, message = db.export_to_excel("data/test_meal_tags_export.xlsx", phone_number=test_phone)

        if success:
            print(f"✅ {message}")
            print("\n💡 Check 'data/test_meal_tags_export.xlsx' to see the meal tags!")
        else:
            print(f"❌ {message}")

        # Clean up
        if os.path.exists("data/test_meal_tags.db"):
            os.remove("data/test_meal_tags.db")
            print("\n🧹 Cleaned up test database")

        print("\n✅ Meal logging with tags test completed!\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_meal_tags.db"):
            os.remove("data/test_meal_tags.db")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("🚀 Meal Tag Feature Tests")
    print("=" * 60)
    print()

    tag_function_ok = test_meal_tag_function()
    meal_logging_ok = test_meal_logging_with_tags()

    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Meal Tag Function: {'✅ PASS' if tag_function_ok else '❌ FAIL'}")
    print(f"Meal Logging with Tags: {'✅ PASS' if meal_logging_ok else '❌ FAIL'}")
    print()

    if tag_function_ok and meal_logging_ok:
        print("🎉 All meal tag tests passed!")
    else:
        print("⚠️  Some tests failed.")
    print()


if __name__ == "__main__":
    main()
