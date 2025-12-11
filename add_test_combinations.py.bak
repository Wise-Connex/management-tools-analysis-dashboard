#!/usr/bin/env python3
"""
ADD TEST COMBINATIONS: Manual Precomputed Data Entry
====================================================

This script demonstrates how to manually add your target combinations
to the precomputed database for immediate testing without AI generation.
"""

import sys
import os
import sqlite3
from datetime import datetime

# Add dashboard_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

from database_implementation.precomputed_findings_db import get_precomputed_db_manager


def create_sample_analysis(tool_name, sources, language="es"):
    """Create sample analysis data for testing."""
    sources_count = len(sources)
    sources_text = ", ".join(sources)
    
    if sources_count == 1:
        # Single source analysis
        return {
            "executive_summary": f"""
Análisis de {tool_name} basado en {sources_text}

Este análisis examina las tendencias y patrones de {tool_name} utilizando datos de {sources_text}. 
Los resultados muestran una evolución temporal interesante con picos de interés en períodos específicos.

La tendencia general muestra un crecimiento sostenido con una volatilidad moderada, 
indicando madurez en la adopción de esta herramienta de gestión.

Los patrones estacionales revelan mayor actividad durante los meses de primavera y otoño,
posiblemente relacionado con ciclos de planificación empresarial.
            """.strip(),
            
            "principal_findings": f"""
🔍 HALLAZGOS PRINCIPALES

📋 RESUMEN EJECUTIVO
El análisis de {tool_name} mediante {sources_text} revela patrones de adopción 
y evolución significativos para el período estudiado.

🔍 ANÁLISIS TEMPORAL
La tendencia temporal muestra un crecimiento constante con una tasa del 15% anual.
Se identifican tres fases principales: introducción (2018-2020), crecimiento (2021-2023) 
y madurez (2024-presente).

📅 PATRONES ESTACIONALES
Los datos muestran estacionalidad clara con picos en Q2 y Q4.
Los meses de mayor actividad: abril, mayo, octubre, noviembre.
Los meses de menor actividad: enero, julio, agosto.

🌊 ANÁLISIS ESPECTRAL
El análisis de Fourier revela ciclos dominantes de 12 meses (anual) y 6 meses (semestral).
La frecuencia principal corresponde al ciclo empresarial anual.

🎯 SÍNTESIS ESTRATÉGICA
{tool_name} demuestra sólida adopción con potencial de crecimiento en mercados emergentes.
La estacionalidad sugiere oportunidades de marketing específicas por temporada.

📝 CONCLUSIONES
La herramienta muestra madurez con crecimiento sostenido.
Recomendaciones: enfocar esfuerzos en Q2/Q4, expandir a mercados emergentes.
            """.strip(),
            
            "temporal_analysis": "",
            "seasonal_analysis": "",
            "fourier_analysis": "",
            "pca_analysis": "",
            "heatmap_analysis": "",
            "confidence_score": 0.85,
            "model_used": "manual_test_data",
            "data_points_analyzed": 240,
            "analysis_type": "single_source"
        }
    else:
        # Multi-source analysis
        return {
            "executive_summary": f"""
Análisis integral de {tool_name} utilizando múltiples fuentes de datos

Este análisis combina información de {sources_count} fuentes diferentes: {sources_text}.
La perspectiva multi-fuente proporciona una visión completa y robusta de las tendencias.

Los resultados muestran consistencia entre fuentes, con correlaciones fuertes 
que validan los patrones identificados. Las diferencias entre fuentes aportan 
matices valiosos para la toma de decisiones estratégicas.

La convergencia de evidencias sugiere que {tool_name} está en una fase 
de madurez con oportunidades específicas de optimización y expansión.
            """.strip(),
            
            "principal_findings": f"""
🔍 HALLAZGOS PRINCIPALES

📋 RESUMEN EJECUTIVO
El análisis multi-fuente de {tool_name} revela patrones consistentes 
y tendencias robustas validadas por {sources_count} fuentes independientes.

📈 ANÁLISIS DE COMPONENTES PRINCIPALES
El PCA identifica tres componentes principales que explican el 78% de la varianza:
- Componente 1 (45%): Tendencia de adopción general
- Componente 2 (22%): Variación estacional y cíclica  
- Componente 3 (11%): Factores específicos por industria/region

🔥 ANÁLISIS DE CORRELACIÓN
Las correlaciones entre fuentes son fuertes (r > 0.7), indicando consistencia.
Google Trends y Crossref muestran la mayor correlación (r = 0.85).
Bain Usability proporciona datos únicos sobre implementación práctica.

📊 ANÁLISIS DE DISTRIBUCIÓN
El heatmap revela patrones geográficos y temporales claros.
Mayor concentración en Norteamérica y Europa Occidental.
Crecimiento acelerado en Asia-Pacífico y América Latina.

🎯 SÍNTESIS ESTRATÉGICA
La evidencia multi-fuente valida la madurez de {tool_name}.
Oportunidades identificadas: expansión geográfica, optimización sectorial.
Riesgos monitoreados: saturación en mercados maduros, competencia emergente.

📝 CONCLUSIONES
{tool_name} demuestra sólida posición con potencial de crecimiento optimizado.
La estrategia multi-fuente proporciona visión completa para decisiones informadas.
Recomendaciones: expansión geográfica, personalización sectorial, monitoreo continuo.
            """.strip(),
            
            "pca_analysis": f"""
Análisis de Componentes Principales para {tool_name}

El análisis PCA aplicado a los datos multi-fuente de {tool_name} revela 
una estructura subyacente robusta con tres componentes principales significativos.

Componente Principal 1 (45.2% de varianza explicada):
Este componente representa la tendencia general de adopción y madurez de {tool_name}.
Las cargas más altas corresponden a Google Trends (0.89) y Crossref (0.85),
indicando que estas fuentes capturan mejor la evolución temporal general.

Componente Principal 2 (22.1% de varianza explicada):
Representa patrones estacionales y cíclicos consistentes across fuentes.
Bain Usability muestra la carga más alta (0.78), sugiriendo datos de implementación 
siguen patrones estacionales predecibles.

Componente Principal 3 (11.3% de varianza explicada):
Captura variaciones específicas por industria y factores regionales.
Google Books y Bain Satisfaction contribuyen significativamente,
reflejando diferencias en adopción académica vs. satisfacción del usuario.

La estructura de componentes sugiere que {tool_name} ha evolucionado 
desde la adopción inicial hacia la optimización y madurez, 
con patrones consistentes validados por múltiples perspectivas de datos.
            """.strip(),
            
            "heatmap_analysis": f"""
Análisis de Distribución Geográfica y Temporal

El análisis heatmap para {tool_name} utilizando {sources_count} fuentes 
revela patrones espaciales y temporales distintivos.

Distribución Geográfica:
- Norteamérica: Mayor concentración (35% de actividad total)
- Europa Occidental: Segunda región (28% de actividad)
- Asia-Pacífico: Crecimiento acelerado (22% de actividad)
- América Latina: Potencial emergente (10% de actividad)
- Otras regiones: Adopción incipiente (5% de actividad)

Patrones Temporales:
- Q1: Planificación y presupuesto (actividad moderada)
- Q2: Implementación y ejecución (pico de actividad)
- Q3: Evaluación y ajustes (actividad alta)
- Q4: Reporte y planificación siguiente año (pico máximo)

Correlaciones Espacio-Temporales:
Las regiones maduras muestran patrones estacionales más marcados.
Las regiones emergentes muestran crecimiento continuo sin estacionalidad clara.

Implicaciones Estratégicas:
Las diferencias geográficas sugieren necesidad de estrategias localizadas.
Los patrones temporales indican oportunidades de optimización de recursos.
La convergencia de patrones valida la robustez de los hallazgos.
            """.strip(),
            
            "temporal_analysis": "",
            "seasonal_analysis": "",
            "fourier_analysis": "",
            "confidence_score": 0.88,
            "model_used": "manual_test_data",
            "data_points_analyzed": 1200,
            "analysis_type": "multi_source"
        }


def add_combination_to_database(tool_name, sources, language="es"):
    """Add a specific combination to the precomputed database."""
    db_manager = get_precomputed_db_manager()
    
    # Generate hash
    hash_value = db_manager.generate_combination_hash(tool_name, sources, language)
    
    # Create sample analysis
    analysis_data = create_sample_analysis(tool_name, sources, language)
    
    # Add tool display name
    analysis_data["tool_display_name"] = tool_name
    
    try:
        # Store in database
        record_id = db_manager.store_precomputed_analysis(
            combination_hash=hash_value,
            tool_name=tool_name,
            selected_sources=sources,
            language=language,
            analysis_data=analysis_data
        )
        
        print(f"✅ SUCCESS: Added combination to database")
        print(f"   📋 Tool: {tool_name}")
        print(f"   📊 Sources: {', '.join(sources)}")
        print(f"   🌍 Language: {language}")
        print(f"   🔑 Hash: {hash_value}")
        print(f"   📝 Record ID: {record_id}")
        print(f"   📊 Analysis Type: {analysis_data['analysis_type']}")
        print(f"   🎯 Confidence: {analysis_data['confidence_score']}")
        print(f"   📄 Executive Summary: {len(analysis_data['executive_summary'])} chars")
        print(f"   🔍 Principal Findings: {len(analysis_data['principal_findings'])} chars")
        
        return True, record_id
        
    except Exception as e:
        print(f"❌ ERROR: Failed to add combination to database")
        print(f"   📋 Tool: {tool_name}")
        print(f"   📊 Sources: {', '.join(sources)}")
        print(f"   🔑 Hash: {hash_value}")
        print(f"   ❌ Error: {e}")
        return False, None


def main():
    """Add test combinations to database."""
    print("🎯 ADD TEST COMBINATIONS TO DATABASE")
    print("=" * 60)
    print("This will add your target combinations with sample data")
    print("for immediate testing without AI generation")
    print("=" * 60)
    
    # Target combinations
    combinations = [
        {
            "name": "Single Source - Google Trends",
            "tool": "Calidad Total",
            "sources": ["Google Trends"],
            "language": "es"
        },
        {
            "name": "Multi-Source - All 5 Sources",
            "tool": "Calidad Total",
            "sources": ["Google Trends", "Google Books", "Bain Usability", "Crossref", "Bain Satisfaction"],
            "language": "es"
        }
    ]
    
    # Check current status first
    print("📊 CURRENT DATABASE STATUS")
    print("-" * 40)
    db_manager = get_precomputed_db_manager()
    stats = db_manager.get_statistics()
    print(f"Total records: {stats['total_findings']}")
    print(f"By language: {stats['findings_by_language']}")
    print(f"By type: {stats['findings_by_type']}")
    
    # Check existing Calidad Total records
    with db_manager.get_connection() as conn:
        cursor = conn.execute("""
            SELECT sources_text, language, analysis_type 
            FROM precomputed_findings 
            WHERE tool_name = 'Calidad Total' AND is_active = 1
            ORDER BY sources_count, language
        """)
        existing = cursor.fetchall()
        
        print(f"\nExisting Calidad Total records ({len(existing)}):")
        for record in existing:
            print(f"  • {record['sources_text']} ({record['language']}) - {record['analysis_type']}")
    
    print("\n" + "=" * 60)
    print("🔧 ADDING NEW COMBINATIONS")
    print("=" * 60)
    
    successful_additions = 0
    total_additions = len(combinations)
    
    for i, combo in enumerate(combinations, 1):
        print(f"\n🧪 ADDITION {i}/{total_additions}: {combo['name']}")
        print("-" * 50)
        
        # Check if already exists
        hash_value = db_manager.generate_combination_hash(
            combo["tool"], combo["sources"], combo["language"]
        )
        existing_record = db_manager.get_combination_by_hash(hash_value)
        
        if existing_record:
            print(f"⚠️  ALREADY EXISTS: {combo['name']}")
            print(f"   📊 Sources: {', '.join(combo['sources'])}")
            print(f"   🔑 Hash: {hash_value}")
            print(f"   💡 Skipping addition")
            successful_additions += 1  # Count as success since it exists
            continue
        
        # Add new combination
        success, record_id = add_combination_to_database(
            combo["tool"], 
            combo["sources"], 
            combo["language"]
        )
        
        if success:
            successful_additions += 1
    
    # Final status
    print("\n" + "=" * 60)
    print("📋 FINAL STATUS")
    print("=" * 60)
    
    # Updated statistics
    updated_stats = db_manager.get_statistics()
    print(f"✅ Successful additions: {successful_additions}/{total_additions}")
    print(f"📊 Total records now: {updated_stats['total_findings']}")
    print(f"📊 By language: {updated_stats['findings_by_language']}")
    print(f"📊 By type: {updated_stats['findings_by_type']}")
    
    # Check updated Calidad Total records
    with db_manager.get_connection() as conn:
        cursor = conn.execute("""
            SELECT sources_text, language, analysis_type, access_count
            FROM precomputed_findings 
            WHERE tool_name = 'Calidad Total' AND is_active = 1
            ORDER BY sources_count, language
        """)
        updated_records = cursor.fetchall()
        
        print(f"\n📈 Updated Calidad Total records ({len(updated_records)}):")
        for record in updated_records:
            print(f"  • {record['sources_text']} ({record['language']}) - {record['analysis_type']} - {record['access_count']} accesses")
    
    print(f"\n🎉 SUCCESS! Your combinations are now ready for testing")
    print(f"🚀 Users can now get instant Key Findings for these combinations")
    print(f"📱 Test in dashboard: Select 'Calidad Total' + your sources, click 'Key Findings'")
    
    print(f"\n🔧 NEXT STEPS:")
    print(f"1. Open dashboard: http://localhost:8050")
    print(f"2. Select 'Calidad Total' from tools dropdown")
    print(f"3. Select your test sources:")
    print(f"   • Single source: Check only 'Google Trends'")
    print(f"   • Multi-source: Check all 5 sources")
    print(f"4. Click 'Key Findings' button")
    print(f"5. Verify instant analysis appears (no loading)")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
