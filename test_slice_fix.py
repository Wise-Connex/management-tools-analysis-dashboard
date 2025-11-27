#!/usr/bin/env python3
"""
Test the slice fix for single-source analysis.
"""

# Test the problematic slicing behavior
print("🧪 Testing slice fix...")

# Test cases that could cause the slice(None, 50, None) error
test_values = [
    None,
    "",
    "Some string content",
    [],
    {},
    123,
    ["item1", "item2"],
    {"key": "value"}
]

for i, value in enumerate(test_values):
    try:
        # This is what was causing the error
        result = value[:50]
        print(f"✅ Test {i+1}: {type(value).__name__} - slice successful: {str(result)[:30]}...")
    except Exception as e:
        print(f"❌ Test {i+1}: {type(value).__name__} - slice failed: {e}")

# Test the fix
print("\n🧪 Testing the fix...")
for i, value in enumerate(test_values):
    try:
        # This is the fix
        str_value = str(value) if value else ""
        result = str_value[:50]
        print(f"✅ Fix {i+1}: {type(value).__name__} - converted and sliced: {str(result)[:30]}...")
    except Exception as e:
        print(f"❌ Fix {i+1}: {type(value).__name__} - fix failed: {e}")

print("\n🎯 Slice fix verification complete!")