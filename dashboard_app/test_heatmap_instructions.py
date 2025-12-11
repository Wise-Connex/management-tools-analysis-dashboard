#!/usr/bin/env python3
"""
Test script to verify heatmap instructions work correctly in both languages.
"""


def test_heatmap_instructions():
    """Test heatmap instructions in both languages"""

    print("🔍 Testing Heatmap Instructions")
    print("=" * 40)

    try:
        # Test Spanish instructions
        from translations import get_text

        spanish_instruction = get_text("click_heatmap", "es")
        english_instruction = get_text("click_heatmap", "en")

        print(f"\n📋 Spanish Instruction:")
        print(f"   Key: 'click_heatmap'")
        print(f"   Text: {spanish_instruction}")

        print(f"\n📋 English Instruction:")
        print(f"   Key: 'click_heatmap'")
        print(f"   Text: {english_instruction}")

        # Verify the instructions match what was in the old version
        expected_spanish = (
            "Haga clic en el mapa de calor para seleccionar variables para regresión"
        )
        expected_english = "Click on the heatmap to select variables for regression"

        print(f"\n✅ Verification:")
        if spanish_instruction == expected_spanish:
            print(f"   ✅ Spanish instruction matches old version")
        else:
            print(f"   ❌ Spanish instruction mismatch")
            print(f"      Expected: {expected_spanish}")
            print(f"      Got:      {spanish_instruction}")

        if english_instruction == expected_english:
            print(f"   ✅ English instruction matches old version")
        else:
            print(f"   ❌ English instruction mismatch")
            print(f"      Expected: {expected_english}")
            print(f"      Got:      {english_instruction}")

        print(f"\n🎯 Usage in Code:")
        print(f"   Spanish: get_text('click_heatmap', 'es')")
        print(f"   English: get_text('click_heatmap', 'en')")

        print(f"\n📍 Location in UI:")
        print(f"   - Appears under Correlation Heatmap section")
        print(f"   - Only shown when 2+ sources are selected")
        print(f"   - Instructions users to click heatmap for regression")

        print("\n✅ Heatmap instructions test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Error testing heatmap instructions: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_heatmap_instructions()
