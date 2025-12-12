#!/usr/bin/env python3
"""Debug script to check actual content structure"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from key_findings.key_findings_service import get_key_findings_service
from database import get_database_manager


def debug_content_structure():
    """Check the actual content structure from database"""

    db_manager = get_database_manager()
    service = get_key_findings_service(db_manager, "", "", {})

    result = asyncio.run(
        service.generate_key_findings("Calidad Total", ["Google Trends"], "es")
    )

    if result.get("success"):
        data = result.get("data", {})

        print("=== CONTENT STRUCTURE ANALYSIS ===")
        print(f"Available keys: {list(data.keys())}")
        print()

        print("1. EXECUTIVE SUMMARY:")
        exec_summary = data.get("executive_summary", "")
        print(f"Length: {len(exec_summary)}")
        print(f"First 200 chars: {repr(exec_summary[:200])}")
        print()

        print("2. PRINCIPAL FINDINGS:")
        principal = data.get("principal_findings", "")
        print(f"Length: {len(principal)}")
        print(f"First 500 chars: {repr(principal[:500])}")
        print()

        print("3. OTHER SECTIONS:")
        for key in [
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]:
            content = data.get(key, "")
            print(
                f"{key}: {len(content)} chars - {'PRESENT' if content.strip() else 'EMPTY'}"
            )

        print()
        print("4. SINGLE-SOURCE SECTIONS:")
        pca = data.get("pca_analysis", "")
        heatmap = data.get("heatmap_analysis", "")
        print(
            f"PCA Analysis: {len(pca)} chars - {'PRESENT' if pca.strip() else 'EMPTY (CORRECT)'}"
        )
        print(
            f"Heatmap Analysis: {len(heatmap)} chars - {'PRESENT' if heatmap.strip() else 'EMPTY (CORRECT)'}"
        )

    else:
        print(f"FAILED: {result.get('error')}")


if __name__ == "__main__":
    debug_content_structure()
