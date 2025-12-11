#!/usr/bin/env python3
"""
Database utilities for key findings review implementation.
Provides consistent database operations for both precomputed and runtime databases.
"""

import sqlite3
import json
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

# Import our hash utilities
from .hash_utils import (
    generate_combination_hash,
    normalize_source_name,
    normalize_tool_name,
)

# Database paths
PRECOMPUTED_DB_PATH = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db"
RUNTIME_DB_PATH = (
    "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/key_findings.db"
)


def get_precomputed_db_connection():
    """Get connection to precomputed findings database."""
    return sqlite3.connect(PRECOMPUTED_DB_PATH, timeout=30.0)


def get_runtime_db_connection():
    """Get connection to runtime cache database."""
    return sqlite3.connect(RUNTIME_DB_PATH, timeout=30.0)


def store_analysis_in_both_databases(
    tool_name: str,
    selected_sources: List[str],
    language: str,
    analysis_data: Dict[str, Any],
    model_used: str = "moonshotai/kimi-k2-instruct",
    api_latency_ms: int = 0,
    confidence_score: float = 0.85,
    data_points_analyzed: int = 1000,
) -> Dict[str, Any]:
    """
    Store analysis in both precomputed and runtime databases with consistent hashing.

    Args:
        tool_name: Management tool name
        selected_sources: List of data sources
        language: Language code
        analysis_data: Complete analysis data
        model_used: AI model used
        api_latency_ms: API response time
        confidence_score: Analysis confidence score
        data_points_analyzed: Number of data points

    Returns:
        Storage results with hashes and IDs
    """
    results = {
        "precomputed": {"success": False, "hash": "", "id": None},
        "runtime": {"success": False, "hash": "", "id": None},
        "errors": [],
    }

    try:
        # Generate consistent hash
        combination_hash = generate_combination_hash(
            tool_name, selected_sources, language
        )

        # Normalize source names for storage
        canonical_sources = [normalize_source_name(s) for s in selected_sources]
        sources_text = ", ".join(canonical_sources)

        # Store in precomputed database
        try:
            from database_implementation.precomputed_findings_db import (
                PrecomputedFindingsDBManager,
            )

            precomputed_db = PrecomputedFindingsDBManager(PRECOMPUTED_DB_PATH)

            # Prepare analysis data for precomputed database
            # Serialize any list objects to JSON strings for database storage
            def serialize_field(value):
                """Convert lists to JSON strings, leave strings as-is."""
                if isinstance(value, list):
                    return json.dumps(value)
                elif isinstance(value, dict):
                    return json.dumps(value)
                return str(value) if value is not None else ""

            precomputed_data = {
                "executive_summary": serialize_field(
                    analysis_data.get("executive_summary", "")
                ),
                "principal_findings": serialize_field(
                    analysis_data.get("principal_findings", "")
                ),
                "temporal_analysis": serialize_field(
                    analysis_data.get("temporal_analysis", "")
                ),
                "seasonal_analysis": serialize_field(
                    analysis_data.get("seasonal_analysis", "")
                ),
                "fourier_analysis": serialize_field(
                    analysis_data.get("fourier_analysis", "")
                ),
                "pca_analysis": serialize_field(analysis_data.get("pca_analysis", "")),
                "heatmap_analysis": serialize_field(
                    analysis_data.get("heatmap_analysis", "")
                ),
                "tool_display_name": analysis_data.get("tool_display_name", tool_name),
                "data_points_analyzed": data_points_analyzed,
                "confidence_score": confidence_score,
                "model_used": model_used,
            }

            # Store in precomputed database
            record_id = precomputed_db.store_precomputed_analysis(
                combination_hash,
                tool_name,
                canonical_sources,
                language,
                precomputed_data,
            )

            results["precomputed"] = {
                "success": True,
                "hash": combination_hash,
                "id": record_id,
            }

        except Exception as e:
            results["errors"].append(f"Precomputed DB error: {e}")
            results["precomputed"]["error"] = str(e)

        # Store in runtime database
        try:
            # Prepare data for runtime database
            # Serialize any list objects to JSON strings for database storage
            def serialize_field(value):
                """Convert lists to JSON strings, leave strings as-is."""
                if isinstance(value, list):
                    return json.dumps(value)
                elif isinstance(value, dict):
                    return json.dumps(value)
                return str(value) if value is not None else ""

            runtime_data = {
                "scenario_hash": combination_hash,
                "tool_name": tool_name,
                "selected_sources": json.dumps(canonical_sources),
                "language": language,
                "executive_summary": serialize_field(
                    analysis_data.get("executive_summary", "")
                ),
                "principal_findings": serialize_field(
                    analysis_data.get("principal_findings", "")
                ),
                "strategic_synthesis": serialize_field(
                    analysis_data.get("strategic_synthesis", "")
                ),
                "conclusions": serialize_field(analysis_data.get("conclusions", "")),
                "heatmap_analysis": serialize_field(
                    analysis_data.get("heatmap_analysis", "")
                ),
                "pca_analysis": serialize_field(analysis_data.get("pca_analysis", "")),
                "temporal_analysis": serialize_field(
                    analysis_data.get("temporal_analysis", "")
                ),
                "seasonal_analysis": serialize_field(
                    analysis_data.get("seasonal_analysis", "")
                ),
                "fourier_analysis": serialize_field(
                    analysis_data.get("fourier_analysis", "")
                ),
                "analysis_type": "single_source"
                if len(selected_sources) == 1
                else "multi_source",
                "sources_count": len(selected_sources),
                "model_used": model_used,
                "api_latency_ms": api_latency_ms,
                "confidence_score": confidence_score,
                "data_points_analyzed": data_points_analyzed,
            }

            # Use direct SQLite for runtime database
            conn = get_runtime_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
            INSERT INTO key_findings_reports (
                scenario_hash, tool_name, selected_sources, language,
                executive_summary, principal_findings, strategic_synthesis, conclusions,
                heatmap_analysis, pca_analysis, temporal_analysis, seasonal_analysis, fourier_analysis,
                analysis_type, sources_count, model_used, api_latency_ms, confidence_score, data_points_analyzed
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    runtime_data["scenario_hash"],
                    runtime_data["tool_name"],
                    runtime_data["selected_sources"],
                    runtime_data["language"],
                    runtime_data["executive_summary"],
                    runtime_data["principal_findings"],
                    runtime_data["strategic_synthesis"],
                    runtime_data["conclusions"],
                    runtime_data["heatmap_analysis"],
                    runtime_data["pca_analysis"],
                    runtime_data["temporal_analysis"],
                    runtime_data["seasonal_analysis"],
                    runtime_data["fourier_analysis"],
                    runtime_data["analysis_type"],
                    runtime_data["sources_count"],
                    runtime_data["model_used"],
                    runtime_data["api_latency_ms"],
                    runtime_data["confidence_score"],
                    runtime_data["data_points_analyzed"],
                ),
            )

            runtime_id = cursor.lastrowid
            conn.commit()
            conn.close()

            results["runtime"] = {
                "success": True,
                "hash": combination_hash,
                "id": runtime_id,
            }

        except Exception as e:
            results["errors"].append(f"Runtime DB error: {e}")
            results["runtime"]["error"] = str(e)

        return results

    except Exception as e:
        results["errors"].append(f"General error: {e}")
        return results


def retrieve_analysis_by_hash(combination_hash: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve analysis from both databases using hash-based lookup.

    Args:
        combination_hash: Hash of the combination

    Returns:
        Analysis data or None if not found
    """
    try:
        # Try precomputed database first
        from database_implementation.precomputed_findings_db import (
            PrecomputedFindingsDBManager,
        )

        precomputed_db = PrecomputedFindingsDBManager(PRECOMPUTED_DB_PATH)
        result = precomputed_db.get_combination_by_hash(combination_hash)

        if result:
            return {
                "source": "precomputed",
                "data": dict(result),
                "hash": combination_hash,
            }

        # Try runtime database
        conn = get_runtime_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
        SELECT * FROM key_findings_reports 
        WHERE scenario_hash = ? 
        ORDER BY generation_timestamp DESC 
        LIMIT 1
        """,
            (combination_hash,),
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            # Convert to dict with column names
            columns = [desc[0] for desc in cursor.description]
            data = dict(zip(columns, row))

            # Parse JSON fields
            if data.get("selected_sources"):
                data["selected_sources"] = json.loads(data["selected_sources"])

            return {"source": "runtime", "data": data, "hash": combination_hash}

        return None

    except Exception as e:
        print(f"Error retrieving analysis by hash: {e}")
        return None


def test_database_consistency():
    """Test consistency between both databases."""
    print("🧪 Testing Database Consistency")
    print("=" * 50)

    test_cases = [
        {
            "tool": "Benchmarking",
            "sources": ["Google Trends", "Bain Usability"],
            "language": "es",
        },
        {"tool": "Calidad Total", "sources": ["Crossref"], "language": "es"},
    ]

    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i + 1}:")
        print(f"Tool: {test_case['tool']}")
        print(f"Sources: {test_case['sources']}")
        print(f"Language: {test_case['language']}")

        # Generate hash
        from .hash_utils import generate_combination_hash

        combination_hash = generate_combination_hash(
            test_case["tool"], test_case["sources"], test_case["language"]
        )

        print(f"Hash: {combination_hash}")

        # Test retrieval
        result = retrieve_analysis_by_hash(combination_hash)

        if result:
            print(f"✅ Found in {result['source']} database")
            print(f"   Tool: {result['data'].get('tool_name', 'N/A')}")
            print(
                f"   Sources: {result['data'].get('sources_text', result['data'].get('selected_sources', 'N/A'))}"
            )
        else:
            print("❌ Not found in either database")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    test_database_consistency()
