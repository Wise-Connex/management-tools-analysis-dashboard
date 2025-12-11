#!/usr/bin/env python3
"""
Test script to verify the single-source Key Findings fix is working.
This simulates the application flow with force_refresh=True to bypass precomputed database.
"""

import sys
import os
import asyncio
from datetime import datetime

# Add the dashboard_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

from key_findings.key_findings_service import get_key_findings_service
from database import get_database_manager
from config import get_config


async def test_single_source_fix():
    """Test that single-source reports now show 7 separate sections."""

    print("🧪 Testing Single-Source Key Findings Fix")
    print("=" * 50)

    try:
        # Initialize the service with the same configuration as the app
        config = get_config()
        db_manager = get_database_manager()

        # Get the key findings service (same as used in the app)
        key_findings_service = get_key_findings_service(
            db_manager=db_manager,
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
            config=config,
        )

        print("✅ Key Findings service initialized")

        # Test with force_refresh=True to bypass precomputed database and use live AI
        print(
            "\\n🔍 Testing with force_refresh=True (bypassing precomputed database)..."
        )

        result = await key_findings_service.generate_key_findings(
            tool_name="Calidad Total",
            selected_sources=["Google Trends"],
            language="es",
            force_refresh=True,  # This forces live AI generation with our new structure
            source_display_names=["Google Trends"],
        )

        print(f"✅ Analysis completed successfully")
        print(f"📊 Success: {result.get('success', False)}")
        print(f"📊 Cache hit: {result.get('cache_hit', False)}")
        print(f"📊 Source: {result.get('source', 'unknown')}")

        if result.get("success") and result.get("data"):
            data = result["data"]
            print(f"\\n📋 Data keys: {list(data.keys())}")

            # Check if all 7 sections are present and separate
            expected_sections = [
                "executive_summary",
                "principal_findings",
                "temporal_analysis",
                "seasonal_analysis",
                "fourier_analysis",
                "strategic_synthesis",
                "conclusions",
            ]

            print("\\n🔍 Section Analysis:")
            all_sections_present = True

            for section in expected_sections:
                content = data.get(section, "")
                is_present = bool(content and len(str(content)) > 10)
                status = "✅" if is_present else "❌"
                content_length = len(str(content))

                print(f"   {status} {section}: {content_length} characters")

                if not is_present:
                    all_sections_present = False
                    print(f"   ⚠️  Section '{section}' is missing or empty!")

            # Check if sections are separate (not combined)
            principal_content = data.get("principal_findings", "")
            temporal_content = data.get("temporal_analysis", "")
            seasonal_content = data.get("seasonal_analysis", "")

            sections_separate = True
            if temporal_content and temporal_content in principal_content:
                print(
                    "❌ temporal_analysis content found in principal_findings (still combined)"
                )
                sections_separate = False

            if seasonal_content and seasonal_content in principal_content:
                print(
                    "❌ seasonal_analysis content found in principal_findings (still combined)"
                )
                sections_separate = False

            # Check PCA and heatmap are empty for single-source
            pca_empty = not data.get("pca_analysis", "")
            heatmap_empty = not data.get("heatmap_analysis", "")

            print(f"\\n📊 Results:")
            print(
                f"   All 7 sections present: {'✅' if all_sections_present else '❌'}"
            )
            print(f"   Sections are separate: {'✅' if sections_separate else '❌'}")
            print(
                f"   PCA analysis empty (single-source): {'✅' if pca_empty else '❌'}"
            )
            print(
                f"   Heatmap analysis empty (single-source): {'✅' if heatmap_empty else '❌'}"
            )
            print(
                f"   Using live AI (not cached): {'✅' if not result.get('cache_hit') else '❌'}"
            )

            if (
                all_sections_present
                and sections_separate
                and pca_empty
                and heatmap_empty
                and not result.get("cache_hit")
            ):
                print("\\n🎉 SUCCESS: Single-source Key Findings fix is working!")
                print("   • All 7 sections are present and separate")
                print("   • Sections are not combined into principal_findings")
                print(
                    "   • Multi-source sections (PCA/Heatmap) are empty for single-source"
                )
                print("   • Using live AI generation (not precomputed cache)")
                return True
            else:
                print("\\n❌ ISSUE: Fix not working as expected")
                return False
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"\\n❌ Request failed: {error_msg}")
            return False

    except Exception as e:
        print(f"\\n❌ Error during test: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_single_source_fix())
    print(f"\\n🎯 Final result: {'SUCCESS' if success else 'FAILURE'}")
    sys.exit(0 if success else 1)
