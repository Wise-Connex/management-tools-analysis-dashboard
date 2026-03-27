#!/usr/bin/env python3
"""
Store Sample Analysis Data for 30 Generated Combinations

This script populates the precomputed_findings database with sample analysis data
for the 30 combinations we generated, so they work in the dashboard.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def create_sample_analysis(
    tool_name: str, sources: list, language: str, is_single_source: bool = True
) -> dict:
    """Create sample analysis data for testing."""

    # Language-specific content
    if language == "es":
        summaries = {
            "Benchmarking": "El benchmarking es una herramienta fundamental para la mejora continua organizacional. Permite comparar procesos, productos y servicios con los mejores estándares de la industria.",
            "Competencias Centrales": "Las competencias centrales representan las capacidades únicas que distinguen a una organización de sus competidores y crean valor sostenible.",
            "Cuadro de Mando Integral": "El Cuadro de Mando Integral proporciona una visión equilibrada del desempeño organizacional a través de múltiples perspectivas estratégicas.",
            "Experiencia del Cliente": "La experiencia del cliente abarca todos los puntos de contacto entre la organización y sus clientes, desde la percepción inicial hasta la post-compra.",
            "Fusiones y Adquisiciones": "Las fusiones y adquisiciones son estrategias de crecimiento que combinan o adquieren empresas para crear valor sinérgico.",
            "Gestión de Costos": "La gestión de costos se enfoca en identificar, analizar y optimizar los gastos para mejorar la rentabilidad organizacional.",
            "Innovación Colaborativa": "La innovación colaborativa fomenta la creatividad y el desarrollo de nuevas soluciones mediante la colaboración interna y externa.",
            "Lealtad del Cliente": "La lealtad del cliente mide la disposición de los consumidores a mantener relaciones continuas con la marca.",
            "Outsourcing": "El outsourcing permite a las organizaciones externalizar funciones no estratégicas para enfocarse en sus competencias centrales.",
            "Planificación Estratégica": "La planificación estratégica establece la dirección a largo plazo de la organización mediante objetivos y estrategias claras.",
        }
    else:
        summaries = {
            "Benchmarking": "Benchmarking is a fundamental tool for continuous organizational improvement. It allows comparing processes, products, and services with industry best practices.",
            "Competencias Centrales": "Core competencies represent unique capabilities that distinguish an organization from competitors and create sustainable value.",
            "Cuadro de Mando Integral": "The Balanced Scorecard provides a balanced view of organizational performance through multiple strategic perspectives.",
            "Experiencia del Cliente": "Customer experience encompasses all touchpoints between the organization and its customers, from initial perception to post-purchase.",
            "Fusiones y Adquisiciones": "Mergers and acquisitions are growth strategies that combine or acquire companies to create synergistic value.",
            "Gestión de Costos": "Cost management focuses on identifying, analyzing, and optimizing expenses to improve organizational profitability.",
            "Innovación Colaborativa": "Collaborative innovation fosters creativity and development of new solutions through internal and external collaboration.",
            "Lealtad del Cliente": "Customer loyalty measures consumers' willingness to maintain ongoing relationships with the brand.",
            "Outsourcing": "Outsourcing allows organizations to externalize non-strategic functions to focus on core competencies.",
            "Planificación Estratégica": "Strategic planning establishes the organization's long-term direction through clear objectives and strategies.",
        }

    # Get summary for tool (fallback to generic if not found)
    summary = summaries.get(
        tool_name,
        f"Análisis de {tool_name} basado en datos de múltiples fuentes para optimizar el rendimiento organizacional.",
    )

    # Create analysis structure
    analysis = {
        "executive_summary": summary,
        "principal_findings": f"Análisis detallado de {tool_name} mostrando tendencias significativas en los datos de {', '.join(sources)}.",
        "temporal_analysis": f"Análisis temporal de {tool_name} revela patrones cíclicos y tendencias de crecimiento en los datos históricos. Los períodos de mayor actividad coinciden con cambios estacionales en el mercado. La volatilidad del indicador muestra correlación directa con eventos económicos importantes.",
        "seasonal_analysis": f"El análisis estacional de {tool_name} indica patrones predecibles de variación a lo largo del año. Los picos de actividad se observan típicamente en el primer y tercer trimestre, mientras que los mínimos ocurren en períodos vacacionales. La fuerza estacional sugiere oportunidades de planificación estratégica.",
        "fourier_analysis": f"El análisis espectral de Fourier identifica frecuencias dominantes en los datos de {tool_name}. Se detectan ciclos principales de 12 meses con componentes secundarios de 6 meses. Los picos espectrales indican períodos óptimos para implementación de iniciativas relacionadas con {tool_name}.",
        "tool_display_name": tool_name,
        "data_points_analyzed": 120,
        "confidence_score": 0.85,
        "model_used": "sample_data",
    }

    # Add multi-source specific sections
    if not is_single_source:
        analysis["pca_analysis"] = (
            f"El análisis de componentes principales revela que {', '.join(sources)} contribuyen de manera diferenciada al perfil de {tool_name}. La primera componente principal explica el 45% de la varianza total, mientras que la segunda componente captura patrones estacionales. Las fuentes muestran correlaciones moderadas, indicando complementariedad en lugar de redundancia."
        )
        analysis["heatmap_analysis"] = (
            f"El mapa de calor de correlaciones entre las fuentes de datos para {tool_name} muestra relaciones complejas. Google Trends presenta correlación positiva moderada con Google Books (r=0.62), mientras que Bain Usability muestra correlación negativa con Crossref (r=-0.34). Estas correlaciones sugieren dinámicas complementarias entre opinión pública, práctica empresarial e investigación académica."
        )

    return analysis


def main():
    """Main function to store sample data for all 30 combinations."""

    print("🚀 Storing Sample Analysis Data for 30 Combinations")
    print("=" * 60)

    # Initialize database manager
    db_manager = get_precomputed_db_manager()

    # Load our generated combinations
    results_file = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/30_combination_generation_results_20251212_003348.json"

    try:
        with open(results_file, "r", encoding="utf-8") as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"❌ Results file not found: {results_file}")
        return

    # Process each combination
    stored_count = 0
    failed_count = 0

    print(f"📊 Processing {len(results['details'])} combinations...")

    for detail in results["details"]:
        try:
            tool_name = detail["tool"]
            sources = detail["sources"]
            language = detail["language"]
            hash_value = detail["hash"]
            category = detail["category"]

            # Determine if single or multi-source
            is_single_source = len(sources) == 1

            # Create sample analysis
            analysis_data = create_sample_analysis(
                tool_name, sources, language, is_single_source
            )

            # Store in database
            record_id = db_manager.store_precomputed_analysis(
                combination_hash=hash_value,
                tool_name=tool_name,
                selected_sources=sources,
                language=language,
                analysis_data=analysis_data,
            )

            if record_id:
                stored_count += 1
                print(
                    f"✅ Stored: {tool_name} + {len(sources)} sources ({language}) - ID: {record_id}"
                )
            else:
                failed_count += 1
                print(f"❌ Failed: {tool_name} + {len(sources)} sources ({language})")

        except Exception as e:
            failed_count += 1
            print(f"❌ Error storing {detail.get('tool', 'Unknown')}: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 STORAGE SUMMARY")
    print("=" * 60)
    print(f"Total combinations: {len(results['details'])}")
    print(f"Successfully stored: {stored_count}")
    print(f"Failed: {failed_count}")
    print(f"Success rate: {(stored_count / len(results['details'])) * 100:.1f}%")

    # Verify in database
    print("\n🔍 DATABASE VERIFICATION")
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM precomputed_findings")
            total_count = cursor.fetchone()[0]
            print(f"Total records in database: {total_count}")

            # Test a few specific combinations
            test_hashes = [
                "benchmarking_google_trends_es_457d64d712",
                "competencias_centrales_google_trends_en_42726c3bb3",
                "cuadro_de_mando_integral_google_books_es_ab03d9a683",
            ]

            print("\n🎯 Testing specific combinations:")
            for hash_val in test_hashes:
                result = db_manager.get_combination_by_hash(hash_val)
                if result:
                    print(
                        f"✅ Found: {result['tool_name']} + {result['sources_text']} ({result['language']})"
                    )
                else:
                    print(f"❌ Missing: {hash_val}")

    except Exception as e:
        print(f"❌ Database verification error: {e}")

    print("\n🎉 Sample data storage complete!")
    print("You can now test these combinations in the dashboard.")


if __name__ == "__main__":
    main()
