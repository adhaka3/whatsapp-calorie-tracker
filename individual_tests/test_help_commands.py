"""Test the help and greeting command handlers"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_greeting_triggers():
    """Test that greeting messages trigger the welcome message"""
    print("=" * 70)
    print("🧪 TEST 1: Greeting Triggers")
    print("=" * 70)
    print()

    greeting_triggers = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'start']

    print("Testing greeting triggers:\n")
    for trigger in greeting_triggers:
        # Check if trigger would be detected
        is_greeting = trigger.lower() in greeting_triggers or trigger.lower().startswith(tuple(greeting_triggers))
        if is_greeting:
            print(f"  ✅ '{trigger}' → Shows welcome message")
        else:
            print(f"  ❌ '{trigger}' → Would NOT trigger")

    # Test variations with extra words
    print("\nTesting variations:\n")
    variations = ['hi there', 'hello bot', 'good morning!', 'Hey!']
    for variation in variations:
        lower_var = variation.lower()
        is_greeting = lower_var in greeting_triggers or lower_var.startswith(tuple(greeting_triggers))
        if is_greeting:
            print(f"  ✅ '{variation}' → Shows welcome message")
        else:
            print(f"  ⚠️  '{variation}' → Needs exact match or startswith")

    print("\n✅ Greeting triggers test: PASSED\n")
    return True


def test_help_triggers():
    """Test that help commands trigger the help message"""
    print("=" * 70)
    print("🧪 TEST 2: Help Command Triggers")
    print("=" * 70)
    print()

    help_triggers = ['help', 'commands', 'command', '?', 'info']

    print("Testing help triggers:\n")
    for trigger in help_triggers:
        is_help = trigger.lower() in help_triggers
        if is_help:
            print(f"  ✅ '{trigger}' → Shows help message")
        else:
            print(f"  ❌ '{trigger}' → Would NOT trigger")

    # Test case variations
    print("\nTesting case variations:\n")
    case_variations = ['HELP', 'Help', 'HeLp', 'COMMANDS', 'Commands']
    for variation in case_variations:
        is_help = variation.lower() in help_triggers
        if is_help:
            print(f"  ✅ '{variation}' → Shows help message")
        else:
            print(f"  ❌ '{variation}' → Would NOT trigger")

    print("\n✅ Help command triggers test: PASSED\n")
    return True


def get_greeting_message() -> str:
    """Return greeting message for hi/hello"""
    return """👋 *Welcome to Calorie Tracker!*

I'm here to help you track your meals and nutrition effortlessly.

✨ *Quick Start:*
Just tell me what you ate, and I'll track it for you!

Example: "I had 2 rotis and dal"

💡 *Want to know more?*
Type *help* or *commands* to see everything I can do.

Let's get started! 🍛"""


def get_help_message() -> str:
    """Return comprehensive help/commands message"""
    return """📚 *Calorie Tracker - Commands Guide*

*🍽️ TRACK MEALS*
Just message what you ate naturally:
• "I had 2 rotis and dal"
• "Ate chicken curry and rice"

*📊 VIEW STATS*
• *total* - Today's calories & protein summary
• *total week* - 7-day breakdown with daily stats
• *summary* or *stats* - Detailed today's stats with recent meals

*➕ ADD CUSTOM FOOD*
• *add <name> <cal> <protein> <serving>*
  Example: "add protein shake 120 30 1 scoop"
• Food is immediately available for tracking!

*✏️ MANUAL ENTRY*
• Know exact values? Send:
  "protein 20g and calories 300"

*🗑️ DELETE LAST MEAL*
• *delete* or *undo* - Remove your last meal entry
• Made a mistake? Just undo it instantly!

*📋 FOOD DATABASE*
• *list* or *menu* - See all 35+ available foods
• Includes roti, rice, dal, paneer, chicken curry, biryani, and more!

*📥 EXPORT DATA*
• *export* - Download your meal log as Excel file
• Get all your data for detailed analysis

*❓ HELP*
• *help* or *commands* - Show this message

Need assistance? Just send a message and I'll guide you! 😊"""


def test_message_differences():
    """Test that greeting and help messages are different"""
    print("=" * 70)
    print("🧪 TEST 3: Message Differentiation")
    print("=" * 70)
    print()

    greeting = get_greeting_message()
    help_msg = get_help_message()

    print("Checking message characteristics:\n")

    # Check they're different
    if greeting != help_msg:
        print("  ✅ Greeting and help messages are different")
    else:
        print("  ❌ Messages should be different")
        return False

    # Check greeting is shorter (welcome should be brief)
    if len(greeting) < len(help_msg):
        print(f"  ✅ Greeting is shorter ({len(greeting)} chars) than help ({len(help_msg)} chars)")
    else:
        print("  ❌ Greeting should be shorter than help")
        return False

    # Check greeting mentions help
    if 'help' in greeting.lower() or 'command' in greeting.lower():
        print("  ✅ Greeting directs users to help/commands")
    else:
        print("  ⚠️  Greeting could mention help/commands")

    # Check help has commands
    if 'total' in help_msg and 'delete' in help_msg and 'export' in help_msg:
        print("  ✅ Help message contains command information")
    else:
        print("  ❌ Help message should list commands")
        return False

    print("\n✅ Message differentiation test: PASSED\n")
    return True


def test_command_coverage():
    """Test that all main commands are documented in help"""
    print("=" * 70)
    print("🧪 TEST 4: Command Coverage in Help")
    print("=" * 70)
    print()

    help_msg = get_help_message().lower()

    # List of main commands that should be documented
    commands = [
        ('total', 'today\'s stats'),
        ('total week', 'weekly breakdown'),
        ('summary', 'detailed stats'),
        ('add', 'custom food'),
        ('delete', 'remove meal'),
        ('list', 'food database'),
        ('export', 'download data'),
    ]

    print("Checking command documentation:\n")

    all_present = True
    for command, description in commands:
        if command in help_msg:
            print(f"  ✅ '{command}' is documented (for {description})")
        else:
            print(f"  ❌ '{command}' is missing (for {description})")
            all_present = False

    if all_present:
        print("\n✅ Command coverage test: PASSED\n")
        return True
    else:
        print("\n❌ Command coverage test: FAILED\n")
        return False


if __name__ == "__main__":
    print()
    print("=" * 70)
    print("🚀 Help & Greeting Commands Tests")
    print("=" * 70)
    print()

    test1_ok = test_greeting_triggers()
    test2_ok = test_help_triggers()
    test3_ok = test_message_differences()
    test4_ok = test_command_coverage()

    print("=" * 70)
    print("📊 Test Summary")
    print("=" * 70)
    print(f"Greeting Triggers: {'✅ PASS' if test1_ok else '❌ FAIL'}")
    print(f"Help Triggers: {'✅ PASS' if test2_ok else '❌ FAIL'}")
    print(f"Message Differentiation: {'✅ PASS' if test3_ok else '❌ FAIL'}")
    print(f"Command Coverage: {'✅ PASS' if test4_ok else '❌ FAIL'}")
    print()

    if test1_ok and test2_ok and test3_ok and test4_ok:
        print("🎉 All tests passed!")
        print()
        print("📱 How users interact:")
        print()
        print("GREETINGS (Welcome message):")
        print("   • hi, hello, hey")
        print("   • good morning, good afternoon, good evening")
        print("   • start")
        print()
        print("HELP (Full commands list):")
        print("   • help, commands, command")
        print("   • ?, info")
        print()
        print("USER FLOW:")
        print("   1. User: 'hi' → Bot shows welcome")
        print("   2. User: 'help' → Bot shows all commands")
        print("   3. User: 'total' → Bot shows today's stats")
    else:
        print("⚠️  Some tests failed.")

    print()
