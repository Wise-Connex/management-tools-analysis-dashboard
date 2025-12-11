#!/usr/bin/env python3
"""
Test script to verify the new multilingual translations work correctly.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard_app.translations import get_text


def test_new_translations():
    """Test the new heatmap and regression instruction translations"""

    print("🔍 Testing new multilingual translations...")
    print("=" * 50)

    # Test Spanish translations
    print("\n🇪🇸 SPANISH TRANSLATIONS:")
    try:
        heatmap_es = get_text("heatmap_instructions", "es")
        regression_es = get_text("regression_instructions", "es")

        print(f"✅ Heatmap instructions (ES): {heatmap_es}")
        print(f"✅ Regression instructions (ES): {regression_es}")

        # Test English translations
        print("\n🇺🇸 ENGLISH TRANSLATIONS:")
        heatmap_en = get_text("heatmap_instructions", "en")
        regression_en = get_text("regression_instructions", "en")

        print(f"✅ Heatmap instructions (EN): {heatmap_en}")
        print(f"✅ Regression instructions (EN): {regression_en}")

        # Verify translations are different (not the same)
        if heatmap_es != heatmap_en and regression_es != regression_en:
            print("\n✅ Translations are properly bilingual")
        else:
            print("\n❌ Translations may not be properly separated")

    except Exception as e:
        print(f"❌ Translation error: {e}")

    print("\n🎯 TRANSLATION TEST COMPLETE")


if __name__ == "__main__":
    test_new_translations()
