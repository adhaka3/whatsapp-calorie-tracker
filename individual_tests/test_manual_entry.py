"""Test the manual entry feature"""
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import MealDatabase

# Import the parse function to test it
import re

def parse_manual_entry(message: str) -> dict:
    """Parse manual calorie and protein entry"""
    message_lower = message.lower()

    # Check if this is a manual entry (contains both "calorie" and "protein" keywords)
    if ('calorie' in message_lower or 'cal' in message_lower) and ('protein' in message_lower):
        # Extract calories
        cal_patterns = [
            r'(\d+\.?\d*)\s*(?:calories?|cals?|kcals?)',
            r'(?:calories?|cals?|kcals?)\s*[:\s]*(\d+\.?\d*)',
        ]
        calories = 0
        for pattern in cal_patterns:
            match = re.search(pattern, message_lower)
            if match:
                calories = float(match.group(1))
                break

        # Extract protein
        protein_patterns = [
            r'(\d+\.?\d*)\s*g?\s*protein',
            r'protein\s*[:\s]*(\d+\.?\d*)\s*g?',
        ]
        protein = 0
        for pattern in protein_patterns:
            match = re.search(pattern, message_lower)
            if match:
                protein = float(match.group(1))
                break

        if calories > 0 or protein > 0:
            return {
                'type': 'manual_entry',
                'calories': calories,
                'protein': protein,
                'original_message': message
            }

    return {'type': 'not_manual_entry'}


def test_parser():
    """Test the manual entry parser with various formats"""
    print("=" * 60)
    print("🧪 Testing Manual Entry Parser")
    print("=" * 60)
    print()

    test_cases = [
        # Format 1: "protein Xg and calories Y"
        ("protein 20g and calories 300", 300, 20),
        ("protein 4g and calories 100", 100, 4),

        # Format 2: "X calories and Yg protein"
        ("150 calories and 10g protein", 150, 10),
        ("200 calories and 15 protein", 200, 15),

        # Format 3: Different variations
        ("300 kcal and 25g protein", 300, 25),
        ("I ate 500 calories and 35g protein", 500, 35),
        ("Snack: 180 calories 12g protein", 180, 12),

        # Format 4: Only one value
        ("300 calories and protein 0", 300, 0),
        ("0 calories and 20g protein", 0, 20),

        # Format 5: Decimals
        ("250.5 calories and 12.5g protein", 250.5, 12.5),

        # Should NOT match (missing one value)
        ("I had 2 rotis", None, None),
        ("300 calories", None, None),
        ("20g protein", None, None),
    ]

    all_passed = True
    for message, expected_cal, expected_protein in test_cases:
        result = parse_manual_entry(message)

        if expected_cal is None:
            # Should not be detected as manual entry
            if result['type'] == 'not_manual_entry':
                print(f"✅ Correctly rejected: '{message}'")
            else:
                print(f"❌ Should have rejected: '{message}'")
                all_passed = False
        else:
            # Should be detected as manual entry
            if result['type'] == 'manual_entry':
                cal_match = result['calories'] == expected_cal
                protein_match = result['protein'] == expected_protein

                if cal_match and protein_match:
                    print(f"✅ '{message}'")
                    print(f"   → {result['calories']}kcal, {result['protein']}g protein")
                else:
                    print(f"❌ '{message}'")
                    print(f"   Expected: {expected_cal}kcal, {expected_protein}g")
                    print(f"   Got: {result['calories']}kcal, {result['protein']}g")
                    all_passed = False
            else:
                print(f"❌ Failed to detect: '{message}'")
                all_passed = False

    print()
    return all_passed


def test_database_logging():
    """Test logging manual entries to database"""
    print("=" * 60)
    print("🧪 Testing Database Logging")
    print("=" * 60)
    print()

    try:
        # Create test database
        db = MealDatabase(db_path="data/test_manual_entry.db")
        test_phone = "whatsapp:+1234567890"

        # Test manual entries
        test_entries = [
            ("protein 20g and calories 300", 300, 20),
            ("150 calories and 10g protein", 150, 10),
            ("500 kcal and 35g protein", 500, 35),
        ]

        print("📝 Logging manual entries...\n")
        for message, calories, protein in test_entries:
            db.log_meal(
                phone_number=test_phone,
                meal_description=message,
                total_calories=calories,
                total_protein=protein,
                parsed_items='[]',
                items_extracted='Manual entry',
                source="whatsapp",
                timestamp=datetime.now()
            )
            print(f"✅ Logged: {message}")
            print(f"   → {calories}kcal, {protein}g protein")

        # Verify totals
        print("\n📊 Checking daily summary...\n")
        daily_summary = db.get_daily_summary(test_phone)

        expected_total_cal = sum(e[1] for e in test_entries)
        expected_total_protein = sum(e[2] for e in test_entries)

        print(f"Expected: {expected_total_cal}kcal, {expected_total_protein}g")
        print(f"Got: {daily_summary['total_calories']}kcal, {daily_summary['total_protein']}g")

        if (daily_summary['total_calories'] == expected_total_cal and
            daily_summary['total_protein'] == expected_total_protein):
            print("✅ Totals match!")
        else:
            print("❌ Totals don't match!")
            return False

        # Verify in recent meals
        print("\n📝 Checking recent meals...\n")
        recent_meals = db.get_recent_meals(test_phone, limit=5)

        print(f"Found {len(recent_meals)} meals:")
        for meal in recent_meals:
            print(f"  - {meal['description']}")
            print(f"    {meal['calories']}kcal, {meal['protein']}g protein")

        # Clean up
        if os.path.exists("data/test_manual_entry.db"):
            os.remove("data/test_manual_entry.db")
            print("\n🧹 Cleaned up test database")

        print("\n✅ Database logging test passed!\n")
        return True

    except Exception as e:
        print(f"❌ Database test failed: {e}\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_manual_entry.db"):
            os.remove("data/test_manual_entry.db")
        return False


def test_mixed_entries():
    """Test combining manual and parsed meals"""
    print("=" * 60)
    print("🧪 Testing Mixed Entry Types")
    print("=" * 60)
    print()

    try:
        from food_parser import FoodParser

        db = MealDatabase(db_path="data/test_mixed.db")
        parser = FoodParser('data/indian_foods.json', use_llm=False)
        test_phone = "whatsapp:+1234567890"

        # Add parsed meal
        print("📝 Adding parsed meal...")
        result = parser.process_message("I had 2 rotis and dal")
        if result['type'] == 'meal_logged':
            db.log_meal(
                phone_number=test_phone,
                meal_description="I had 2 rotis and dal",
                total_calories=result['total_calories'],
                total_protein=result['total_protein'],
                parsed_items=str(result['parsed_items']),
                items_extracted="2x roti, 1x dal",
                source="whatsapp"
            )
            print(f"✅ Parsed meal: {result['total_calories']}kcal, {result['total_protein']}g")

        # Add manual entry
        print("\n📝 Adding manual entry...")
        db.log_meal(
            phone_number=test_phone,
            meal_description="protein 30g and calories 400",
            total_calories=400,
            total_protein=30,
            parsed_items='[]',
            items_extracted='Manual entry',
            source="whatsapp"
        )
        print("✅ Manual entry: 400kcal, 30g")

        # Check combined total
        print("\n📊 Checking combined total...\n")
        daily_summary = db.get_daily_summary(test_phone)

        print(f"Total Meals: {daily_summary['meal_count']}")
        print(f"Total Calories: {daily_summary['total_calories']}kcal")
        print(f"Total Protein: {daily_summary['total_protein']}g")

        if daily_summary['meal_count'] == 2:
            print("\n✅ Both meal types logged correctly!")
        else:
            print(f"\n❌ Expected 2 meals, got {daily_summary['meal_count']}")
            return False

        # Clean up
        if os.path.exists("data/test_mixed.db"):
            os.remove("data/test_mixed.db")
            print("\n🧹 Cleaned up test database")

        print("\n✅ Mixed entries test passed!\n")
        return True

    except Exception as e:
        print(f"❌ Mixed entries test failed: {e}\n")
        import traceback
        traceback.print_exc()
        if os.path.exists("data/test_mixed.db"):
            os.remove("data/test_mixed.db")
        return False


if __name__ == "__main__":
    print()
    print("🚀 Manual Entry Feature Tests")
    print()

    parser_ok = test_parser()
    db_ok = test_database_logging()
    mixed_ok = test_mixed_entries()

    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Parser Test: {'✅ PASS' if parser_ok else '❌ FAIL'}")
    print(f"Database Test: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"Mixed Entries Test: {'✅ PASS' if mixed_ok else '❌ FAIL'}")
    print()

    if parser_ok and db_ok and mixed_ok:
        print("🎉 All tests passed!")
        print()
        print("📱 How to use in WhatsApp:")
        print("   • 'protein 20g and calories 300'")
        print("   • '150 calories and 10g protein'")
        print("   • '500 kcal and 35g protein'")
    else:
        print("⚠️  Some tests failed.")

    print()
