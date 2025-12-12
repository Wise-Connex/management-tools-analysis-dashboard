#!/usr/bin/env python3
"""
Simple script to store the recent Benchmarking analysis in the database
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def store_benchmarking_analysis():
    """Store the recent Benchmarking analysis directly in the database"""

    print("🗃️ SIMPLE BENCHMARKING ANALYSIS STORAGE")
    print("=" * 60)

    # Import the database manager
    from key_findings.database_manager import KeyFindingsDBManager
    import hashlib

    # Initialize the Key Findings database manager with local path
    print("🗃️ Initializing Key Findings database manager...")
    local_db_path = os.path.join(os.path.dirname(__file__), 'dashboard_app', 'data', 'key_findings.db')
    kf_db_manager = KeyFindingsDBManager(db_path=local_db_path)

    # Analysis data from the recent dashboard run (captured from logs)
    print("📊 Preparing analysis data from recent dashboard run...")

    tool_name = "Benchmarking"
    sources_text = "Google Trends"
    language = "es"

    # Use the AI-generated content we saw in the dashboard
    analysis_data = {
        'tool_name': tool_name,
        'selected_sources': [1],  # Google Trends ID
        'date_range_start': '2004-01-01',
        'date_range_end': '2023-12-01',
        'language': language,
        'executive_summary': "El análisis temporal de veinte años de la herramienta de gestión Benchmarking revela un ciclo de vida que ha transitado de fase exploratoria a madurez plena, con una volatilidad decreciente que indica consolidación del mercado. Los patrones estacionales muestran ventanas óptimas de implementación en períodos de planificación estratégica anual, mientras que el análisis espectral de Fourier identifica frecuencias dominantes de 3-4 años, coincidentes con ciclos de planificación estratégica corporativa. La convergencia de estos hallazgos sugiere que las organizaciones deben alinear la adopción de Benchmarking con sus ciclos de planificación estratégica, aprovechando los períodos de menor volatilidad para maximizar la probabilidad de éxito en la implementación. El timing óptimo se presenta en las transiciones entre ciclos de planificación, cuando la organización está naturalmente predispuesta a la evaluación y mejora continua.",
        'principal_findings': [
            "La convergencia de hallazgos temporales, estacionales y espectrales de Benchmarking crea una narrativa coherente sobre la evolución y estado actual de Benchmarking como herramienta de gestión. Los patrones temporales revelan una herramienta que ha alcanzado madurez, con ciclos de vida característicos que han pasado por las fases típicas de introducción, crecimiento y estabilización. Esta madurez temporal coincide con la institutionalización de la práctica, donde Benchmarking se ha transformado de una ventaja competitiva potencial a un estándar de industria esperado.",
            "🔍 HALLAZGOS PRINCIPALES\nBasado en el análisis integral de los datos temporales, espectrales y estratégicos, se identificaron los siguientes hallazgos clave:\n• La convergencia de hallazgos temporales, estacionales y espectrales de Benchmarking crea una narrativa unificada sobre el estado actual y trayectoria futura de esta herramienta de gestión."
        ],
        'temporal_analysis': "El análisis longitudinal de Benchmarking a lo largo de dos décadas revela una evolución característica de tecnologías y prácticas de gestión que transitan por fases de introducción, crecimiento, madurez y eventual estabilización. La trayectoria temporal muestra claramente cómo la herramienta ha experimentado una transformación desde una práctica novedosa y relativamente desconocida a una disciplina ampliamente aceptada y estandarizada en el arsenal de herramientas de gestión organizacional.",
        'seasonal_analysis': "📅 PATRONES ESTACIONALES\nEl análisis estacional de Benchmarking revela patrones temporales significativos:\n• Patrones cíclicos anuales que sugieren ventanas óptimas de implementación en los primeros meses del año fiscal\n• Ciclos de 3-4 años que coinciden con renovaciones estratégicas corporativas\n• Volatilidad controlada que reduce riesgos de adopción durante períodos específicos",
        'fourier_analysis': "🌊 ANÁLISIS ESPECTRAL\nEl análisis espectral de Fourier aplicado a la serie temporal de Benchmarking revela una estructura cíclica compleja que va más allá de los patrones estacionales simples, mostrando múltiples frecuencias dominantes que corresponden a diferentes tipos de ciclos organizacionales y de mercado. Las frecuencias dominantes identificadas proporcionan insights profundos sobre los ritmos naturales a los cuales las organizaciones tienden a adoptar, implementar y renovar sus prácticas de benchmarking.",
        'strategic_synthesis': "🎯 SÍNTESIS ESTRATÉGICA\nLa convergencia de hallazgos temporales, estacionales y espectrales crea una narrativa coherente sobre la evolución y estado actual de Benchmarking como herramienta de gestión. Los patrones temporales revelan una herramienta que ha alcanzado madurez, con ciclos de vida característicos que han pasado por las fases típicas de introducción, crecimiento y estabilización.",
        'conclusions': "📝 CONCLUSIONES\nEl análisis integral de patrones temporales, estacionales y espectrales de Benchmarking concluye que esta herramienta de gestión ha alcanzado un estado de madurez que ofrece tanto oportunidades como desafíos para las organizaciones contemporáneas. El timing óptimo para adopción o renovación de prácticas de Benchmarking está intrínsecamente ligado a los ciclos naturales de planificación estratégica organizacional.",
        'model_used': 'moonshotai/kimi-k2-instruct',
        'api_latency_ms': 16967,
        'confidence_score': 0.92,
        'data_points_analyzed': 240,
        'sources_count': 1,
        'analysis_depth': 'comprehensive',
        'report_type': 'single_source'
    }

    # Calculate the hash using the same method as the dashboard
    query_hash = kf_db_manager.generate_scenario_hash(
        tool_name=tool_name,
        selected_sources=[1],  # Google Trends ID
        language=language
    )

    print(f"🔑 Generated query hash: {query_hash}")

    # Store in the database using the correct method
    print("\n💾 Storing in precomputed findings database...")
    success = kf_db_manager.cache_report(scenario_hash=query_hash, report_data=analysis_data)

    if success:
        print("✅ Successfully stored in precomputed findings database")

        # Verify the storage
        print("\n🔍 Verifying storage...")
        stored_data = kf_db_manager.get_cached_report(scenario_hash=query_hash)

        if stored_data:
            print("✅ Successfully retrieved stored data")
            print(f"📊 Retrieved keys: {list(stored_data.keys())}")

            # Check section lengths
            sections = ['executive_summary', 'principal_findings', 'seasonal_analysis',
                       'temporal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']

            print("\n📊 Section analysis:")
            total_sections = 0
            for section in sections:
                content = stored_data.get(section, '')
                length = len(str(content)) if content else 0
                has_content = length > 50
                status = '✅' if has_content else '❌'
                print(f"  {status} {section}: {length} characters")
                if has_content:
                    total_sections += 1

            print(f"\n📊 Total sections with content: {total_sections}/7")

            if total_sections == 7:
                print("🎉 SUCCESS: All 7 sections stored and ready for dashboard retrieval!")
                print("\n📋 Next steps:")
                print("1. Go to the dashboard (http://localhost:8052)")
                print("2. Select 'Benchmarking' tool")
                print("3. Select 'Google Trends' source")
                print("4. Click 'Hallazgos Principales' button")
                print("5. The analysis should now load instantly from the database with all 7 sections!")
            else:
                print("⚠️ WARNING: Some sections may be missing content")

            return True
        else:
            print("❌ Failed to retrieve stored data")
            return False
    else:
        print("❌ Failed to store in database")
        return False

if __name__ == "__main__":
    result = store_benchmarking_analysis()
    if result:
        print("\n🎉 Operation completed successfully!")
    else:
        print("\n❌ Operation failed!")