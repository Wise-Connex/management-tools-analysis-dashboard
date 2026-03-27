#!/usr/bin/env python3
"""
Verify dashboard validation works for Benchmarking + Google Trends (es)
Using the correct database schema with individual columns
"""

import os
import sys
import json

# Add database implementation path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "database_implementation"))

try:
    from precomputed_findings_db import get_precomputed_db_manager

    print("✅ Successfully imported database manager")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def validate_dashboard_content(tool_name, selected_sources, language):
    """Validate content for dashboard display - mimics dashboard logic."""

    try:
        # Initialize database manager
        db_manager = get_precomputed_db_manager()

        # Generate the hash for this combination (same as dashboard does)
        combination_hash = db_manager.generate_combination_hash(
            tool_name=tool_name, selected_sources=selected_sources, language=language
        )

        print(f"🔍 Generated hash: {combination_hash}")

        # Retrieve from database
        analysis = db_manager.get_combination_by_hash(combination_hash)

        if not analysis:
            return {
                "success": False,
                "error": f"No analysis found for {tool_name} + {selected_sources} ({language})",
            }

        print(f"✅ Found analysis: ID {analysis.get('id')}")

        # Check required sections from individual columns (not analysis_data)
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

        sections_present = []
        sections_missing = []

        for section in required_sections:
            content = analysis.get(section, "")
            if content and len(content.strip()) > 10:
                sections_present.append(section)
            else:
                sections_missing.append(section)

        print(f"\n📊 Section Analysis:")
        print(f"  ✅ Present ({len(sections_present)}): {sections_present}")
        print(f"  ❌ Missing ({len(sections_missing)}): {sections_missing}")

        # Dashboard validation logic: minimum 6 sections required
        is_valid = len(sections_present) >= 6

        result = {
            "success": is_valid,
            "sections_present": len(sections_present),
            "sections_missing": len(sections_missing),
            "required_sections": len(required_sections),
            "analysis_data": {
                section: analysis.get(section, "") for section in required_sections
            },
            "validation_message": "",
        }

        if is_valid:
            result["validation_message"] = (
                f"✅ PASS: {len(sections_present)}/7 sections present (minimum 6 required)"
            )
            print(f"\n✅ DASHBOARD VALIDATION PASSED!")
            print(f"   {len(sections_present)}/7 sections present (minimum 6 required)")
        else:
            result["validation_message"] = (
                f"❌ FAIL: Only {len(sections_present)}/7 sections present (minimum 6 required)"
            )
            print(f"\n❌ DASHBOARD VALIDATION FAILED!")
            print(
                f"   Only {len(sections_present)}/7 sections present (minimum 6 required)"
            )

        # Show content preview for each section
        print(f"\n📝 Content Preview:")
        for section in required_sections:
            content = analysis.get(section, "")
            if content:
                preview = content[:100] + "..." if len(content) > 100 else content
                print(f"  📝 {section}: {len(content)} chars - {preview}")
            else:
                print(f"  ❌ {section}: Missing")

        return result

    except Exception as e:
        return {"success": False, "error": f"Validation error: {str(e)}"}


def main():
    """Main verification function."""
    print("🧪 Verifying Dashboard Validation for Benchmarking + Google Trends (es)")
    print("=" * 75)

    # Test the specific combination that was failing
    tool_name = "Benchmarking"
    selected_sources = ["Google Trends"]
    language = "es"

    print(f"Testing: {tool_name} + {selected_sources} ({language})")

    result = validate_dashboard_content(tool_name, selected_sources, language)

    if result["success"]:
        print(f"\n🎉 SUCCESS: Dashboard validation works!")
        print(f"   {result['validation_message']}")
        print(f"\n🚀 Ready for dashboard testing!")
        print(
            f"   The Benchmarking + Google Trends (es) combination should now work in the dashboard."
        )
    else:
        print(f"\n❌ FAILED: Dashboard validation failed")
        print(f"   {result.get('validation_message', result.get('error'))}")

    # Save verification results
    output_file = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_validation_result_fixed.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Verification results saved to: {output_file}")


if __name__ == "__main__":
    main()
