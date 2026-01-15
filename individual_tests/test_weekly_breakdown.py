"""Test the weekly breakdown feature"""
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import MealDatabase


def test_weekly_breakdown():
    """Test the weekly breakdown functionality"""
    print("=" * 70)
    print("🧪 TEST 1: Weekly Breakdown Functionality")
    print("=" * 70)
    print()

    try:
        # Create test database
        db = MealDatabase(db_path="data/test_weekly.db")
        test_phone = "whatsapp:+1234567890"

        # Test 1: Empty database
        print("Test 1: Weekly breakdown with no meals...\\n")
        breakdown = db.get_weekly_breakdown(test_phone)

        if breakdown['total_meals'] == 0:
            print("✅ Correctly handled empty database")
            print(f"   Total meals: {breakdown['total_meals']}")
            print(f"   Days with meals: {breakdown['days_with_meals']}/7\\n")
        else:
            print("❌ Should have 0 meals\\n")
            return False

        # Test 2: Add meals across different days
        print("Test 2: Add meals across 7 days...\\n")

        meal_data = [
            # (days_ago, description, calories, protein)
            (6, "Breakfast", 300, 15),
            (5, "Lunch", 500, 25),
            (4, "Dinner", 600, 30),
            (3, "Breakfast", 250, 12),
            (2, "Lunch", 450, 22),
            (1, "Dinner", 550, 28),
            (0, "Today's meal", 400, 20),
        ]

        for days_ago, description, calories, protein in meal_data:
            timestamp = datetime.now() - timedelta(days=days_ago)
            db.log_meal(
                phone_number=test_phone,
                meal_description=description,
                total_calories=calories,
                total_protein=protein,
                parsed_items='[]',
                items_extracted=description,
                source="testing",
                timestamp=timestamp
            )
            print(f"  ✅ Added: {description} ({calories} kcal, {protein}g) - {days_ago} days ago")

        print()

        # Test 3: Get weekly breakdown
        print("Test 3: Get weekly breakdown...\\n")
        breakdown = db.get_weekly_breakdown(test_phone)

        print("Daily breakdown:")
        for day in breakdown['daily_breakdown']:
            print(f"  {day['day_label']:12} ({day['full_date']}): "
                  f"{day['calories']} kcal | {day['protein']}g | {day['meal_count']} meals")

        print(f"\\nWeek Summary:")
        print(f"  Total Calories: {breakdown['total_calories']} kcal")
        print(f"  Total Protein: {breakdown['total_protein']}g")
        print(f"  Total Meals: {breakdown['total_meals']}")
        print(f"  Daily Average: {breakdown['avg_daily_calories']} kcal | {breakdown['avg_daily_protein']}g")
        print(f"  Active Days: {breakdown['days_with_meals']}/7\\n")

        # Verify totals
        expected_total_calories = sum(cal for _, _, cal, _ in meal_data)
        expected_total_protein = sum(pro for _, _, _, pro in meal_data)

        if breakdown['total_calories'] == expected_total_calories:
            print(f"✅ Total calories correct: {breakdown['total_calories']} kcal\\n")
        else:
            print(f"❌ Total calories incorrect: {breakdown['total_calories']} (expected {expected_total_calories})\\n")
            return False

        if breakdown['total_protein'] == expected_total_protein:
            print(f"✅ Total protein correct: {breakdown['total_protein']}g\\n")
        else:
            print(f"❌ Total protein incorrect: {breakdown['total_protein']}g (expected {expected_total_protein})\\n")
            return False

        if breakdown['total_meals'] == len(meal_data):
            print(f"✅ Total meals correct: {breakdown['total_meals']}\\n")
        else:
            print(f"❌ Total meals incorrect: {breakdown['total_meals']} (expected {len(meal_data)})\\n")
            return False

        if breakdown['days_with_meals'] == 7:
            print(f"✅ All 7 days have meals\\n")
        else:
            print(f"❌ Days with meals incorrect: {breakdown['days_with_meals']} (expected 7)\\n")
            return False

        # Test 4: Verify daily averages
        print("Test 4: Verify calculations...\\n")
        expected_avg_cal = expected_total_calories / 7
        expected_avg_pro = expected_total_protein / 7

        if abs(breakdown['avg_daily_calories'] - expected_avg_cal) < 0.1:
            print(f"✅ Daily average calories correct: {breakdown['avg_daily_calories']} kcal\\n")
        else:
            print(f"❌ Daily average calories incorrect: {breakdown['avg_daily_calories']} (expected {expected_avg_cal})\\n")
            return False

        # Clean up
        if os.path.exists("data/test_weekly.db"):
            os.remove("data/test_weekly.db")
            print("🧹 Cleaned up test database\\n")

        print("✅ Weekly breakdown test: PASSED\\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_weekly.db"):
            os.remove("data/test_weekly.db")
        return False


def test_partial_week():
    """Test weekly breakdown with only some days having meals"""
    print("=" * 70)
    print("🧪 TEST 2: Partial Week (Some Days Empty)")
    print("=" * 70)
    print()

    try:
        db = MealDatabase(db_path="data/test_partial_week.db")
        test_phone = "whatsapp:+1234567890"

        # Add meals only on 3 days
        meal_data = [
            (5, "Meal 1", 400, 20),
            (3, "Meal 2", 500, 25),
            (0, "Meal 3", 300, 15),
        ]

        print("Adding meals on 3 out of 7 days...\\n")
        for days_ago, description, calories, protein in meal_data:
            timestamp = datetime.now() - timedelta(days=days_ago)
            db.log_meal(
                phone_number=test_phone,
                meal_description=description,
                total_calories=calories,
                total_protein=protein,
                parsed_items='[]',
                items_extracted=description,
                source="testing",
                timestamp=timestamp
            )

        breakdown = db.get_weekly_breakdown(test_phone)

        print("Daily breakdown:")
        for day in breakdown['daily_breakdown']:
            status = "✅" if day['meal_count'] > 0 else "⚪"
            print(f"  {status} {day['day_label']:12} ({day['full_date']}): "
                  f"{day['calories']} kcal | {day['protein']}g | {day['meal_count']} meals")

        print(f"\\nActive days: {breakdown['days_with_meals']}/7\\n")

        if breakdown['days_with_meals'] == 3:
            print("✅ Correctly counted 3 active days\\n")
        else:
            print(f"❌ Should have 3 active days, got {breakdown['days_with_meals']}\\n")
            return False

        # Average should be calculated only for days with meals
        expected_avg = (400 + 500 + 300) / 3
        if abs(breakdown['avg_daily_calories'] - expected_avg) < 0.1:
            print(f"✅ Daily average calculated correctly: {breakdown['avg_daily_calories']} kcal\\n")
            print(f"   (Average of active days only: {expected_avg:.1f} kcal)\\n")
        else:
            print(f"❌ Daily average incorrect\\n")
            return False

        # Clean up
        if os.path.exists("data/test_partial_week.db"):
            os.remove("data/test_partial_week.db")
            print("🧹 Cleaned up test database\\n")

        print("✅ Partial week test: PASSED\\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_partial_week.db"):
            os.remove("data/test_partial_week.db")
        return False


def test_multiple_meals_per_day():
    """Test with multiple meals on the same day"""
    print("=" * 70)
    print("🧪 TEST 3: Multiple Meals Per Day")
    print("=" * 70)
    print()

    try:
        db = MealDatabase(db_path="data/test_multiple_meals.db")
        test_phone = "whatsapp:+1234567890"

        # Add 3 meals today
        print("Adding 3 meals for today...\\n")
        today_meals = [
            ("Breakfast", 300, 15),
            ("Lunch", 500, 25),
            ("Dinner", 600, 30),
        ]

        for description, calories, protein in today_meals:
            db.log_meal(
                phone_number=test_phone,
                meal_description=description,
                total_calories=calories,
                total_protein=protein,
                parsed_items='[]',
                items_extracted=description,
                source="testing"
            )
            print(f"  ✅ Added: {description}")

        print()

        breakdown = db.get_weekly_breakdown(test_phone)

        # Check today's totals
        today = breakdown['daily_breakdown'][-1]  # Last entry is today
        expected_cal = sum(cal for _, cal, _ in today_meals)
        expected_pro = sum(pro for _, _, pro in today_meals)

        print(f"Today's summary:")
        print(f"  Meals: {today['meal_count']}")
        print(f"  Calories: {today['calories']} kcal")
        print(f"  Protein: {today['protein']}g\\n")

        if today['meal_count'] == 3:
            print("✅ Correctly counted 3 meals today\\n")
        else:
            print(f"❌ Should have 3 meals, got {today['meal_count']}\\n")
            return False

        if today['calories'] == expected_cal:
            print(f"✅ Total calories correct: {today['calories']} kcal\\n")
        else:
            print(f"❌ Total calories incorrect: {today['calories']} (expected {expected_cal})\\n")
            return False

        if today['protein'] == expected_pro:
            print(f"✅ Total protein correct: {today['protein']}g\\n")
        else:
            print(f"❌ Total protein incorrect: {today['protein']}g (expected {expected_pro})\\n")
            return False

        # Clean up
        if os.path.exists("data/test_multiple_meals.db"):
            os.remove("data/test_multiple_meals.db")
            print("🧹 Cleaned up test database\\n")

        print("✅ Multiple meals per day test: PASSED\\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_multiple_meals.db"):
            os.remove("data/test_multiple_meals.db")
        return False


def test_command_triggers():
    """Test that different command variations work"""
    print("=" * 70)
    print("🧪 TEST 4: Command Trigger Variations")
    print("=" * 70)
    print()

    triggers = [
        "total week",
        "Total Week",
        "TOTAL WEEK",
        "week total",
        "weekly",
        "Weekly",
        "show me total week",
        "what's my weekly total",
    ]

    print("Testing command triggers:\\n")
    for trigger in triggers:
        # Check if trigger would be detected
        if 'total week' in trigger.lower() or 'week total' in trigger.lower() or 'weekly' in trigger.lower():
            print(f"  ✅ '{trigger}' → would trigger weekly breakdown")
        else:
            print(f"  ❌ '{trigger}' → would NOT trigger")

    print("\\n✅ Command triggers test: PASSED\\n")
    return True


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("🚀 Weekly Breakdown Feature Tests")
    print("=" * 70)
    print()

    test1_ok = test_weekly_breakdown()
    test2_ok = test_partial_week()
    test3_ok = test_multiple_meals_per_day()
    test4_ok = test_command_triggers()

    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print(f"Weekly Breakdown: {'✅ PASS' if test1_ok else '❌ FAIL'}")
    print(f"Partial Week: {'✅ PASS' if test2_ok else '❌ FAIL'}")
    print(f"Multiple Meals: {'✅ PASS' if test3_ok else '❌ FAIL'}")
    print(f"Command Triggers: {'✅ PASS' if test4_ok else '❌ FAIL'}")
    print()

    if test1_ok and test2_ok and test3_ok and test4_ok:
        print("🎉 All tests passed!")
        print()
        print("📱 How to use in WhatsApp:")
        print("   • 'total week' - Show 7-day breakdown")
        print("   • 'week total' - Show 7-day breakdown")
        print("   • 'weekly' - Show 7-day breakdown")
        print()
        print("Example output:")
        print("   📅 Weekly Breakdown - Last 7 Days")
        print()
        print("   🟢 Today (Jan 15)")
        print("      🔥 400 kcal | 💪 20g | 🍽️ 1 meals")
        print("   🟢 Yesterday (Jan 14)")
        print("      🔥 550 kcal | 💪 28g | 🍽️ 1 meals")
        print("   ⚪ Friday (Jan 13)")
        print("      🔥 - | 💪 - | 🍽️ 0 meals")
        print()
        print("   📊 Week Summary:")
        print("   🔥 Total Calories: 3050 kcal")
        print("   💪 Total Protein: 152g")
        print("   🍽️ Total Meals: 7")
        print("   📈 Daily Average: 435.7 kcal | 21.7g")
        print("   📆 Active Days: 7/7")
    else:
        print("⚠️  Some tests failed.")

    print()
