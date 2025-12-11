#!/usr/bin/env python3
"""
Test script to verify single-source modal display formatting fixes.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_single_source_content():
    """Test that single-source content has all sections properly stored."""
    print("🧪 Testing single-source content structure...")

    # Get database manager
    db_manager = get_precomputed_db_manager()

    # Generate hash for Calidad Total + Google Trends + Spanish
    hash_value = db_manager.generate_combination_hash(
        tool_name="Calidad Total", selected_sources=["Google Trends"], language="es"
    )
    print(f"🔍 Generated hash: {hash_value}")

    # Retrieve the analysis
    result = db_manager.get_combination_by_hash(hash_value)

    if not result:
        print("❌ No result found in database")
        return False

    print(f"✅ Result found in database")
    print(f"📊 Available sections:")

    sections = [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "strategic_synthesis",
        "conclusions",
        "pca_analysis",
        "heatmap_analysis",
    ]

    all_good = True
    for section in sections:
        content = result.get(section, "")
        if isinstance(content, str):
            length = len(content)
            status = "✅" if length > 0 else "❌"
            print(f"   {status} {section}: {length} chars")
            if section in [
                "executive_summary",
                "principal_findings",
                "temporal_analysis",
                "seasonal_analysis",
                "fourier_analysis",
                "strategic_synthesis",
                "conclusions",
            ]:
                if length == 0:
                    all_good = False
        elif isinstance(content, list):
            length = len(content)
            status = "✅" if length > 0 else "❌"
            print(f"   {status} {section}: {length} items")
        else:
            print(f"   ✅ {section}: {type(content)}")

    # Check confidence score
    confidence = result.get("confidence_score", 0)
    print(f"🎯 Confidence score: {confidence}")

    # Check model used
    model = result.get("model_used", "unknown")
    print(f"🤖 Model used: {model}")

    if all_good and confidence > 0.8:
        print("🎉 All critical sections have content and high confidence!")
        return True
    else:
        print("⚠️  Some issues detected")
        return False


if __name__ == "__main__":
    success = test_single_source_content()
    sys.exit(0 if success else 1)
