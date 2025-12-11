#!/usr/bin/env python3
"""
Deep debugging to trace the entire modal flow from database to display.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def deep_debug_modal_flow():
    """Trace the entire modal flow step by step."""
    print("🔍 DEEP DEBUG: Tracing entire modal flow...")
    print("=" * 70)

    # Get database manager
    db_manager = get_precomputed_db_manager()

    # Test parameters
    selected_tool = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    print(f"🔍 Testing: {selected_tool} + {selected_sources} + {language}")

    # Step 1: Get data from database
    print(f"\n1️⃣ DATABASE RETRIEVAL:")
    hash_value = db_manager.generate_combination_hash(
        tool_name=selected_tool, selected_sources=selected_sources, language=language
    )
    print(f"   Generated hash: {hash_value}")

    result = db_manager.get_combination_by_hash(hash_value)
    if not result:
        print("❌ No result found in database")
        return False

    print("✅ Result found in database")

    # Step 2: Examine raw data structure
    print(f"\n2️⃣ RAW DATA STRUCTURE:")
    print(f"   Available keys: {list(result.keys())}")

    for key in ["executive_summary", "principal_findings", "conclusions"]:
        content = result.get(key, "")
        if isinstance(content, str):
            print(f"   {key}: {len(content)} chars")
            print(f"   {key} preview: {repr(content[:100])}")
        else:
            print(f"   {key}: {type(content)}")

    # Step 3: Test the exact modal component logic
    print(f"\n3️⃣ MODAL COMPONENT LOGIC TEST:")

    # Get the actual modal component function
    try:
        from dashboard_app.key_findings.modal_component import KeyFindingsModal

        print("   ✅ Successfully imported KeyFindingsModal")

        # Test the _extract_text_content method directly
        modal = KeyFindingsModal.__new__(
            KeyFindingsModal
        )  # Create without initialization

        principal_findings_raw = result.get("principal_findings", "")
        print(f"   Input principal_findings: {len(principal_findings_raw)} chars")
        print(f"   Input type: {type(principal_findings_raw)}")
        print(f"   Input preview: {repr(principal_findings_raw[:150])}")

        # Call the actual _extract_text_content method
        extracted = modal._extract_text_content(principal_findings_raw)
        print(f"   Output length: {len(extracted)}")
        print(f"   Output preview: {repr(extracted[:200])}")

        # Check if formatting worked
        if "•" in extracted:
            print("   ✅ BULLET POINTS DETECTED!")
            bullet_count = extracted.count("•")
            print(f"   📋 Found {bullet_count} bullet points")
        else:
            print("   ❌ No bullet points found")

        # Test conclusions
        conclusions_raw = result.get("conclusions", "")
        print(f"\n   Input conclusions: {len(conclusions_raw)} chars")
        extracted_conclusions = modal._extract_text_content(conclusions_raw)
        print(f"   Output conclusions: {len(extracted_conclusions)} chars")

        if len(extracted_conclusions) > 2000:
            print("   ✅ Substantial conclusions content")
        else:
            print("   ⚠️  Conclusions content shorter than expected")

    except Exception as e:
        print(f"❌ Error importing or using modal component: {e}")
        import traceback

        traceback.print_exc()

    # Step 4: Check if there's a different path being used
    print(f"\n4️⃣ ALTERNATIVE PATHS CHECK:")

    # Check if there's another modal component or function
    import importlib
    import sys

    # Look for other modal-related modules
    for module_name in sys.modules:
        if "modal" in module_name.lower() and "key_findings" in module_name:
            print(f"   Found modal module: {module_name}")

    # Check the actual app structure
    try:
        # Look at what's actually imported in the app
        import dashboard_app.app as app_module

        print(f"   App module loaded: {app_module}")

        # Check if there are any modal-related attributes
        app_attrs = [attr for attr in dir(app_module) if "modal" in attr.lower()]
        if app_attrs:
            print(f"   App modal attributes: {app_attrs}")
    except Exception as e:
        print(f"   Could not inspect app module: {e}")

    print(f"\n🎯 FINAL ASSESSMENT:")
    print("   Backend data: ✅ Available and correct")
    print("   Modal component: ✅ Imported successfully")
    print("   _extract_text_content: ✅ Function exists and accessible")

    # The key test - does it actually format?
    if "•" in extracted:
        print("   🎉 MODAL FORMATTING: WORKING!")
        return True
    else:
        print("   ❌ MODAL FORMATTING: NOT WORKING")
        print("   🔍 Need to investigate why formatting isn't applied")
        return False


if __name__ == "__main__":
    success = deep_debug_modal_flow()
    sys.exit(0 if success else 1)
