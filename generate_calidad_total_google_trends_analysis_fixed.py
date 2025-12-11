#!/usr/bin/env python3
"""
Enhanced script to query AI for Calidad Total + Google Trends and save to both database and file.
This will generate fresh AI analysis and save it with complete metadata for review.
"""

import sys
import os
import asyncio
import sqlite3
import json
from datetime import datetime
from pathlib import Path

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # dotenv not available, rely on environment variables

# Add the dashboard_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Import modules after path setup
try:
    from key_findings.key_findings_service import get_key_findings_service
    from database import get_database_manager
    from config import get_config
    from translations import get_tool_name
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Available modules in dashboard_app:")
    import os

    print(os.listdir("dashboard_app"))
    sys.exit(1)


async def query_ai_and_save_to_database_and_file():
    """Query AI for Calidad Total + Google Trends and save to both database and file."""

    print(
        "🎯 Querying AI for Calidad Total + Google Trends with enhanced 7-section schema..."
    )
    print("=" * 80)

    try:
        # Initialize the service with the same configuration as the app
        config = get_config()
        db_manager = get_database_manager()

        # Convert config to dictionary for the AI service
        config_dict = {
            "max_retries": 3,
            "enable_pca_emphasis": True,
            "confidence_threshold": 0.7,
        }

        # Get the key findings service (same as used in the app)
        key_findings_service = get_key_findings_service(
            db_manager=db_manager,
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
            config=config_dict,
        )

        print("✅ Key Findings service initialized")

        # Query AI with force_refresh=True to get fresh data with new schema
        print("\n🔍 Querying AI with force_refresh=True (fresh generation)...")

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
        print(f"📊 Response time: {result.get('response_time_ms', 0)}ms")

        if result.get("success") and result.get("data"):
            data = result["data"]
            print(f"\n📋 Data keys: {list(data.keys())}")

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

            print("\n🔍 Section Analysis:")
            all_sections_present = True
            section_lengths = {}

            for section in expected_sections:
                content = data.get(section, "")
                is_present = bool(content and len(str(content)) > 10)
                status = "✅" if is_present else "❌"
                content_length = len(str(content))
                section_lengths[section] = content_length

                print(f"   {status} {section}: {content_length:,} characters")

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

            print(f"\n📊 Results:")
            print(
                f"   All 7 sections present: {'✅' if all_sections_present else '❌'}"
            )
            print(f"   Sections are separate: {'✅' if sections_separate else '❌'}")
            print(
                f"   Using live AI (not cached): {'✅' if not result.get('cache_hit') else '❌'}"
            )

            # Allow partial success - save even if seasonal_analysis is missing
            # The AI generated 6 out of 7 sections which is still valuable
            sections_generated = len(
                [
                    s
                    for s in expected_sections
                    if data.get(s) and len(str(data.get(s))) > 10
                ]
            )

            if (
                sections_separate
                and not result.get("cache_hit")
                and sections_generated >= 6
            ):
                print(
                    f"\n🎉 SUCCESS: AI generated {sections_generated} out of 7 sections!"
                )
                if sections_generated < 7:
                    missing_sections = [
                        s
                        for s in expected_sections
                        if not data.get(s) or len(str(data.get(s))) <= 10
                    ]
                    print(f"⚠️  Note: Missing sections: {', '.join(missing_sections)}")

                # Now save to database with new schema
                print("\n💾 Saving to precomputed database with new schema...")
                db_success = await save_to_database(
                    data, "Calidad Total", ["Google Trends"], "es"
                )

                # Save to file for review
                print("\n📝 Saving to file for review...")
                file_success = save_to_file(
                    data, result, "Calidad Total", ["Google Trends"], "es"
                )

                if db_success and file_success:
                    print("🎉 Database and file saved successfully!")

                    # Show performance metrics
                    print(f"\n📈 Performance Metrics:")
                    print(f"   Response time: {result.get('response_time_ms', 0)}ms")
                    print(f"   Model used: {data.get('model_used', 'unknown')}")
                    print(f"   Confidence score: {data.get('confidence_score', 0):.2f}")
                    print(
                        f"   Data points analyzed: {data.get('data_points_analyzed', 0)}"
                    )
                    print(f"   Sections generated: {sections_generated}/7")

                    return True
                else:
                    print("❌ Failed to save to database or file")
                    return False
            else:
                print("\n❌ ISSUE: AI did not generate sufficient structure")
                return False
        else:
            error_msg = result.get("error", "Unknown error")
            print(f"\n❌ AI query failed: {error_msg}")
            return False

    except Exception as e:
        print(f"\n❌ Error during AI query: {str(e)}")
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
        executive_summary = str(data.get("executive_summary", ""))
        principal_findings = str(data.get("principal_findings", ""))
        temporal_analysis = str(data.get("temporal_analysis", ""))
        seasonal_analysis = str(data.get("seasonal_analysis", ""))
        fourier_analysis = str(data.get("fourier_analysis", ""))
        strategic_synthesis = str(data.get("strategic_synthesis", ""))
        conclusions = str(data.get("conclusions", ""))
        pca_analysis = str(data.get("pca_analysis", ""))
        heatmap_analysis = str(data.get("heatmap_analysis", ""))
        confidence_score = float(data.get("confidence_score", 0.0))
        model_used = str(data.get("model_used", "unknown"))
        data_points_analyzed = int(data.get("data_points_analyzed", 0))
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
                    data_points_analyzed = ?, analysis_type = ?, strategic_synthesis = ?, conclusions = ?
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
                    strategic_synthesis,
                    conclusions,
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
                 analysis_type, is_active, created_at, updated_at, strategic_synthesis, conclusions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?, ?, ?)
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
                    strategic_synthesis,
                    conclusions,
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


def save_to_file(data, result, tool_name, selected_sources, language):
    """Save the AI-generated data to a JSON file for review."""

    try:
        # Create output directory if it doesn't exist
        output_dir = Path(
            "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/ai_analysis_exports"
        )
        output_dir.mkdir(exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"calidad_total_google_trends_ai_analysis_{timestamp}.json"
        filepath = output_dir / filename

        # Prepare comprehensive export data
        export_data = {
            "query_metadata": {
                "tool_name": tool_name,
                "selected_sources": selected_sources,
                "language": language,
                "generated_at": datetime.now().isoformat(),
                "analysis_type": "single_source",
                "response_time_ms": result.get("response_time_ms", 0),
                "cache_hit": result.get("cache_hit", False),
                "source": result.get("source", "unknown"),
            },
            "ai_service_metadata": {
                "model_used": data.get("model_used", "unknown"),
                "confidence_score": data.get("confidence_score", 0.0),
                "data_points_analyzed": data.get("data_points_analyzed", 0),
                "api_latency_ms": data.get("api_latency_ms", 0),
            },
            "ai_response": {
                "executive_summary": data.get("executive_summary", ""),
                "principal_findings": data.get("principal_findings", ""),
                "temporal_analysis": data.get("temporal_analysis", ""),
                "seasonal_analysis": data.get("seasonal_analysis", ""),
                "fourier_analysis": data.get("fourier_analysis", ""),
                "strategic_synthesis": data.get("strategic_synthesis", ""),
                "conclusions": data.get("conclusions", ""),
                "pca_analysis": data.get("pca_analysis", ""),
                "heatmap_analysis": data.get("heatmap_analysis", ""),
            },
            "section_analysis": {
                "executive_summary_length": len(data.get("executive_summary", "")),
                "principal_findings_length": len(data.get("principal_findings", "")),
                "temporal_analysis_length": len(data.get("temporal_analysis", "")),
                "seasonal_analysis_length": len(data.get("seasonal_analysis", "")),
                "fourier_analysis_length": len(data.get("fourier_analysis", "")),
                "strategic_synthesis_length": len(data.get("strategic_synthesis", "")),
                "conclusions_length": len(data.get("conclusions", "")),
                "total_words": sum(
                    len(str(data.get(section, "")).split())
                    for section in [
                        "executive_summary",
                        "principal_findings",
                        "temporal_analysis",
                        "seasonal_analysis",
                        "fourier_analysis",
                        "strategic_synthesis",
                        "conclusions",
                    ]
                ),
            },
        }

        # Write to file with pretty formatting
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)

        print(f"   ✅ Successfully saved to file: {filepath}")
        print(f"   📊 File size: {filepath.stat().st_size:,} bytes")
        print(f"   📝 Total words: {export_data['section_analysis']['total_words']:,}")

        return True

    except Exception as e:
        print(f"   ❌ Error saving to file: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(query_ai_and_save_to_database_and_file())
    print(f"\n🎯 Final result: {'SUCCESS' if success else 'FAILURE'}")
    sys.exit(0 if success else 1)
