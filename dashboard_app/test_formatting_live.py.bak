#!/usr/bin/env python3
"""
Test script to verify key findings formatting fixes by triggering live AI generation.
"""

import sys
import os
import json
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Add dashboard_app to path
sys.path.insert(0, str(Path(__file__).parent))

from key_findings.key_findings_service import KeyFindingsService
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_live_key_findings():
    """Test key findings generation with updated formatting."""

    print("🚀 Testing Key Findings with Updated Formatting")
    print("=" * 60)

    # Initialize services
    db_manager = get_precomputed_db_manager()
    kf_service = KeyFindingsService(db_manager=db_manager)

    # Test parameters
    tool_name = "Calidad Total"
    selected_sources = [4]  # Crossref
    language = "es"

    print(f"Tool: {tool_name}")
    print(f"Sources: {selected_sources}")
    print(f"Language: {language}")
    print()

    try:
        # Generate key findings (this will use live AI since cache is cleared)
        print("🔄 Generating key findings with live AI...")
        result = kf_service.generate_key_findings(
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            force_refresh=True,  # Force fresh generation
        )

        if result and result.get("success"):
            content = result.get("content", {})
            print("✅ Key findings generated successfully!")
            print()

            # Check principal_findings formatting
            principal_findings = content.get("principal_findings", "")
            if principal_findings:
                print("📝 PRINCIPAL FINDINGS FORMATTING:")
                print("=" * 40)
                print(
                    principal_findings[:800] + "..."
                    if len(principal_findings) > 800
                    else principal_findings
                )
                print()

                # Verify formatting
                if "•" in principal_findings and "\n  " in principal_findings:
                    print("✅ SUCCESS: Bullet points are properly formatted!")
                    bullet_count = principal_findings.count("•")
                    reasoning_count = principal_findings.count("\n  ")
                    print(
                        f"   Found {bullet_count} bullet points with {reasoning_count} reasoning sections"
                    )
                else:
                    print("❌ ISSUE: Bullet points not formatted correctly")
                    print("Raw content preview:", repr(principal_findings[:200]))
            else:
                print("❌ No principal_findings content found")

            # Check other sections
            sections = [
                "executive_summary",
                "temporal_analysis",
                "seasonal_analysis",
                "fourier_analysis",
                "strategic_synthesis",
                "conclusions",
            ]

            print("\n📊 SECTION COMPLETENESS:")
            print("=" * 40)
            for section in sections:
                content = content.get(section, "")
                if content and len(content.strip()) > 50:
                    print(f"✅ {section}: {len(content)} chars")
                else:
                    print(
                        f"⚠️  {section}: Missing or short ({len(content) if content else 0} chars)"
                    )

            return True

        else:
            print("❌ Key findings generation failed")
            if result:
                print("Error:", result.get("error", "Unknown error"))
            return False

    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_live_key_findings()

    if success:
        print("\n🎉 All tests passed! The formatting fixes are working correctly.")
    else:
        print("\n⚠️  Tests failed. Check the errors above.")

    sys.exit(0 if success else 1)
