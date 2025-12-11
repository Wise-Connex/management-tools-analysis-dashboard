#!/usr/bin/env python3
"""
Check if the Calidad Total + 5 sources combination exists in database.
"""

from database_implementation.precomputed_findings_db import get_precomputed_db_manager

db_manager = get_precomputed_db_manager()

tool_name = "Calidad Total"
sources = [
    "Google Trends",
    "Google Books",
    "Bain Usability",
    "Bain Satisfaction",
    "Crossref",
]
language = "es"

combination_hash = db_manager.generate_combination_hash(tool_name, sources, language)
print(f"Combination Hash: {combination_hash}")

result = db_manager.get_combination_by_hash(combination_hash)
if result:
    print("✅ Combination found in database")
    print(f"Content keys: {list(result.keys())}")

    required_sections = [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "pca_analysis",
        "heatmap_analysis",
        "strategic_synthesis",
        "conclusions",
    ]
    print("\nSection analysis:")
    for section in required_sections:
        content = result.get(section, "")
        length = len(str(content)) if content else 0
        status = "OK" if length > 50 else "MISSING/SHORT"
        print(f"  {section:20} {status} ({length:4} chars)")

    complete_sections = 0
    for section in required_sections:
        content = result.get(section, "")
        if content and len(str(content)) > 50:
            complete_sections += 1
    print(f"\nComplete sections: {complete_sections}/{len(required_sections)}")
else:
    print("❌ Combination NOT found in database")
