#!/usr/bin/env python3
"""
Final test for the slice fix in single-source analysis.
"""

import asyncio
import sys
import os

# Set up environment
os.environ['DASHBOARD_DB_PATH'] = 'data/database.db'
os.environ['DASHBOARD_KEY_FINDINGS_DB_PATH'] = 'data/key_findings.db'
os.environ['DASHBOARD_PRECOMPUTED_FINDINGS_DB_PATH'] = '../data/precomputed_findings.db'

sys.path.insert(0, '..')
from key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager

async def test_slice_fix_final():
    """Test that the slice fix works in the actual single-source analysis."""
    print("🧪 TESTING SLICE FIX FINAL")
    print("=" * 50)

    service = KeyFindingsService(get_database_manager())

    try:
        # Test single-source analysis
        result = await service.generate_key_findings(
            tool_name="Benchmarking",
            selected_sources=["Google Trends"],
            language="es"
        )

        if result.get("success"):
            print("✅ Single-source analysis completed without slice error!")

            content = result.get("data", {})

            # Verify mathematical correctness
            heatmap_empty = not content.get('heatmap_analysis') or len(str(content.get('heatmap_analysis', '')).strip()) == 0
            pca_empty = not content.get('pca_analysis') or len(str(content.get('pca_analysis', '')).strip()) == 0

            if heatmap_empty and pca_empty:
                print("✅ Mathematical correctness verified: Heatmap and PCA correctly excluded")
            else:
                print(f"❌ Mathematical error: Heatmap empty={heatmap_empty}, PCA empty={pca_empty}")
                return False

            # Verify content structure
            principal_findings = content.get('principal_findings', '')
            if principal_findings and len(principal_findings) > 0:
                print(f"✅ Principal findings generated: {len(principal_findings)} characters")
            else:
                print("❌ No principal findings content generated")
                return False

            print(f"\n🎯 SLICE FIX FINAL: PASSED")
            return True

        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"❌ Analysis failed: {error_msg}")
            return False

    except TypeError as e:
        if "slice" in str(e):
            print(f"❌ SLICE FIX FAILED: {e}")
            return False
        else:
            raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_slice_fix_final())
    if success:
        print("\n🎉 SLICE FIX FINAL VERIFIED SUCCESSFULLY!")
        print("✅ The slice(None, 50, None) error has been resolved")
    else:
        print("\n❌ SLICE FIX FINAL FAILED!")
        sys.exit(1)