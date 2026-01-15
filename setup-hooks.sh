#!/bin/bash

# Setup script for Git hooks
# Run this once to install pre-commit hooks

echo "🔧 Setting up Git hooks..."

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

echo ""
echo "🔍 Running pre-commit checks..."
echo ""

# Check for .env file
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "❌ ERROR: Attempting to commit .env file!"
    echo "   Remove from staging: git reset HEAD .env"
    echo ""
    exit 1
fi

# Check for database files
if git diff --cached --name-only | grep -q "\.db$"; then
    echo "⚠️  WARNING: Attempting to commit .db file!"
    echo "   Database files should not be committed."
    read -p "   Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Commit aborted"
        exit 1
    fi
fi

# Check for secrets in staged code
echo "🔒 Checking for secrets..."

# Get list of changed files (excluding workflow files and documentation)
changed_files=$(git diff --cached --name-only | grep -v "\.github/workflows" | grep -v "\.md$" | grep -v "setup-hooks.sh")

if [ -n "$changed_files" ]; then
    # Only check non-workflow files for secrets
    if echo "$changed_files" | xargs git diff --cached | grep -E "(sk-[a-zA-Z0-9]{48}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36}|glpat-[a-zA-Z0-9_-]{20,})"; then
        echo "⚠️  WARNING: Possible secrets detected in staged changes!"
        echo ""
        echo "$changed_files" | xargs git diff --cached | grep -E "(sk-|AKIA|ghp_|glpat-)" --color=always
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Commit aborted"
            exit 1
        fi
    fi
fi

# Run tests (optional - can be slow)
# Uncomment to enable automatic test running before each commit
# echo "🧪 Running tests..."
# if ! python test_v2_features.py > /dev/null 2>&1; then
#     echo "❌ V2 tests failed! Run: python test_v2_features.py"
#     exit 1
# fi
# if ! python test_all.py > /dev/null 2>&1; then
#     echo "❌ V1 tests failed! Run: python test_all.py"
#     exit 1
# fi

echo "✅ Pre-commit checks passed!"
echo ""
exit 0
EOF

# Make hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed!"
echo ""
echo "The hook will:"
echo "  • Prevent committing .env files"
echo "  • Warn about database files"
echo "  • Check for secrets in code"
echo "  • (Optional) Run tests before commit"
echo ""
echo "To enable automatic test running, edit:"
echo "  .git/hooks/pre-commit"
echo ""
echo "To bypass hook temporarily (not recommended):"
echo "  git commit --no-verify"
echo ""
