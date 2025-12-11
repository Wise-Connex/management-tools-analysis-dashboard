#!/usr/bin/env python3
"""
Test script to demonstrate the new AI validation system for Calidad Total queries.
This script shows what the queries would look like and validates existing content.
"""

import os
import sys
from datetime import datetime
from database_implementation.precomputed_findings_db import get_precomputed_db_manager

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_validation_system():
    """Test the new validation system with existing database content."""

    print("🧪 TESTING NEW AI VALIDATION SYSTEM")
    print("=" * 60)

    # Initialize database manager
    db_manager = get_precomputed_db_manager()

    # Test cases
    tool_name = "Calidad Total"
    language = "es"

    # Single source test
    single_sources = ["Google Trends"]

    # Multi source test
    multi_sources = [
        "Google Trends",
        "Bain Usability",
        "Bain Satisfaction",
        "Crossref",
        "Google Books",
    ]

    print(f"📊 Testing validation for: {tool_name}")
    print(f"🌍 Language: {language}")
    print()

    # Test single source
    print("🔍 SINGLE SOURCE ANALYSIS (Google Trends)")
    print("-" * 50)

    single_hash = db_manager.generate_combination_hash(
        tool_name, single_sources, language
    )
    single_result = db_manager.get_combination_by_hash(single_hash)

    if single_result:
        validate_single_source_content(single_result)
    else:
        print("❌ Single source result not found in database")

    print()

    # Test multi source
    print("🔍 MULTI SOURCE ANALYSIS (All 5 sources)")
    print("-" * 50)

    multi_hash = db_manager.generate_combination_hash(
        tool_name, multi_sources, language
    )
    multi_result = db_manager.get_combination_by_hash(multi_hash)

    if multi_result:
        validate_multi_source_content(multi_result)
    else:
        print("❌ Multi source result not found in database")

    print()

    # Show what the new queries would look like
    print("📝 NEW AI QUERY REQUIREMENTS")
    print("-" * 50)
    show_new_query_requirements()


def validate_single_source_content(result):
    """Validate single source content against new requirements."""

    required_sections = [
        "executive_summary",
        "principal_findings",
        "temporal_analysis",
        "seasonal_analysis",
        "fourier_analysis",
        "strategic_synthesis",
        "conclusions",
    ]

    print("Required sections for single-source analysis:")
    all_present = True

    for section in required_sections:
        content = result.get(section, "")
        has_content = bool(content and len(str(content)) > 50)
        status = "✅" if has_content else "❌"
        length = len(str(content)) if content else 0

        print(f"  {section:20} {status} ({length:4} chars)")

        if not has_content:
            all_present = False

    print(f"\nResult: {'✅ COMPLETE' if all_present else '❌ INCOMPLETE'}")

    # Show content samples
    if result.get("executive_summary"):
        print(f"\n📝 Executive Summary preview:")
        print(f"{result['executive_summary'][:200]}...")


def validate_multi_source_content(result):
    """Validate multi source content against new requirements."""

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

    print("Required sections for multi-source analysis:")
    all_present = True

    for section in required_sections:
        content = result.get(section, "")
        has_content = bool(content and len(str(content)) > 50)
        status = "✅" if has_content else "❌"
        length = len(str(content)) if content else 0

        print(f"  {section:20} {status} ({length:4} chars)")

        if not has_content:
            all_present = False

    print(f"\nResult: {'✅ COMPLETE' if all_present else '❌ INCOMPLETE'}")

    # Show content samples
    sections_with_content = [
        s for s in required_sections if result.get(s) and len(str(result[s])) > 50
    ]
    if sections_with_content:
        print(f"\n📋 Available sections: {', '.join(sections_with_content)}")

        if "pca_analysis" in result and result["pca_analysis"]:
            print(f"\n🎯 PCA Analysis preview:")
            print(f"{result['pca_analysis'][:200]}...")


def show_new_query_requirements():
    """Show what the new AI queries would require."""

    print("Single-source analysis requires 7 sections:")
    print("  1. Executive Summary (400 words)")
    print("  2. Principal Findings (600 words)")
    print("  3. Temporal Analysis (1000 words) - MANDATORY")
    print("  4. Seasonal Analysis (800 words) - MANDATORY")
    print("  5. Fourier Analysis (800 words) - MANDATORY")
    print("  6. Strategic Synthesis (600 words) - MANDATORY")
    print("  7. Conclusions (400 words) - MANDATORY")

    print("\nMulti-source analysis requires 9 sections:")
    print("  1. Executive Summary (400 words)")
    print("  2. Principal Findings (600 words)")
    print("  3. Temporal Analysis (800 words) - OBLIGATORIO")
    print("  4. Seasonal Analysis (600 words) - OBLIGATORIO - NEW!")
    print("  5. Heatmap Analysis (800 words) - OBLIGATORIO")
    print("  6. PCA Analysis (600 words) - OBLIGATORIO")
    print("  7. Fourier Analysis (600 words) - OBLIGATORIO")
    print("  8. Strategic Synthesis (400 words) - OBLIGATORIO")
    print("  9. Conclusions (600 words) - OBLIGATORIO")

    print("\n🚨 VALIDATION RULES:")
    print("  - ALL sections must be present with substantial content (>50 chars)")
    print("  - NO default content generation - AI must provide everything")
    print("  - Incomplete responses are REJECTED and trigger retry")
    print("  - Validation occurs at JSON, markdown, and fragment parsing levels")


def show_query_examples():
    """Show example queries that would be sent to AI."""

    print("📝 EXAMPLE AI QUERIES")
    print("=" * 60)

    print("\n🔍 SINGLE SOURCE QUERY (Calidad Total + Google Trends):")
    print("-" * 50)
    print("""
Herramienta: Calidad Total
Fuente: Google Trends
Período: 2020-2024

REQUERIMIENTOS:
- Análisis temporal de tendencias de búsqueda
- Patrones estacionales en interés público
- Análisis espectral de ciclos de adopción
- Síntesis estratégica de hallazgos temporales
- Conclusiones sobre timing de implementación

FORMATO JSON OBLIGATORIO con 7 secciones.
""")

    print("\n🔍 MULTI SOURCE QUERY (Calidad Total + All 5 sources):")
    print("-" * 50)
    print("""
Herramienta: Calidad Total  
Fuentes: Google Trends, Bain Usability, Bain Satisfaction, Crossref, Google Books
Período: 2020-2024

REQUERIMIENTOS:
- Análisis de correlaciones entre fuentes
- Comparación de estacionalidad entre stakeholders
- PCA de influencia por fuente (público vs empresa vs academia)
- Mapa de calor de alineaciones/desalineaciones
- Análisis espectral combinado
- Síntesis estratégica multi-fuente
- Conclusiones con recomendaciones accionables

FORMATO JSON OBLIGATORIO con 9 secciones incluyendo seasonal_analysis.
""")


if __name__ == "__main__":
    test_validation_system()
    print("\n" + "=" * 60)
    show_query_examples()
    print("\n✅ Validation system test completed!")
