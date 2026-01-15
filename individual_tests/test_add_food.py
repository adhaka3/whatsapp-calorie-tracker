"""Test the add custom food feature"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from food_parser import FoodParser
import json
import shutil


def test_parse_add_command():
    """Test parsing add food commands"""
    print("=" * 70)
    print("🧪 TEST 1: Parse Add Food Commands")
    print("=" * 70)
    print()

    parser = FoodParser('data/indian_foods.json', use_llm=False)

    test_cases = [
        # Format 1: Space-separated
        ("add protein shake 120 30 1 scoop", True, {
            'name': 'protein shake',
            'calories': 120.0,
            'protein': 30.0,
            'serving': '1 scoop'
        }),

        # Format 2: Comma-separated
        ("add pizza slice, 285, 12, 1 slice (100g)", True, {
            'name': 'pizza slice',
            'calories': 285.0,
            'protein': 12.0,
            'serving': '1 slice (100g)'
        }),

        # Format 3: Pipe-separated
        ("add oats | 150 | 5 | 1 bowl", True, {
            'name': 'oats',
            'calories': 150.0,
            'protein': 5.0,
            'serving': '1 bowl'
        }),

        # Format 4: Mixed case
        ("ADD Protein Bar 200 15 1 bar (60g)", True, {
            'name': 'Protein Bar',
            'calories': 200.0,
            'protein': 15.0,
            'serving': '1 bar (60g)'
        }),

        # Error case: Not enough parts
        ("add protein shake 120", False, None),

        # Error case: Invalid number (using comma format for clearer test)
        ("add protein shake, abc, 30, 1 scoop", False, None),
    ]

    all_passed = True
    for message, should_succeed, expected in test_cases:
        print(f"📝 Testing: '{message}'")
        result = parser.parse_add_food_command(message)

        if should_succeed:
            if result['type'] == 'add_food':
                # Check if all values match
                name_match = result['name'].lower() == expected['name'].lower()
                cal_match = result['calories'] == expected['calories']
                protein_match = result['protein'] == expected['protein']
                serving_match = result['serving_size'] == expected['serving']

                if name_match and cal_match and protein_match and serving_match:
                    print(f"✅ Parsed correctly")
                    print(f"   Name: {result['name']}")
                    print(f"   Calories: {result['calories']} kcal")
                    print(f"   Protein: {result['protein']}g")
                    print(f"   Serving: {result['serving_size']}")
                else:
                    print(f"❌ Parse mismatch")
                    all_passed = False
            else:
                print(f"❌ Expected success but got: {result['type']}")
                all_passed = False
        else:
            if result['type'] == 'parse_error':
                print(f"✅ Correctly identified as invalid format")
            else:
                print(f"❌ Should have failed but got: {result['type']}")
                all_passed = False

        print()

    if all_passed:
        print("✅ Parse add command test: PASSED\n")
    else:
        print("❌ Parse add command test: FAILED\n")

    return all_passed


def test_add_custom_food():
    """Test adding custom foods to database"""
    print("=" * 70)
    print("🧪 TEST 2: Add Custom Foods to Database")
    print("=" * 70)
    print()

    # Create a copy of the food database for testing
    test_db_path = 'data/test_indian_foods.json'
    shutil.copy('data/indian_foods.json', test_db_path)

    try:
        parser = FoodParser(test_db_path, use_llm=False)
        initial_count = len(parser.food_db)

        print(f"Initial food count: {initial_count}\n")

        # Test 1: Add a new food
        print("Test 1: Adding a new food...\n")
        result = parser.add_custom_food(
            name="protein shake",
            calories=120,
            protein=30,
            serving_size="1 scoop (30g)"
        )

        if result['success']:
            print(f"✅ {result['message']}\n")
        else:
            print(f"❌ {result['message']}\n")
            return False

        # Verify it was added
        if 'protein shake' in parser.food_index:
            print("✅ Food found in index\n")
        else:
            print("❌ Food not found in index\n")
            return False

        # Test 2: Try to add duplicate
        print("Test 2: Trying to add duplicate...\n")
        result = parser.add_custom_food(
            name="protein shake",
            calories=150,
            protein=25,
            serving_size="1 scoop"
        )

        if not result['success'] and 'already exists' in result['message']:
            print(f"✅ Correctly rejected duplicate\n")
        else:
            print(f"❌ Should have rejected duplicate\n")
            return False

        # Test 3: Add another food
        print("Test 3: Adding another food...\n")
        result = parser.add_custom_food(
            name="energy bar",
            calories=250,
            protein=10,
            serving_size="1 bar (50g)"
        )

        if result['success']:
            print(f"✅ {result['message']}\n")
        else:
            print(f"❌ {result['message']}\n")
            return False

        # Test 4: Verify JSON file was updated
        print("Test 4: Verifying JSON file...\n")
        with open(test_db_path, 'r') as f:
            saved_foods = json.load(f)

        if len(saved_foods) == initial_count + 2:
            print(f"✅ JSON file updated correctly ({initial_count} → {len(saved_foods)} foods)\n")
        else:
            print(f"❌ JSON file not updated correctly\n")
            return False

        # Test 5: Verify we can track the new food
        print("Test 5: Testing meal logging with new food...\n")
        # Reload parser to get updated database
        parser = FoodParser(test_db_path, use_llm=False)
        result = parser.process_message("I had 2 protein shake")

        if result['type'] == 'meal_logged':
            print(f"✅ New food can be tracked!")
            print(f"   Meal: 2x protein shake")
            print(f"   Calories: {result['total_calories']} kcal")
            print(f"   Protein: {result['total_protein']}g")
        else:
            print(f"❌ Failed to track new food: {result.get('type')}\n")
            return False

        print("\n✅ Add custom food test: PASSED\n")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Clean up test database
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("🧹 Cleaned up test database\n")


def test_validation():
    """Test validation rules"""
    print("=" * 70)
    print("🧪 TEST 3: Validation Rules")
    print("=" * 70)
    print()

    # Create test database
    test_db_path = 'data/test_validation.json'
    shutil.copy('data/indian_foods.json', test_db_path)

    try:
        parser = FoodParser(test_db_path, use_llm=False)

        test_cases = [
            # (name, calories, protein, serving, should_succeed, error_contains)
            ("", 100, 10, "1 serving", False, "empty"),
            ("test food", 0, 10, "1 serving", False, "must be > 0"),
            ("test food", -100, 10, "1 serving", False, "must be > 0"),
            ("test food", 100, -5, "1 serving", False, "must be >= 0"),
            ("valid food", 100, 10, "1 serving", True, None),
        ]

        all_passed = True
        for name, cal, protein, serving, should_succeed, error_text in test_cases:
            print(f"📝 Testing: name='{name}', cal={cal}, protein={protein}")

            result = parser.add_custom_food(name, cal, protein, serving)

            if should_succeed:
                if result['success']:
                    print(f"✅ Correctly accepted valid input\n")
                else:
                    print(f"❌ Should have succeeded: {result['message']}\n")
                    all_passed = False
            else:
                if not result['success']:
                    if error_text and error_text.lower() in result['message'].lower():
                        print(f"✅ Correctly rejected with appropriate error\n")
                    else:
                        print(f"✅ Correctly rejected\n")
                else:
                    print(f"❌ Should have failed\n")
                    all_passed = False

        if all_passed:
            print("✅ Validation test: PASSED\n")
        else:
            print("❌ Validation test: FAILED\n")

        return all_passed

    except Exception as e:
        print(f"❌ Test failed: {e}\n")
        return False

    finally:
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print("🧹 Cleaned up test database\n")


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("🚀 Add Custom Food Feature Tests")
    print("=" * 70)
    print()

    parse_ok = test_parse_add_command()
    add_ok = test_add_custom_food()
    validation_ok = test_validation()

    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print(f"Parse Commands: {'✅ PASS' if parse_ok else '❌ FAIL'}")
    print(f"Add to Database: {'✅ PASS' if add_ok else '❌ FAIL'}")
    print(f"Validation: {'✅ PASS' if validation_ok else '❌ FAIL'}")
    print()

    if parse_ok and add_ok and validation_ok:
        print("🎉 All tests passed!")
        print()
        print("📱 How to use in WhatsApp:")
        print("   • 'add protein shake 120 30 1 scoop'")
        print("   • 'add pizza slice, 285, 12, 1 slice (100g)'")
        print("   • 'add oats | 150 | 5 | 1 bowl'")
        print()
        print("Then track it:")
        print("   • 'I had 2 protein shake'")
        print("   • 'Had oats for breakfast'")
    else:
        print("⚠️  Some tests failed.")

    print()
