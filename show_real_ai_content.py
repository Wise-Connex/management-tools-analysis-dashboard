#!/usr/bin/env python3
"""
Show the REAL AI content that was just stored in the database
"""

import os
import sys
import json

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def show_real_ai_content():
    """Display the real AI content that was just stored."""

    print("🔍 SHOWING REAL AI CONTENT FROM DATABASE")
    print("=" * 50)

    # Configuration
    tool_name = "Calidad Total"
    selected_sources = [
        "Google Trends",
        "Bain Usability",
        "Kimi K-Test",
        "Survey Data",
        "Academic Research",
    ]
    language = "es"

    # Get database manager
    try:
        precomputed_db = get_precomputed_db_manager()
        print("✅ Database manager initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

    # Generate combination hash
    try:
        combination_hash = precomputed_db.generate_combination_hash(
            tool_name=tool_name, selected_sources=selected_sources, language=language
        )
        print(f"✅ Combination hash: {combination_hash}")
    except Exception as e:
        print(f"❌ Hash generation failed: {e}")
        return False

    # Retrieve the real AI content
    try:
        cached_result = precomputed_db.get_combination_by_hash(combination_hash)
        if not cached_result:
            print("❌ No cached analysis found")
            return False

        print("✅ Retrieved real AI content from database")
        print(f"   - Confidence Score: {cached_result.get('confidence_score', 'N/A')}")
        print(f"   - Model Used: {cached_result.get('model_used', 'N/A')}")
        print(f"   - Data Points: {cached_result.get('data_points_analyzed', 'N/A')}")
        print()

        # Show the actual content sections
        sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "pca_analysis",
            "heatmap_analysis",
        ]

        print("📝 REAL AI CONTENT SECTIONS:")
        print("=" * 40)

        for section in sections:
            content = cached_result.get(section, "")
            if content:
                print(f"\n🎯 {section.replace('_', ' ').upper()}:")
                print(f"   Length: {len(str(content))} characters")
                print(f"   Preview: {str(content)[:200]}...")
            else:
                print(f"❌ {section}: Missing")

        # Save to file for detailed inspection
        timestamp = (
            cached_result.get("computation_timestamp", "unknown")
            .replace(" ", "_")
            .replace(":", "-")
        )
        filename = f"real_ai_content_{timestamp}.json"

        content_data = {
            "tool": tool_name,
            "sources": selected_sources,
            "language": language,
            "model_used": cached_result.get("model_used"),
            "confidence_score": cached_result.get("confidence_score"),
            "data_points_analyzed": cached_result.get("data_points_analyzed"),
            "computation_timestamp": cached_result.get("computation_timestamp"),
            "content": {},
        }

        for section in sections:
            content_data["content"][section] = cached_result.get(section, "")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(content_data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Full content saved to: {filename}")
        return True

    except Exception as e:
        print(f"❌ Database retrieval failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    show_real_ai_content()
