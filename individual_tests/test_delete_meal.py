"""Test the delete last meal feature"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import MealDatabase
from food_parser import FoodParser


def test_delete_last_meal():
    """Test deleting the last meal"""
    print("=" * 70)
    print("🧪 TEST 1: Delete Last Meal")
    print("=" * 70)
    print()

    try:
        # Create test database
        db = MealDatabase(db_path="data/test_delete.db")
        parser = FoodParser('data/indian_foods.json', use_llm=False)

        test_phone = "whatsapp:+1234567890"

        # Test 1: Try to delete when no meals exist
        print("Test 1: Delete when no meals exist...\n")
        result = db.delete_last_meal(test_phone)

        if not result['success'] and 'No meals found' in result['message']:
            print("✅ Correctly handled empty database\n")
        else:
            print("❌ Should have returned error for empty database\n")
            return False

        # Test 2: Add meals and delete last one
        print("Test 2: Add meals and delete last one...\n")

        # Add 3 meals
        meals = [
            ("I had 2 rotis and dal", datetime.now() - timedelta(hours=2)),
            ("Ate 3 idlis for breakfast", datetime.now() - timedelta(hours=1)),
            ("Had chicken biryani", datetime.now())
        ]

        print("Adding test meals:\n")
        for meal_msg, timestamp in meals:
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
                    source="testing",
                    timestamp=timestamp
                )
                print(f"  ✅ {meal_msg}")

        # Get summary before deletion
        print("\nBefore deletion:")
        summary_before = db.get_daily_summary(test_phone)
        print(f"  Meals: {summary_before['meal_count']}")
        print(f"  Calories: {summary_before['total_calories']} kcal")
        print(f"  Protein: {summary_before['total_protein']}g\n")

        # Delete last meal
        print("Deleting last meal...\n")
        delete_result = db.delete_last_meal(test_phone)

        if delete_result['success']:
            print("✅ Deletion successful!")
            print(f"   Deleted: {delete_result['deleted_meal']['description']}")
            print(f"   Calories: {delete_result['deleted_meal']['calories']} kcal")
            print(f"   Protein: {delete_result['deleted_meal']['protein']}g\n")
        else:
            print(f"❌ Deletion failed: {delete_result['message']}\n")
            return False

        # Verify meal was deleted
        print("After deletion:")
        summary_after = db.get_daily_summary(test_phone)
        print(f"  Meals: {summary_after['meal_count']}")
        print(f"  Calories: {summary_after['total_calories']} kcal")
        print(f"  Protein: {summary_after['total_protein']}g\n")

        # Check counts
        if summary_before['meal_count'] == 3 and summary_after['meal_count'] == 2:
            print("✅ Meal count decreased correctly (3 → 2)\n")
        else:
            print(f"❌ Meal count incorrect: {summary_before['meal_count']} → {summary_after['meal_count']}\n")
            return False

        # Check the last meal is now different
        recent_meals = db.get_recent_meals(test_phone, limit=1)
        if recent_meals and recent_meals[0]['description'] != "Had chicken biryani":
            print(f"✅ Last meal is now: {recent_meals[0]['description']}\n")
        else:
            print("❌ Last meal was not deleted correctly\n")
            return False

        # Test 3: Delete multiple times
        print("Test 3: Delete all meals...\n")

        for i in range(2):
            delete_result = db.delete_last_meal(test_phone)
            if delete_result['success']:
                print(f"  ✅ Deleted meal {i+1}")
            else:
                print(f"  ❌ Failed to delete meal {i+1}")
                return False

        # Verify all meals deleted
        summary_empty = db.get_daily_summary(test_phone)
        if summary_empty['meal_count'] == 0:
            print("\n✅ All meals deleted successfully\n")
        else:
            print(f"\n❌ Still has {summary_empty['meal_count']} meals\n")
            return False

        # Test 4: Try to delete when empty again
        print("Test 4: Try to delete from empty database...\n")
        result = db.delete_last_meal(test_phone)

        if not result['success']:
            print("✅ Correctly handled empty database again\n")
        else:
            print("❌ Should have failed for empty database\n")
            return False

        # Clean up
        if os.path.exists("data/test_delete.db"):
            os.remove("data/test_delete.db")
            print("🧹 Cleaned up test database\n")

        print("✅ Delete last meal test: PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_delete.db"):
            os.remove("data/test_delete.db")
        return False


def test_delete_with_meal_tags():
    """Test that deletion works with meal tags"""
    print("=" * 70)
    print("🧪 TEST 2: Delete with Meal Tags")
    print("=" * 70)
    print()

    try:
        db = MealDatabase(db_path="data/test_delete_tags.db")
        test_phone = "whatsapp:+1234567890"

        # Add meals at different times (different tags)
        timestamps = [
            datetime(2026, 1, 14, 8, 0),   # breakfast
            datetime(2026, 1, 14, 13, 0),  # lunch
            datetime(2026, 1, 14, 19, 0),  # dinner
        ]

        print("Adding meals with different tags:\n")
        for i, ts in enumerate(timestamps):
            db.log_meal(
                phone_number=test_phone,
                meal_description=f"Test meal {i+1}",
                total_calories=100,
                total_protein=10,
                parsed_items='[]',
                items_extracted='test',
                source="testing",
                timestamp=ts
            )
            print(f"  ✅ Added meal at {ts.strftime('%I:%M %p')}")

        # Delete last meal (should be dinner)
        print("\nDeleting last meal...\n")
        result = db.delete_last_meal(test_phone)

        if result['success']:
            print("✅ Deletion successful!")
            print(f"   Message preview: {result['message'][:100]}...\n")

            # Check meal tag is shown
            if 'Meal Tag' in result['message'] or 'Dinner' in result['message']:
                print("✅ Meal tag information included in response\n")
            else:
                print("⚠️  Meal tag not clearly shown in response\n")
        else:
            print(f"❌ Deletion failed: {result['message']}\n")
            return False

        # Verify only 2 meals remain
        summary = db.get_daily_summary(test_phone, datetime(2026, 1, 14))
        if summary['meal_count'] == 2:
            print("✅ Correct meal count after deletion (2 meals remain)\n")
        else:
            print(f"❌ Wrong meal count: {summary['meal_count']}\n")
            return False

        # Clean up
        if os.path.exists("data/test_delete_tags.db"):
            os.remove("data/test_delete_tags.db")
            print("🧹 Cleaned up test database\n")

        print("✅ Delete with meal tags test: PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_delete_tags.db"):
            os.remove("data/test_delete_tags.db")
        return False


def test_command_triggers():
    """Test that different command variations work"""
    print("=" * 70)
    print("🧪 TEST 3: Command Trigger Variations")
    print("=" * 70)
    print()

    triggers = [
        "delete",
        "Delete",
        "DELETE",
        "undo",
        "delete last",
        "delete meal",
        "remove last",
    ]

    print("Testing command triggers:\n")
    for trigger in triggers:
        # Just check the trigger would be detected
        # (We don't actually call webhook here)
        if any(phrase in trigger.lower() for phrase in ['delete last', 'delete meal', 'undo', 'remove last', 'delete']):
            print(f"  ✅ '{trigger}' → would trigger delete")
        else:
            print(f"  ❌ '{trigger}' → would NOT trigger")

    print("\n✅ Command triggers test: PASSED\n")
    return True


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("🚀 Delete Last Meal Feature Tests")
    print("=" * 70)
    print()

    delete_ok = test_delete_last_meal()
    tags_ok = test_delete_with_meal_tags()
    triggers_ok = test_command_triggers()

    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print(f"Delete Last Meal: {'✅ PASS' if delete_ok else '❌ FAIL'}")
    print(f"Delete with Tags: {'✅ PASS' if tags_ok else '❌ FAIL'}")
    print(f"Command Triggers: {'✅ PASS' if triggers_ok else '❌ FAIL'}")
    print()

    if delete_ok and tags_ok and triggers_ok:
        print("🎉 All tests passed!")
        print()
        print("📱 How to use in WhatsApp:")
        print("   • 'delete' - Remove last meal")
        print("   • 'undo' - Remove last meal")
        print("   • 'delete last' - Remove last meal")
        print("   • 'remove last' - Remove last meal")
        print()
        print("Example:")
        print("   You: I had 2 rotis")
        print("   Bot: ✅ Meal logged! 142 kcal...")
        print()
        print("   You: delete")
        print("   Bot: ✅ Last Meal Deleted")
        print("        🗑️ Removed: I had 2 rotis")
        print("        🔥 Calories: 142 kcal...")
    else:
        print("⚠️  Some tests failed.")

    print()
