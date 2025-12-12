#!/usr/bin/env python3
"""
Script to query AI for Calidad Total + Google Trends and save to database with new 7-section schema.
This will populate the precomputed database with the correct individual section structure.
"""

import sys
import os
import asyncio
import sqlite3
from datetime import datetime

# Add the dashboard_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

from key_findings.key_findings_service import get_key_findings_service
from database import get_database_manager
from config import get_config


async def query_ai_and_save_to_database():
    """Query AI for Calidad Total + Google Trends and save to database with new schema."""

    print(
        "🎯 Querying AI for Calidad Total + Google Trends with new 7-section schema..."
    )
    print("=" * 70)

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

        # Query AI with force_refresh=True to get fresh data with new schema
        print("\\n🔍 Querying AI with force_refresh=True (fresh generation)...")

        result = await key_findings_service.generate_key_findings(
            tool_name="Calidad Total",
            selected_sources=["Google Trends"],
            language="es",
            force_refresh=True,  # Force fresh AI generation
            source_display_names=["Google Trends"],
        )

        print(f"✅ AI query completed successfully")
        print(f"📊 Success: {result.get('success', False)}")
        print(f"📊 Cache hit: {result.get('cache_hit', False)}")
        print(f"📊 Source: {result.get('source', 'unknown')}")

        if result.get("success") and result.get("data"):
            data = result["data"]
            print(f"\\n📋 Data keys: {list(data.keys())}")

            # Check if all 7 sections are present
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

            print(f"\\n📊 Results:")
            print(
                f"   All 7 sections present: {'✅' if all_sections_present else '❌'}"
            )
            print(f"   Sections are separate: {'✅' if sections_separate else '❌'}")
            print(
                f"   Using live AI (not cached): {'✅' if not result.get('cache_hit') else '❌'}"
            )

            if (
                all_sections_present
                and sections_separate
                and not result.get("cache_hit")
            ):
                print("\\n🎉 SUCCESS: AI generated all 7 separate sections!")

                # Now save to database with new schema
                print("\\n💾 Saving to precomputed database with new schema...")
                success = await save_to_database(
                    data, "Calidad Total", ["Google Trends"], "es"
                )

                if success:
                    print("🎉 Database updated successfully!")
                    return True
                else:
                    print("❌ Failed to save to database")
                    return False
            else:
                print("\\n❌ ISSUE: AI did not generate correct structure")
                return False
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"\\n❌ AI query failed: {error_msg}")
            return False

    except Exception as e:
        print(f"\\n❌ Error during AI query: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


async def save_to_database(data, tool_name, selected_sources, language):
    """Save the AI-generated data to precomputed database with new schema."""

    try:
        db_path = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Convert tool name to Spanish (database stores Spanish names)
        from translations import get_tool_name

        spanish_tool_name = get_tool_name(tool_name, "es")

        # Convert source IDs to display names
        source_mapping = {
            "google_trends": "Google Trends",
            "google_books": "Google Books",
            "bain_usability": "Bain Usability",
            "bain_satisfaction": "Bain Satisfaction",
            "crossref": "Crossref",
            1: "Google Trends",
            2: "Google Books",
            3: "Bain Usability",
            4: "Crossref",
            5: "Bain Satisfaction",
        }

        # Convert source IDs to display names and sort by numeric ID for consistency
        source_display_pairs = []
        for source_id in selected_sources:
            display_name = source_mapping.get(source_id, str(source_id))
            # Get numeric ID for sorting
            numeric_id = (
                source_id
                if isinstance(source_id, int)
                else {
                    "google_trends": 1,
                    "google_books": 2,
                    "bain_usability": 3,
                    "crossref": 4,
                    "bain_satisfaction": 5,
                }.get(source_id, 999)
            )
            source_display_pairs.append((numeric_id, display_name))

        # Sort by numeric ID and extract display names
        source_display_pairs.sort(key=lambda x: x[0])
        display_sources = [pair[1] for pair in source_display_pairs]
        sources_text = ", ".join(display_sources)

        # Prepare data for database insertion
        executive_summary = data.get("executive_summary", "")
        principal_findings = data.get("principal_findings", "")
        temporal_analysis = data.get("temporal_analysis", "")
        seasonal_analysis = data.get("seasonal_analysis", "")
        fourier_analysis = data.get("fourier_analysis", "")
        strategic_synthesis = data.get("strategic_synthesis", "")
        conclusions = data.get("conclusions", "")
        pca_analysis = data.get("pca_analysis", "")
        heatmap_analysis = data.get("heatmap_analysis", "")
        confidence_score = data.get("confidence_score", 0.0)
        model_used = data.get("model_used", "unknown")
        data_points_analyzed = data.get("data_points_analyzed", 0)
        analysis_type = (
            "single_source" if len(selected_sources) == 1 else "multi_source"
        )

        # Check if record already exists
        cursor.execute(
            """
            SELECT id FROM precomputed_findings 
            WHERE tool_name = ? AND sources_text = ? AND language = ? AND is_active = 1
        """,
            (spanish_tool_name, sources_text, language),
        )

        existing_record = cursor.fetchone()

        if existing_record:
            # Update existing record
            print(
                f"   🔄 Updating existing record for {tool_name} + {len(selected_sources)} sources"
            )
            cursor.execute(
                """
                UPDATE precomputed_findings 
                SET executive_summary = ?, principal_findings = ?, temporal_analysis = ?,
                    seasonal_analysis = ?, fourier_analysis = ?, pca_analysis = ?,
                    heatmap_analysis = ?, confidence_score = ?, model_used = ?,
                    data_points_analyzed = ?, analysis_type = ?, updated_at = ?
                WHERE id = ?
            """,
                (
                    executive_summary,
                    principal_findings,
                    temporal_analysis,
                    seasonal_analysis,
                    fourier_analysis,
                    pca_analysis,
                    heatmap_analysis,
                    confidence_score,
                    model_used,
                    data_points_analyzed,
                    analysis_type,
                    datetime.now(),
                    existing_record[0],
                ),
            )
        else:
            # Insert new record
            print(
                f"   💾 Inserting new record for {tool_name} + {len(selected_sources)} sources"
            )
            cursor.execute(
                """
                INSERT INTO precomputed_findings 
                (tool_name, sources_text, language, executive_summary, principal_findings, 
                 temporal_analysis, seasonal_analysis, fourier_analysis, pca_analysis, 
                 heatmap_analysis, confidence_score, model_used, data_points_analyzed, 
                 analysis_type, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
            """,
                (
                    spanish_tool_name,
                    sources_text,
                    language,
                    executive_summary,
                    principal_findings,
                    temporal_analysis,
                    seasonal_analysis,
                    fourier_analysis,
                    pca_analysis,
                    heatmap_analysis,
                    confidence_score,
                    model_used,
                    data_points_analyzed,
                    analysis_type,
                    datetime.now(),
                    datetime.now(),
                ),
            )

        conn.commit()
        conn.close()

        print(f"   ✅ Successfully saved to database")
        return True

    except Exception as e:
        print(f"   ❌ Error saving to database: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(query_ai_and_save_to_database())
    print(f"\\n🎯 Final result: {'SUCCESS' if success else 'FAILURE'}")
    sys.exit(0 if success else 1)
EOF
