#!/usr/bin/env python3
"""
Simple test to verify complete content is stored.
"""

from database_implementation.precomputed_findings_db import get_precomputed_db_manager

db = get_precomputed_db_manager()

# Check the specific combination
combination_hash = "calidad_total_bain_satisfaction_bain_usability_crossref_google_books_google_trends_es_556ff3371a"
result = db.get_combination_by_hash(combination_hash)

if result:
    print("✅ Content found in database")
    print("Sections found:")
    for section in [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "pca_analysis",
        "heatmap_analysis",
        "strategic_synthesis",
        "conclusions",
    ]:
        content = result.get(section, "")
        print(f"{section}: {len(str(content))} chars")

    # Count complete sections
    complete_count = 0
    for section in [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "pca_analysis",
        "heatmap_analysis",
        "strategic_synthesis",
        "conclusions",
    ]:
        content = result.get(section, "")
        if content and len(str(content)) > 50:
            complete_count += 1

    print(f"\\n🎉 FINAL RESULT: {complete_count}/9 sections complete!")

    if complete_count == 9:
        print("🎉 SUCCESS! All 9 sections are now complete and validated!")
    else:
        print("⚠️ Still incomplete - sections missing or too short")
else:
    print("❌ No content found in database")
