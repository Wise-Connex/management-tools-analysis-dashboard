#!/usr/bin/env python3
"""
Detailed comparison between database content and expected modal display
This will help us verify that the modal formatting matches the database content exactly
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from key_findings.key_findings_service import get_key_findings_service
from database import get_database_manager


def compare_content_vs_modal():
    """Compare database content with expected modal display format"""

    print("🔍 DETAILED CONTENT vs MODAL DISPLAY COMPARISON")
    print("=" * 70)

    db_manager = get_database_manager()
    service = get_key_findings_service(db_manager, "", "", {})

    # Test Single Source
    print("\n🎯 SINGLE SOURCE: Calidad Total + Google Trends")
    print("-" * 50)

    result = asyncio.run(
        service.generate_key_findings("Calidad Total", ["Google Trends"], "es")
    )

    if result.get("success"):
        data = result.get("data", {})

        print("📊 DATABASE CONTENT STRUCTURE:")
        print(f"  Executive Summary: {len(data.get('executive_summary', ''))} chars")
        print(f"  Principal Findings: {len(data.get('principal_findings', ''))} chars")
        print(
            f"  PCA Analysis: {len(data.get('pca_analysis', ''))} chars (should be 0 for single-source)"
        )
        print(
            f"  Heatmap Analysis: {len(data.get('heatmap_analysis', ''))} chars (should be 0 for single-source)"
        )

        # Show actual content samples
        print("\n📝 EXECUTIVE SUMMARY (Database):")
        exec_summary = data.get("executive_summary", "")
        print(f"   First 200 chars: {repr(exec_summary[:200])}")

        print("\n🔍 PRINCIPAL FINDINGS (Database):")
        principal = data.get("principal_findings", "")
        print(f"   First 500 chars: {repr(principal[:500])}")

        # Check for proper formatting indicators
        print("\n🔧 FORMATTING ANALYSIS:")
        print(f"  Executive Summary has line breaks: {'\\n' in exec_summary}")
        print(f"  Executive Summary has emojis: {'📋' in exec_summary}")
        print(f"  Principal Findings has line breaks: {'\\n' in principal}")
        print(f"  Principal Findings has section headers: {'🔍' in principal}")
        print(
            f"  Principal Findings has emojis: {'📅' in principal or '🌊' in principal}"
        )

        # Test Multi-Source
        print("\n" + "=" * 70)
        print("\n🎯 MULTI-SOURCE: Calidad Total + All 5 Sources")
        print("-" * 50)

        result_multi = asyncio.run(
            service.generate_key_findings(
                "Calidad Total",
                [
                    "Google Trends",
                    "Google Books",
                    "Bain Usability",
                    "Crossref",
                    "Bain Satisfaction",
                ],
                "es",
            )
        )

        if result_multi.get("success"):
            data_multi = result_multi.get("data", {})

            print("📊 MULTI-SOURCE CONTENT STRUCTURE:")
            print(
                f"  Executive Summary: {len(data_multi.get('executive_summary', ''))} chars"
            )
            print(
                f"  Principal Findings: {len(data_multi.get('principal_findings', ''))} chars"
            )
            print(
                f"  PCA Analysis: {len(data_multi.get('pca_analysis', ''))} chars (should be present for multi-source)"
            )
            print(
                f"  Heatmap Analysis: {len(data_multi.get('heatmap_analysis', ''))} chars (should be present for multi-source)"
            )

            print("\n📊 PCA ANALYSIS (Database):")
            pca_content = data_multi.get("pca_analysis", "")
            print(f"   First 300 chars: {repr(pca_content[:300])}")

            print("\n🔥 HEATMAP ANALYSIS (Database):")
            heatmap_content = data_multi.get("heatmap_analysis", "")
            print(f"   First 300 chars: {repr(heatmap_content[:300])}")

            print("\n🔧 MULTI-SOURCE FORMATTING ANALYSIS:")
            print(f"  PCA Analysis has line breaks: {'\\n' in pca_content}")
            print(f"  PCA Analysis has emojis: {'📊' in pca_content}")
            print(f"  Heatmap Analysis has line breaks: {'\\n' in heatmap_content}")
            print(f"  Heatmap Analysis has emojis: {'🔥' in heatmap_content}")

            print("\n✅ EXPECTED MODAL DISPLAY FORMAT:")
            print("  1. Modal Title: '🧠 Hallazgos Principales - Calidad Total'")
            print("  2. Executive Summary: Clean content with preserved line breaks")
            print(
                "  3. Principal Findings: Complete narrative with all 7 sections and proper spacing"
            )
            print(
                "  4. PCA Analysis: Separate section with proper formatting (multi-source only)"
            )
            print(
                "  5. Heatmap Analysis: Separate section with proper formatting (multi-source only)"
            )

            print("\n🔧 MODAL FORMATTING REQUIREMENTS:")
            print(
                "  - Use 'white-space: pre-line' CSS to preserve line breaks from database"
            )
            print("  - Proper section spacing with 'mb-4' margins")
            print("  - Consistent line-height of 1.6 for readability")
            print("  - Text-justify alignment for professional appearance")
            print("  - Proper emoji and header display")

        else:
            print(f"❌ Multi-source test failed: {result_multi.get('error')}")

    else:
        print(f"❌ Single source test failed: {result.get('error')}")


if __name__ == "__main__":
    compare_content_vs_modal()
