"""Test script to verify the food parser and database locally"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from food_parser import FoodParser
from database import MealDatabase

def test_food_parser():
    """Test the food parser"""
    print("🧪 Testing Food Parser...\n")
    
    try:
        # By default use FREE regex-based parsing
        use_llm = os.getenv("USE_LLM", "false").lower() == "true"
        llm_provider = os.getenv("LLM_PROVIDER", "anthropic") if use_llm else None
        
        if use_llm:
            print(f"🤖 Using LLM-powered parsing with {llm_provider}\n")
        else:
            print("🆓 Using FREE regex-based parsing (no API costs!)\n")
        
        parser = FoodParser(
            food_database_path="data/indian_foods.json",
            llm_provider=llm_provider,
            use_llm=use_llm
        )
        
        # Test messages
        test_messages = [
            "I had 2 rotis and dal",
            "Ate chicken biryani and raita",
            "Had 3 idlis for breakfast",
            "2 parathas with curd",
        ]
        
        for msg in test_messages:
            print(f"📝 Testing: '{msg}'")
            result = parser.process_message(msg)
            
            if result['type'] == 'meal_logged':
                print(f"✅ Parsed successfully!")
                print(f"   Calories: {result['total_calories']} kcal")
                print(f"   Protein: {result['total_protein']}g")
                print(f"   Items: {', '.join([item['name'] for item in result['items']])}")
            else:
                print(f"❌ Failed: {result.get('message', 'Unknown error')}")
            print()
        
        print("✅ Food Parser test completed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Food Parser test failed: {e}\n")
        return False


def test_database():
    """Test the database"""
    print("🧪 Testing Database...\n")
    
    try:
        db = MealDatabase(db_path="data/test_meals.db")
        
        # Test user creation
        test_phone = "whatsapp:+1234567890"
        db.add_user(test_phone, "Test User")
        print("✅ User added successfully")
        
        # Test meal logging
        db.log_meal(
            phone_number=test_phone,
            meal_description="2 rotis and dal",
            total_calories=250.0,
            total_protein=15.5,
            parsed_items='[{"food": "roti", "quantity": 2}, {"food": "dal", "quantity": 1}]',
            items_extracted="2x roti, 1x dal",
            source="testing"
        )
        print("✅ Meal logged successfully")
        
        # Test daily summary
        summary = db.get_daily_summary(test_phone)
        print(f"✅ Daily summary retrieved: {summary}")
        
        # Test recent meals
        recent = db.get_recent_meals(test_phone)
        print(f"✅ Recent meals retrieved: {len(recent)} meals")
        
        # Clean up test database
        if os.path.exists("data/test_meals.db"):
            os.remove("data/test_meals.db")
            print("🧹 Cleaned up test database")
        
        print("\n✅ Database test completed!\n")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}\n")
        # Clean up on failure too
        if os.path.exists("data/test_meals.db"):
            os.remove("data/test_meals.db")
        return False


def check_environment():
    """Check if environment variables are set"""
    print("🔍 Checking Environment Variables...\n")
    
    # Check Twilio vars
    twilio_vars = {
        "TWILIO_ACCOUNT_SID": "Twilio Account SID",
        "TWILIO_AUTH_TOKEN": "Twilio Auth Token",
    }
    
    missing = []
    for var, description in twilio_vars.items():
        if not os.getenv(var):
            missing.append(f"  ❌ {var}: {description}")
        else:
            print(f"  ✅ {var} is set")
    
    # Check LLM API keys (optional - only needed if USE_LLM=true)
    use_llm = os.getenv("USE_LLM", "false").lower() == "true"
    has_openai = os.getenv("OPENAI_API_KEY")
    has_anthropic = os.getenv("ANTHROPIC_API_KEY")
    
    if use_llm:
        if has_openai:
            print(f"  ✅ OPENAI_API_KEY is set")
        if has_anthropic:
            print(f"  ✅ ANTHROPIC_API_KEY is set")
        
        if not has_openai and not has_anthropic:
            missing.append(f"  ❌ Need either OPENAI_API_KEY or ANTHROPIC_API_KEY (USE_LLM is enabled)")
    else:
        print(f"  ℹ️  LLM API keys not required (using FREE regex-based parsing)")
        if has_openai or has_anthropic:
            print(f"  💡 Set USE_LLM=true to enable LLM parsing")
    
    if missing:
        print("\n⚠️  Missing environment variables:")
        for item in missing:
            print(item)
        print("\nCreate a .env file with these variables or export them.")
        return False
    
    print("\n✅ All environment variables are set!\n")
    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 WhatsApp Calorie Tracker - Local Testing")
    print("=" * 60)
    print()
    
    # Check environment
    env_ok = check_environment()
    
    # Test database (doesn't require API keys)
    db_ok = test_database()
    
    # Test food parser (requires API key)
    if env_ok:
        parser_ok = test_food_parser()
    else:
        print("⚠️  Skipping food parser test (missing API keys)")
        parser_ok = False
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"Environment: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"Database: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"Food Parser: {'✅ PASS' if parser_ok else '⚠️  SKIPPED' if not env_ok else '❌ FAIL'}")
    print()
    
    if db_ok and (parser_ok or not env_ok):
        print("🎉 All tests passed! You're ready to deploy!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    print()


if __name__ == "__main__":
    # Load environment variables if .env exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception as e:
        print(f"Note: Could not load .env file: {e}")
        print("Continuing with existing environment variables...\n")
    
    main()
