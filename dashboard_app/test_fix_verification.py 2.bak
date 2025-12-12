#!/usr/bin/env python3
"""
Simple test to verify the variable ordering fix in single-source analysis.
"""

import asyncio
import sys
import os

# Set up environment
os.environ['DASHBOARD_DB_PATH'] = 'data/database.db'
os.environ['DASHBOARD_KEY_FINDINGS_DB_PATH'] = 'data/key_findings.db'
os.environ['DASHBOARD_PRECOMPUTED_FINDINGS_DB_PATH'] = '../data/precomputed_findings.db'

import sys
sys.path.insert(0, '..')
from key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager

async def test_variable_ordering_fix():
    """Test that the variable ordering fix works correctly."""
    print("🧪 TESTING VARIABLE ORDERING FIX")
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
            print("✅ Single-source analysis completed without variable reference error!")

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

            # Verify essential sections
            essential_sections = ['executive_summary', 'principal_findings', 'strategic_synthesis', 'conclusions']
            missing_sections = [section for section in essential_sections if not content.get(section)]

            if not missing_sections:
                print("✅ All essential sections present")
            else:
                print(f"⚠️ Missing sections: {missing_sections}")

            print(f"\n🎯 VARIABLE ORDERING FIX: PASSED")
            return True

        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"❌ Analysis failed: {error_msg}")
            return False

    except UnboundLocalError as e:
        if "principal_findings_narrative" in str(e):
            print(f"❌ VARIABLE ORDERING FIX FAILED: {e}")
            return False
        else:
            raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_variable_ordering_fix())
    if success:
        print("\n🎉 VARIABLE ORDERING FIX VERIFIED SUCCESSFULLY!")
        print("✅ The principal_findings_narrative variable is now properly defined before use")
    else:
        print("\n❌ VARIABLE ORDERING FIX FAILED!")
        sys.exit(1)