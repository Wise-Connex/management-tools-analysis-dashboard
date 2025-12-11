#!/usr/bin/env python3
"""
Test script to verify Calidad Total + All 5 Sources modal content loads correctly
Simulates the dashboard interaction to test the modal content.
"""

import os
import sys
import json
import time

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Add path for database implementation
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def test_modal_content_loading():
    """Test that modal content loads correctly for Calidad Total + All 5 Sources."""

    print("🧪 Testing Modal Content Loading for Calidad Total + All 5 Sources")
    print("=" * 70)

    # Test configuration
    tool_name = "Calidad Total"
    selected_sources = [
        "Google Trends",
        "Bain Usability",
        "Kimi K-Test",
        "Survey Data",
        "Academic Research",
    ]
    language = "es"

    print(f"Tool: {tool_name}")
    print(f"Sources: {', '.join(selected_sources)}")
    print(f"Language: {language}")
    print()

    # Get database manager
    try:
        precomputed_db = get_precomputed_db_manager()
        print("✅ Database manager initialized successfully")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

    # Generate combination hash
    try:
        combination_hash = precomputed_db.generate_combination_hash(
            tool_name=tool_name, selected_sources=selected_sources, language=language
        )
        print(f"✅ Combination hash generated: {combination_hash}")
    except Exception as e:
        print(f"❌ Hash generation failed: {e}")
        return False

    # Retrieve the cached analysis
    try:
        cached_result = precomputed_db.get_combination_by_hash(combination_hash)
        if not cached_result:
            print("❌ No cached analysis found")
            return False

        print("✅ Retrieved cached analysis from database")
        print(f"   - Confidence Score: {cached_result.get('confidence_score', 'N/A')}")
        print(f"   - Model Used: {cached_result.get('model_used', 'N/A')}")
        print(f"   - Data Points: {cached_result.get('data_points_analyzed', 'N/A')}")
        print()

    except Exception as e:
        print(f"❌ Database retrieval failed: {e}")
        return False

    # Simulate modal content structure (similar to what the dashboard would create)
    print("📋 Simulating Modal Content Structure:")
    print("=" * 40)

    # Expected sections for a complete modal
    expected_sections = [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "pca_analysis",
        "heatmap_analysis",
    ]

    modal_content = {}
    missing_sections = []

    for section in expected_sections:
        if section in cached_result and cached_result[section]:
            content = cached_result[section]
            modal_content[section] = content
            print(
                f"✅ {section.replace('_', ' ').title()}: {len(str(content))} characters"
            )
        else:
            missing_sections.append(section)
            print(f"❌ {section.replace('_', ' ').title()}: Missing")

    print()

    # Check content quality
    if missing_sections:
        print(f"⚠️  Missing sections: {', '.join(missing_sections)}")
        if len(missing_sections) > 2:
            print("❌ Too many missing sections for complete modal")
            return False

    # Verify content quality indicators
    total_content_length = sum(len(str(content)) for content in modal_content.values())
    print(f"📊 Content Quality Analysis:")
    print(f"   - Total content length: {total_content_length:,} characters")
    print(f"   - Sections present: {len(modal_content)}/{len(expected_sections)}")
    print(
        f"   - Average section length: {total_content_length // len(modal_content) if modal_content else 0:,} characters"
    )

    # Check for premium content indicators
    premium_indicators = 0
    for section, content in modal_content.items():
        content_str = str(content)
        if any(
            indicator in content_str
            for indicator in ["🔍", "📊", "🔬", "🗓️", "🔥", "🎯", "💎"]
        ):
            premium_indicators += 1

    print(f"   - Premium content indicators: {premium_indicators}/{len(modal_content)}")

    # Validate confidence score
    confidence_score = cached_result.get("confidence_score", 0)
    if confidence_score >= 0.9:
        print(f"   ✅ High confidence score: {confidence_score}")
    elif confidence_score >= 0.7:
        print(f"   ⚠️  Medium confidence score: {confidence_score}")
    else:
        print(f"   ❌ Low confidence score: {confidence_score}")

    print()

    # Sample content preview
    print("📝 Content Preview (Executive Summary):")
    if "executive_summary" in modal_content:
        summary = modal_content["executive_summary"]
        # Show first few lines
        lines = str(summary).split("\n")
        for i, line in enumerate(lines[:5]):
            if line.strip():
                print(f"   {line}")
        if len(lines) > 5:
            print(f"   ... ({len(lines) - 5} more lines)")

    print()

    # Final assessment
    if (
        len(modal_content) >= 5
        and total_content_length > 5000
        and confidence_score >= 0.8
    ):
        print("🎉 MODAL CONTENT VALIDATION SUCCESSFUL!")
        print("✅ Complete multi-source analysis available")
        print("✅ High-quality premium content structure")
        print("✅ Ready for dashboard integration")
        return True
    else:
        print("❌ MODAL CONTENT VALIDATION FAILED")
        print("⚠️  Content may be incomplete or low quality")
        return False


if __name__ == "__main__":
    success = test_modal_content_loading()
    if success:
        print("\n🚀 Ready to test in dashboard! Navigate to:")
        print("   http://localhost:8050")
        print("   Select: Calidad Total + All 5 Sources")
        print("   Click: Key Findings button")
        sys.exit(0)
    else:
        print("\n❌ Content validation failed. Check database.")
        sys.exit(1)
