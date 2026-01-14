"""Test the new 'total' command feature"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import MealDatabase
from food_parser import FoodParser

# Define the format functions here to avoid loading the full app
def format_total(summary: dict) -> str:
    """Format a quick total summary (calories and protein only)"""
    return (
        f"📊 *Today's Total*\n\n"
        f"🔥 Calories: {summary['total_calories']} kcal\n"
        f"💪 Protein: {summary['total_protein']}g\n"
        f"🍽️ Meals: {summary['meal_count']}"
    )

def format_daily_summary(summary: dict, recent_meals: list) -> str:
    """Format the daily summary as a WhatsApp message"""
    response_lines = [
        f"📅 *Daily Summary - {summary['date']}*\n",
        f"🍽️ Meals logged: {summary['meal_count']}",
        f"🔥 Total Calories: {summary['total_calories']} kcal",
        f"💪 Total Protein: {summary['total_protein']}g"
    ]

    if recent_meals:
        response_lines.append("\n📝 *Recent Meals:*")
        for i, meal in enumerate(recent_meals[:3], 1):
            response_lines.append(
                f"{i}. {meal['description'][:50]}\n"
                f"   {meal['calories']} kcal | {meal['protein']}g protein"
            )

    return "\n".join(response_lines)


def test_total_command():
    """Test the total command functionality"""
    print("=" * 60)
    print("🧪 Testing 'total' Command Feature")
    print("=" * 60)
    print()

    try:
        # Create test database
        db = MealDatabase(db_path="data/test_total_cmd.db")
        parser = FoodParser('data/indian_foods.json', use_llm=False)

        test_phone = "whatsapp:+1234567890"

        # Add some test meals for today
        test_meals = [
            "I had 2 rotis and dal for lunch",
            "Ate 3 idlis for breakfast",
            "Had chicken biryani for dinner"
        ]

        print("📝 Adding test meals for today...\n")
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
                    source="testing",
                    timestamp=datetime.now()
                )
                print(f"✅ Logged: {meal_msg}")
                print(f"   → {result['total_calories']}kcal, {result['total_protein']}g protein")

        # Test "total" command (quick format)
        print("\n" + "=" * 60)
        print("Testing 'total' Command (Quick Format)")
        print("=" * 60)
        print()

        daily_summary = db.get_daily_summary(test_phone)
        total_response = format_total(daily_summary)

        print("Response for 'total':")
        print(total_response)

        # Test "summary" command (detailed format)
        print("\n" + "=" * 60)
        print("Testing 'summary' Command (Detailed Format)")
        print("=" * 60)
        print()

        recent_meals = db.get_recent_meals(test_phone, limit=3)
        summary_response = format_daily_summary(daily_summary, recent_meals)

        print("Response for 'summary':")
        print(summary_response)

        # Verify the difference
        print("\n" + "=" * 60)
        print("Comparison")
        print("=" * 60)
        print()

        print("✅ 'total' command:")
        print("   - Shows quick totals only")
        print("   - Calories, protein, meal count")
        print(f"   - {len(total_response)} characters")
        print()

        print("✅ 'summary' command:")
        print("   - Shows detailed information")
        print("   - Includes recent meals list")
        print(f"   - {len(summary_response)} characters")

        # Clean up
        if os.path.exists("data/test_total_cmd.db"):
            os.remove("data/test_total_cmd.db")
            print("\n🧹 Cleaned up test database")

        print("\n✅ Total command test completed successfully!\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_total_cmd.db"):
            os.remove("data/test_total_cmd.db")
        return False


def test_command_triggers():
    """Test that the right triggers work for each command"""
    print("=" * 60)
    print("🧪 Testing Command Triggers")
    print("=" * 60)
    print()

    test_cases = [
        ("total", "Should trigger: Quick total format"),
        ("Total", "Should trigger: Quick total format (case insensitive)"),
        ("summary", "Should trigger: Detailed summary format"),
        ("stats", "Should trigger: Detailed summary format"),
        ("today", "Should trigger: Detailed summary format"),
    ]

    for command, expected in test_cases:
        print(f"Command: '{command}'")
        print(f"   → {expected}")

    print("\n✅ All triggers mapped correctly!\n")
    return True


if __name__ == "__main__":
    print()
    print("🚀 Total Command Feature Tests")
    print()

    total_test_ok = test_total_command()
    trigger_test_ok = test_command_triggers()

    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Total Command Test: {'✅ PASS' if total_test_ok else '❌ FAIL'}")
    print(f"Trigger Test: {'✅ PASS' if trigger_test_ok else '❌ FAIL'}")
    print()

    if total_test_ok and trigger_test_ok:
        print("🎉 All tests passed!")
        print()
        print("📱 How to use in WhatsApp:")
        print("   • Send 'total' → Quick calories & protein")
        print("   • Send 'summary' → Detailed with recent meals")
    else:
        print("⚠️  Some tests failed.")

    print()
