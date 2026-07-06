#!/bin/bash
# Test runner for GenSON bug fixes
# Usage:
#   ./test.sh base  → Run existing tests (should pass)
#   ./test.sh new   → Run new tests only (should fail on buggy code, pass on fixed code)

set -e  # Exit on error

MODE="${1:-base}"

case "$MODE" in
    base)
        echo "=========================================="
        echo "Running BASE tests (existing test suite)"
        echo "=========================================="
        python3 -m unittest discover -s test -p "test_*.py" -v
        echo ""
        echo "✓ All base tests passed!"
        ;;
    
    new)
        echo "=========================================="
        echo "Running NEW tests (bug-specific tests)"
        echo "=========================================="
        echo "These tests FAIL on original code"
        echo "These tests PASS on fixed code"
        echo "=========================================="
        python3 -m unittest test.test_bug_fixes -v
        echo ""
        echo "✓ All new tests passed!"
        ;;
    
    *)
        echo "Usage: $0 {base|new}"
        echo "  base - Run existing test suite"
        echo "  new  - Run new bug-specific tests"
        exit 1
        ;;
esac
