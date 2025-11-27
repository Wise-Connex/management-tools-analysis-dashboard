#!/usr/bin/env python3
"""
Populate database with proper test data for single source and multi-source analysis.
"""

import sqlite3
import json
import datetime
import sys

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

def populate_test_data():
    """Populate database with test data for both single source and multi-source analysis."""

    db_path = '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/data/key_findings.db'

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print("🧹 Cleaning database...")
        # Clear existing data
        cursor.execute("DELETE FROM key_findings_reports")
        cursor.execute("DELETE FROM key_findings_history")
        cursor.execute("DELETE FROM cache_statistics")
        cursor.execute("DELETE FROM model_performance")

        print("✅ Database cleaned")

        print("📋 Populating with test data...")

        # === SINGLE SOURCE ANALYSIS (1 source) ===
        print("🎯 Creating single source analysis...")

        # Single source - Google Trends only
        single_source_data = {
            "scenario_hash": "single_source_test_001",
            "tool_name": "Benchmarking",
            "selected_sources": json.dumps(["Google Trends"]),
            "date_range_start": "1950-01-01",
            "date_range_end": "2023-12-31",
            "language": "es",
            "model_used": "moonshotai/kimi-k2-instruct",
            "api_latency_ms": 19782,
            "confidence_score": 0.85,
            "data_points_analyzed": 888,
            "sources_count": 1,
            "analysis_depth": "comprehensive"
        }

        # Single source principal findings
        single_findings = [
            {
                "bullet_point": "Patrones temporales revelan madurez de mercado con volatilidad decreciente",
                "reasoning": "La estabilidad temporal observada indica que Benchmarking ha evolucionado desde práctica emergente a disciplina establecida, reduciendo riesgos de implementación."
            },
            {
                "bullet_point": "Ciclos espectrales de 4-5 años alineados con patrones económicos",
                "reasoning": "El análisis espectral identifica ciclos que coinciden con crisis económicas, sugiriendo que Benchmarking responde a necesidades estratégicas cíclicas."
            },
            {
                "bullet_point": "Estacionalidad Q1/Q3 revela ventanas óptimas de implementación",
                "reasoning": "Los picos estacionales en períodos de planificación corporativa crean ventanas anuales para implementación con distintos enfoques estratégicos."
            }
        ]

        single_source_data["principal_findings"] = json.dumps(single_findings)

        single_source_data["executive_summary"] = (
            "El análisis temporal integral de Benchmarking a través de Google Trends (1950-2023) revela un ciclo de vida maduro "
            "con patrones estacionales estables y ciclos espectrales bien definidos. Los hallazgos indican que la herramienta "
            "se encuentra en fase de estabilización tras experimentar picos de adopción significativos. El análisis espectral "
            "identifica ciclos principales de aproximadamente 4-5 años, coincidiendo con ciclos económicos clásicos."
        )

        single_source_data["pca_insights"] = json.dumps({
            "analysis": {
                "componentes_principales": [{"varianza_explicada": 0.78}],
                "patrones_temporales": "estables"
            },
            "reasoning": "El análisis de componentes principales confirma la importancia estratégica de Benchmarking como herramienta de gestión."
        })

        # Insert single source report
        cursor.execute("""
            INSERT INTO key_findings_reports (
                scenario_hash, tool_name, selected_sources, date_range_start, date_range_end,
                language, principal_findings, pca_insights, executive_summary,
                model_used, api_latency_ms, confidence_score, data_points_analyzed,
                sources_count, analysis_depth, generation_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            single_source_data["scenario_hash"],
            single_source_data["tool_name"],
            single_source_data["selected_sources"],
            single_source_data["date_range_start"],
            single_source_data["date_range_end"],
            single_source_data["language"],
            single_source_data["principal_findings"],
            single_source_data["pca_insights"],
            single_source_data["executive_summary"],
            single_source_data["model_used"],
            single_source_data["api_latency_ms"],
            single_source_data["confidence_score"],
            single_source_data["data_points_analyzed"],
            single_source_data["sources_count"],
            single_source_data["analysis_depth"],
            datetime.datetime.now()
        ))

        # === MULTI-SOURCE ANALYSIS (5 sources) ===
        print("🎯 Creating multi-source analysis...")

        # Multi-source - 5 sources
        multi_source_data = {
            "scenario_hash": "multi_source_test_001",
            "tool_name": "Benchmarking",
            "selected_sources": json.dumps(["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"]),
            "date_range_start": "1950-01-01",
            "date_range_end": "2023-12-31",
            "language": "es",
            "model_used": "moonshotai/kimi-k2-instruct",
            "api_latency_ms": 21682,
            "confidence_score": 0.92,
            "data_points_analyzed": 1247,
            "sources_count": 5,
            "analysis_depth": "comprehensive"
        }

        # Multi-source principal findings
        multi_findings = [
            {
                "bullet_point": "Convergencia total de stakeholders revela madurez de mercado",
                "reasoning": "El 78.5% de varianza explicada por un único componente indica alineación perfecta entre Google Trends, Bain y fuentes académicas, sugiriendo que Benchmarking ha alcanzado un estado de madurez donde ya no existen fronteras conceptuales entre stakeholders."
            },
            {
                "bullet_point": "Desalineación crítica Bain Satisfaction indica brecha expectativa-realidad",
                "reasoning": "Mientras que Google Trends y Google Books muestran crecimiento constante, Bain Satisfaction revela un patrón de 'expectativas infladas-resultados moderados', sugiriendo que la implementación real no cumple con las expectativas generadas."
            },
            {
                "bullet_point": "Ciclos espectrales de 7-8 años actúan como reloj estratégico",
                "reasoning": "El análisis espectral identifica ciclos principales que coinciden con crisis económicas, permitiendo a las organizaciones anticipar y prepararse para los cambios en el entorno competitivo."
            }
        ]

        multi_source_data["principal_findings"] = json.dumps(multi_findings)

        multi_source_data["executive_summary"] = (
            "El análisis multi-fuente de Benchmarking revela una herramienta de gestión que ha alcanzado verdadera madurez "
            "de mercado a través de una convergencia sin precedentes entre opinión pública, práctica empresarial e investigación académica. "
            "La singularidad del componente principal identificado (78.5% de varianza) indica que el Benchmarking ha evolucionado "
            "desde una técnica competitiva aislada hacia un paradigma integrado de mejora continua."
        )

        multi_source_data["pca_insights"] = json.dumps({
            "analysis": {
                "dominant_patterns": [{"component": 1, "loadings": {"Google Trends": 0.8, "Google Books": 0.7, "Bain Usability": 0.6, "Bain Satisfaction": 0.5, "Crossref": 0.9}}],
                "total_variance_explained": 78.5
            },
            "reasoning": "El PCA revela alineamiento entre stakeholders pero identifica desalineamiento crítico en satisfacción post-implementación."
        })

        # Insert multi-source report
        cursor.execute("""
            INSERT INTO key_findings_reports (
                scenario_hash, tool_name, selected_sources, date_range_start, date_range_end,
                language, principal_findings, pca_insights, executive_summary,
                model_used, api_latency_ms, confidence_score, data_points_analyzed,
                sources_count, analysis_depth, generation_timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            multi_source_data["scenario_hash"],
            multi_source_data["tool_name"],
            multi_source_data["selected_sources"],
            multi_source_data["date_range_start"],
            multi_source_data["date_range_end"],
            multi_source_data["language"],
            multi_source_data["principal_findings"],
            multi_source_data["pca_insights"],
            multi_source_data["executive_summary"],
            multi_source_data["model_used"],
            multi_source_data["api_latency_ms"],
            multi_source_data["confidence_score"],
            multi_source_data["data_points_analyzed"],
            multi_source_data["sources_count"],
            multi_source_data["analysis_depth"],
            datetime.datetime.now()
        ))

        # Add history entries
        print("📜 Adding history entries...")

        cursor.execute("""
            INSERT INTO key_findings_history (
                scenario_hash, report_id, change_type, change_timestamp, change_reason
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            single_source_data["scenario_hash"],
            1,  # Will be the ID of the first report
            "new",
            datetime.datetime.now(),
            "Initial single source analysis generation"
        ))

        cursor.execute("""
            INSERT INTO key_findings_history (
                scenario_hash, report_id, change_type, change_timestamp, change_reason
            ) VALUES (?, ?, ?, ?, ?)
        """, (
            multi_source_data["scenario_hash"],
            2,  # Will be the ID of the second report
            "new",
            datetime.datetime.now(),
            "Initial multi-source analysis generation"
        ))

        # Add cache statistics
        print("📊 Adding cache statistics...")

        cursor.execute("""
            INSERT INTO cache_statistics (
                id, date, total_requests, cache_hits, cache_misses, avg_response_time_ms, unique_scenarios
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            1,
            datetime.date.today(),
            2,  # total requests
            2,  # cache hits
            0,  # cache misses
            19782.0,  # average response time
            2   # unique scenarios (our 2 test cases)
        ))

        conn.commit()
        print("✅ Test data populated successfully!")

        # Show summary of what was added
        print("\\n📋 Database Summary:")
        cursor.execute("SELECT COUNT(*) FROM key_findings_reports")
        reports_count = cursor.fetchone()[0]
        print(f"Reports created: {reports_count}")

        cursor.execute("SELECT COUNT(*) FROM key_findings_history")
        history_count = cursor.fetchone()[0]
        print(f"History entries: {history_count}")

        cursor.execute("SELECT tool_name, selected_sources, language FROM key_findings_reports")
        records = cursor.fetchall()
        for i, (tool, sources, lang) in enumerate(records, 1):
            sources_list = json.loads(sources)
            print(f"  {i}. {tool} | {len(sources_list)} sources | {lang}")

    except Exception as e:
        print(f"❌ Error populating test data: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    populate_test_data()

    print("\\n" + "="*60)
    print("✅ Test data population complete!")
    print("="*60)
    print("Database now contains:")
    print("• 1 Single Source Analysis (Google Trends only)")
    print("• 1 Multi-Source Analysis (5 sources)")
    print("• Complete history tracking")
    print("• Cache statistics")
    print("Ready for UI testing!")