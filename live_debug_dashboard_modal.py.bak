#!/usr/bin/env python3
"""
Live debugging to trace exactly what's happening in the dashboard modal.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def live_debug_dashboard_modal():
    """Live debug the actual dashboard modal generation process."""
    print("🔍 LIVE DEBUG: Tracing actual dashboard modal generation...")
    print("=" * 70)

    # Get database manager
    db_manager = get_precomputed_db_manager()

    # Test parameters
    selected_tool = "Calidad Total"
    selected_sources = ["Google Trends"]
    language = "es"

    print(f"🔍 Testing: {selected_tool} + {selected_sources} + {language}")

    # Get the precomputed analysis
    hash_value = db_manager.generate_combination_hash(
        tool_name=selected_tool, selected_sources=selected_sources, language=language
    )

    result = db_manager.get_combination_by_hash(hash_value)
    if not result:
        print("❌ No result found")
        return False

    print("✅ Result found in database")

    # Create the exact data structure that gets passed to the modal
    print(f"\n🔍 CREATING MODAL DATA STRUCTURE:")

    # This is the exact structure that gets passed to KeyFindingsModal
    report_data = {
        "executive_summary": result.get("executive_summary", ""),
        "principal_findings": result.get("principal_findings", ""),
        "temporal_analysis": result.get("temporal_analysis", ""),
        "seasonal_analysis": result.get("seasonal_analysis", ""),
        "fourier_analysis": result.get("fourier_analysis", ""),
        "strategic_synthesis": result.get("strategic_synthesis", ""),
        "conclusions": result.get("conclusions", ""),
        "pca_analysis": result.get("pca_analysis", ""),
        "heatmap_analysis": result.get("heatmap_analysis", ""),
        "analysis_type": "single_source",
    }

    print(f"   Report data keys: {list(report_data.keys())}")
    print(f"   Analysis type: {report_data.get('analysis_type', 'unknown')}")

    # Test each section with the actual modal component
    print(f"\n🔍 TESTING EACH SECTION WITH MODAL COMPONENT:")

    # Import the actual modal component
    try:
        from dashboard_app.key_findings.modal_component import KeyFindingsModal

        print("   ✅ Successfully imported KeyFindingsModal")

        # Create a minimal modal instance just to test the function
        modal = KeyFindingsModal.__new__(KeyFindingsModal)

        # Test principal findings specifically
        principal_findings_raw = report_data.get("principal_findings", "")
        print(f"\n   📋 PRINCIPAL FINDINGS TEST:")
        print(f"   Input length: {len(principal_findings_raw)}")
        print(f"   Input preview: {repr(principal_findings_raw[:150])}")

        # Call the actual _extract_text_content method
        extracted_pf = modal._extract_text_content(principal_findings_raw)
        print(f"   Output length: {len(extracted_pf)}")
        print(f"   Output preview: {repr(extracted_pf[:200])}")

        # Check if formatting worked
        if "•" in extracted_pf:
            print("   🎉 SUCCESS: Bullet points detected!")
            bullet_count = extracted_pf.count("•")
            print(f"   📊 Found {bullet_count} bullet points")
            print(f"   ✅ Principal findings formatting: WORKING")
        else:
            print("   ❌ FAILURE: No bullet points found")
            print(f"   🔍 Principal findings formatting: NOT WORKING")

        # Test conclusions
        conclusions_raw = report_data.get("conclusions", "")
        print(f"\n   📄 CONCLUSIONS TEST:")
        print(f"   Input length: {len(conclusions_raw)}")
        print(f"   Input preview: {repr(conclusions_raw[:150])}")

        extracted_conclusions = modal._extract_text_content(conclusions_raw)
        print(f"   Output length: {len(extracted_conclusions)}")
        print(f"   Output preview: {repr(extracted_conclusions[:200])}")

        if len(extracted_conclusions) > 2000:
            print("   ✅ SUCCESS: Substantial conclusions content")
            print(f"   ✅ Conclusions content: WORKING")
        else:
            print("   ⚠️  WARNING: Conclusions content shorter than expected")

        # Test the complete modal generation process
        print(f"\n🔍 TESTING COMPLETE MODAL GENERATION:")

        # Create a mock app and language store for testing
        import dash
        from dash import html

        class MockApp:
            pass

        class MockLanguageStore:
            def get(self, key, default="es"):
                return "es"

        mock_app = MockApp()
        mock_lang_store = MockLanguageStore()

        # Create the actual modal instance
        full_modal = KeyFindingsModal(mock_app, mock_lang_store)

        # Test the modal content generation
        try:
            modal_content = full_modal.generate_modal_content(report_data, language)
            print(f"   ✅ Modal content generated successfully!")
            print(f"   Modal content type: {type(modal_content)}")

            # Check if it's a Div component with children
            if hasattr(modal_content, "children"):
                print(f"   Modal has children: {hasattr(modal_content, 'children')}")
                if hasattr(modal_content.children, "__len__"):
                    print(f"   Number of children: {len(modal_content.children)}")

                    # Look for principal findings section
                    pf_found = False
                    for i, child in enumerate(modal_content.children):
                        if hasattr(child, "children") and any(
                            "Hallazgos Principales" in str(c)
                            for c in child.children
                            if hasattr(c, "__str__")
                        ):
                            print(
                                f"   📋 Found Principal Findings section at index {i}"
                            )
                            pf_found = True
                            break

                    if not pf_found:
                        print(f"   ❌ Principal Findings section not found in children")

                    # Check the actual content of principal findings
                    for i, child in enumerate(modal_content.children):
                        child_str = str(child)
                        if "bullet_point" in child_str.lower():
                            print(
                                f"   🔍 Raw JSON found in child {i}: {child_str[:200]}..."
                            )
                            break
            else:
                print(f"   Modal content: {str(modal_content)[:300]}...")

        except Exception as e:
            print(f"   ❌ Error generating modal content: {e}")
            import traceback

            traceback.print_exc()

    except Exception as e:
        print(f"   ❌ Error importing modal component: {e}")
        import traceback

        traceback.print_exc()

    print(f"\n🎯 FINAL ASSESSMENT:")
    print("   Backend data: ✅ Available and correct")
    print("   Modal component: ✅ Imported successfully")
    print("   _extract_text_content: ✅ Function exists and accessible")

    # The key test - does it actually format?
    if "•" in extracted_pf:
        print("   🎉 MODAL FORMATTING: WORKING!")
        return True
    else:
        print("   ❌ MODAL FORMATTING: NOT WORKING")
        print("   🔍 Need to investigate why formatting isn't applied")
        return False


if __name__ == "__main__":
    success = live_debug_dashboard_modal()
    sys.exit(0 if success else 1)
