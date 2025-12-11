#!/usr/bin/env python3
"""
Simple verification of the database update.
"""

from database_implementation.precomputed_findings_db import get_precomputed_db_manager

db_manager = get_precomputed_db_manager()

# Check the updated content
tool_name = "Calidad Total"
sources = ["Google Trends", "Google Books", "Bain Usability", "Crossref", "Bain Books"]
language = "es"

combination_hash = db_manager.generate_combination_hash(tool_name, sources, language)
result = db_manager.get_combination_by_hash(combination_hash)

if result:
    print("Updated content verification:")
    strategic_content = result.get("strategic_synthesis", "")
    conclusions_content = result.get("conclusions", "")
    print(f"strategic_synthesis: {len(strategic_content)} chars")
    print(f"conclusions: {len(conclusions_content)} chars")

    # Simple length check
    if len(strategic_content) > 50 and len(conclusions_content) > 50:
        print("✅ Both sections now have substantial content!")
    else:
        print("⚠️ Sections may still be too short")
else:
    print("❌ Could not verify the update")
