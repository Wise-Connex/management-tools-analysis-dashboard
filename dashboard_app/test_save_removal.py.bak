#!/usr/bin/env python3
"""Test script to verify save button removal"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layout import create_key_findings_modal


def test_save_button_removal():
    """Test if save button is completely removed from modal"""

    modal = create_key_findings_modal()
    modal_html = str(modal)

    print("🔍 Testing Save Button Removal")
    print("=" * 40)

    # Check for save button text
    if "Guardar" in modal_html:
        print("❌ Save button still found in modal!")
        # Find where it's located
        lines = modal_html.split("\n")
        for i, line in enumerate(lines):
            if "Guardar" in line:
                print(f"Found at line {i}: {line.strip()}")
        return False
    else:
        print("✅ Save button text successfully removed from modal!")

    # Check for save button ID
    if "save-key-findings" in modal_html:
        print("❌ Save button ID still found!")
        return False
    else:
        print("✅ Save button ID successfully removed!")

    # Check for any save-related functionality
    save_related = ["guardar", "save", "Guardar", "Save"]
    found_any = False
    for term in save_related:
        if term in modal_html.lower():
            print(f"⚠️  Found save-related term: '{term}'")
            found_any = True

    if not found_any:
        print("✅ No save-related functionality found!")

    print("\n🎉 Save button removal verification complete!")
    return True


if __name__ == "__main__":
    success = test_save_button_removal()
    sys.exit(0 if success else 1)
