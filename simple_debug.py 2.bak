#!/usr/bin/env python3
"""
Simple debug of hash generation and database lookup.
"""

import sqlite3
import json
import hashlib
from pathlib import Path

def simple_debug():
    """Simple debug without full service initialization."""

    print("🔍 SIMPLE DEBUG - Hash Generation and Database Lookup")
    print("=" * 70)

    # Test hash generation manually
    def generate_scenario_hash(tool_name, selected_sources, language):
        """Generate scenario hash manually."""
        data_dict = {
            "tool_name": tool_name,
            "selected_sources": sorted(selected_sources),
            "language": language,
            "date_range_start": "1950-01-01",  # Default values
            "date_range_end": "2023-12-31"
        }
        data_string = json.dumps(data_dict, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()

    print("\n1️⃣ Testing Hash Generation:")

    # Single source
    tool_name = "Benchmarking"
    selected_sources_single = ["Google Trends"]
    language = "es"

    hash_single = generate_scenario_hash(tool_name, selected_sources_single, language)
    print(f"   Single source hash: {hash_single}")

    # Multi-source
    selected_sources_multi = ["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"]
    hash_multi = generate_scenario_hash(tool_name, selected_sources_multi, language)
    print(f"   Multi-source hash: {hash_multi}")

    print("\n2️⃣ Testing Precomputed Database Direct Access:")

    # Connect directly to precomputed database
    db_path = Path('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/data/precomputed_findings.db')

    if db_path.exists():
        print(f"   ✅ Database exists at: {db_path}")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Test single source lookup
        print(f"\n   Looking up single source...")
        cursor.execute("""
            SELECT combination_hash, tool_name, sources_text, analysis_type,
                   LENGTH(COALESCE(executive_summary, '')) as exec_len,
                   LENGTH(COALESCE(principal_findings, '')) as findings_len,
                   LENGTH(COALESCE(pca_analysis, '')) as pca_len,
                   model_used, confidence_score, data_points_analyzed
            FROM precomputed_findings
            WHERE tool_name = 'Benchmarking'
            AND sources_text = 'Google Trends'
            AND language = 'es'
            AND is_active = 1
            LIMIT 1
        """)

        result = cursor.fetchone()
        if result:
            combo_hash, tool_name, sources_text, analysis_type, exec_len, findings_len, pca_len, model_used, confidence_score, data_points = result
            print(f"   ✅ Found precomputed data!")
            print(f"     Combination Hash: {combo_hash}")
            print(f"     Analysis Type: {analysis_type}")
            print(f"     Model Used: {model_used}")
            print(f"     Confidence Score: {confidence_score}")
            print(f"     Data Points: {data_points}")
            print(f"     Executive Summary: {exec_len} chars")
            print(f"     Principal Findings: {findings_len} chars")
            print(f"     PCA Analysis: {pca_len} chars")
        else:
            print(f"   ❌ No precomputed data found for single source")

        # Test multi-source lookup
        print(f"\n   Looking up multi-source...")
        cursor.execute("""
            SELECT combination_hash, tool_name, sources_text, analysis_type,
                   LENGTH(COALESCE(executive_summary, '')) as exec_len,
                   LENGTH(COALESCE(principal_findings, '')) as findings_len,
                   LENGTH(COALESCE(pca_analysis, '')) as pca_len,
                   LENGTH(COALESCE(heatmap_analysis, '')) as heatmap_len,
                   model_used, confidence_score, data_points_analyzed
            FROM precomputed_findings
            WHERE tool_name = 'Benchmarking'
            AND sources_text = 'Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref'
            AND language = 'es'
            AND is_active = 1
            LIMIT 1
        """)

        result = cursor.fetchone()
        if result:
            combo_hash, tool_name, sources_text, analysis_type, exec_len, findings_len, pca_len, heatmap_len, model_used, confidence_score, data_points = result
            print(f"   ✅ Found precomputed data!")
            print(f"     Combination Hash: {combo_hash}")
            print(f"     Analysis Type: {analysis_type}")
            print(f"     Model Used: {model_used}")
            print(f"     Confidence Score: {confidence_score}")
            print(f"     Data Points: {data_points}")
            print(f"     Executive Summary: {exec_len} chars")
            print(f"     Principal Findings: {findings_len} chars")
            print(f"     PCA Analysis: {pca_len} chars")
            print(f"     Heatmap Analysis: {heatmap_len} chars")
        else:
            print(f"   ❌ No precomputed data found for multi-source")

        conn.close()
    else:
        print(f"   ❌ Database not found at: {db_path}")

    print("\n3️⃣ Testing Combination Hash Generation:")

    # Test the exact combination hash generation used by the system
    def generate_combination_hash(tool_name, sources_text, language):
        """Generate combination hash exactly as the system does."""
        combination_data = {
            "tool_name": tool_name,
            "sources_text": sources_text,
            "language": language
        }
        combination_json = json.dumps(combination_data, sort_keys=True)
        return hashlib.sha256(combination_json.encode('utf-8')).hexdigest()

    # Single source combination hash
    combo_hash_single = generate_combination_hash("Benchmarking", "Google Trends", "es")
    print(f"   Single source combo hash: {combo_hash_single}")

    # Multi-source combination hash
    combo_hash_multi = generate_combination_hash("Benchmarking", "Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref", "es")
    print(f"   Multi-source combo hash: {combo_hash_multi}")

    print("\n" + "=" * 70)
    print("🔍 Simple Debug Complete!")
    print("=" * 70)

if __name__ == "__main__":
    simple_debug()