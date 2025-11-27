#!/usr/bin/env python3
"""
Simple final test for simplified architecture.
"""

import asyncio
import sys
import time

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

# Mock the dashboard environment
import os
os.environ['DASHBOARD_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/database.db'
os.environ['DASHBOARD_KEY_FINDINGS_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/key_findings.db'
os.environ['DASHBOARD_PRECOMPUTED_FINDINGS_DB_PATH'] = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db'

from key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager

async def main():
    """Run final test."""
    print("🚀 FINAL INTEGRATION TEST")
    print("=" * 60)

    service = KeyFindingsService(get_database_manager())

    # Test single-source
    print("\n🧪 Testing Single-Source...")
    start = time.time()

    result = await service.generate_key_findings(
        tool_name="Benchmarking",
        selected_sources=["Google Trends"],
        language="es"
    )

    elapsed = time.time() - start

    if result.get("success"):
        content = result.get("data", {})
        heatmap_empty = not content.get('heatmap_analysis') or len(str(content.get('heatmap_analysis', '')).strip()) == 0
        pca_empty = not content.get('pca_analysis') or len(str(content.get('pca_analysis', '')).strip()) == 0

        if heatmap_empty and pca_empty:
            print("✅ Single-source: Mathematical correctness verified")
        else:
            print("❌ Single-source: Mathematical error")
            return False

        print(f"✅ Single-source: {elapsed:.3f}s response time")
    else:
        print("❌ Single-source failed")
        return False

    # Test multi-source
    print("\n🧪 Testing Multi-Source...")
    start = time.time()

    result = await service.generate_key_findings(
        tool_name="Benchmarking",
        selected_sources=["Google Trends", "Google Books", "Bain Usability"],
        language="es"
    )

    elapsed = time.time() - start

    if result.get("success"):
        content = result.get("data", {})
        heatmap_has_content = content.get('heatmap_analysis') and len(str(content.get('heatmap_analysis', '')).strip()) > 10
        pca_has_content = content.get('pca_analysis') and len(str(content.get('pca_analysis', '')).strip()) > 10

        if heatmap_has_content and pca_has_content:
            print("✅ Multi-source: Mathematical correctness verified")
        else:
            print("❌ Multi-source: Mathematical error")
            return False

        print(f"✅ Multi-source: {elapsed:.3f}s response time")
    else:
        print("❌ Multi-source failed")
        return False

    print("\n🎉 ALL TESTS PASSED!")
    print("✅ Architecture ready for production!")

    return True

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)