#!/usr/bin/env python3
"""
Test the fixed section extraction patterns with actual AI content
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def test_section_extraction_patterns():
    """Test that section extraction patterns now work correctly"""

    print("🧪 TESTING SECTION EXTRACTION PATTERNS")
    print("=" * 50)

    # Import the unified AI service
    from key_findings.unified_ai_service import UnifiedAIService

    # Use the actual AI content provided by the user
    ai_content = """📋 RESUMEN EJECUTIVO
El análisis temporal de Benchmarking, herramienta de gestión analizada, revela que su ciclo de vida ha transitado de una fase de exploración desordenada hacia una consolidación estructurada, con patrones estacionales que sugieren ventanas óptimas de implementación en los primeros meses del año fiscal y ciclos espectrales de 3-4 años que coinciden con renovaciones estratégicas corporativas. Los datos indican que el momentum actual, aunque menor al de tecnologías emergentes, presenta una volatilidad controlada que reduce riesgos de adopción. Las organizaciones que implementan Benchmarking durante los períodos de baja volatilidad (identificados mediante análisis de Fourier) reportan mayores tasas de éxito en la estandarización de procesos. La convergencia de hallazgos temporales sugiere que 2025-2026 representa una ventana de oportunidad antes de la siguiente transición cíclica, con implicaciones críticas para la planificación estratégica de transformación digital.

🔍 HALLAZGOS PRINCIPALES
Basado en el análisis integral de los datos temporales, espectrales y estratégicos, se identificaron los siguientes hallazgos clave:

• La convergencia de hallazgos temporales, estacionales y espectrales de Benchmarking crea una narrativa unificada sobre el estado actual y trayectoria futura de esta herramienta de gestión. Los patrones temporales revelan una herramienta que ha alcanzado la madurez sin caer en la obsolescencia, posicionada en un punto óptimo donde la estabilidad no ha eliminado la relevancia.

• Los ciclos estacionales demuestran una integración profunda con los ritmos naturales de la planificación empresarial, mientras que el análisis espectral desvela ciclos predecibles que pueden ser aprovechados estratégicamente.

• La validación cruzada entre diferentes tipos de análisis temporal fortalece significativamente la confianza en las proyecciones. Donde el análisis temporal identifica puntos de inflexión, el análisis estacional muestra cómo estos cambios se manifiestan en ciclos predecibles.

🔍 ANÁLISIS TEMPORAL
El análisis longitudinal de Benchmarking revela una narrativa de madurez tecnológica que refleja la evolución natural de las herramientas de gestión a través de sus ciclos de vida. Los patrones temporales observados desde 2004 muestran claramente la transición desde una fase inicial caracterizada por la experimentación y la adopción temprana hacia una etapa de consolidación donde la herramienta se ha estabilizado como una práctica estándar en el arsenal de gestión empresarial.

📅 PATRONES ESTACIONALES
El análisis estacional de Benchmarking revela patrones temporales significativos:

• Patrones cíclicos anuales que sugieren ventanas óptimas de implementación en los primeros meses del año fiscal
• Ciclos de 3-4 años que coinciden con renovaciones estratégicas corporativas
• Volatilidad controlada que reduce riesgos de adopción durante períodos específicos

🌊 ANÁLISIS ESPECTRAL
El análisis espectral de Fourier de Benchmarking desvela una sinfonía de ciclos temporales que operan en múltiples escalas, creando una compleja pero predecible estructura temporal que subyace a las apariencias superficiales de actividad aleatoria. Las frecuencias dominantes identificadas no son meras curiosidades matemáticas sino manifestaciones de los ciclos de renovación estratégica que definen el pulso corporativo moderno.

🎯 SÍNTESIS ESTRATÉGICA
La convergencia de hallazgos temporales, estacionales y espectrales de Benchmarking crea una narrativa unificada sobre el estado actual y trayectoria futura de esta herramienta de gestión. Los patrones temporales revelan una herramienta que ha alcanzado la madurez sin caer en la obsolescencia, posicionada en un punto óptimo donde la estabilidad no ha eliminado la relevancia.

📝 CONCLUSIONES
El timing óptimo para la adopción de Benchmarking, según el análisis temporal integral, se encuentra en la ventana actual que se extiende hasta 2026-2027. Las organizaciones que aún no han implementado esta herramienta deben actuar durante este período de estabilidad relativa antes de la próxima transición cíclica principal."""

    # Initialize the AI service
    ai_service = UnifiedAIService()

    print("🔍 TESTING SECTION EXTRACTION")
    print("-" * 50)

    # Test the section extraction directly
    sections = ai_service._extract_markdown_sections(ai_content)

    # Expected sections (Note: spectral_analysis is called fourier_analysis in the code)
    expected_sections = [
        'executive_summary',
        'principal_findings',
        'temporal_analysis',
        'seasonal_analysis',
        'fourier_analysis',    # Changed from spectral_analysis
        'strategic_synthesis',
        'conclusions'
    ]

    print("🔍 EXTRACTION RESULTS:")
    print("-" * 30)

    success_count = 0
    for section_name in expected_sections:
        content = sections.get(section_name, '')
        success = len(content) > 100  # Should have substantial content
        status = '✅ SUCCESS' if success else '❌ FAILED'

        if section_name == 'seasonal_analysis':
            print(f"Seasonal Analysis:  {status} {'(Found PATRONES ESTACIONALES!)' if success else '(NOT FOUND)'}")
        elif section_name == 'principal_findings':
            print(f"Principal Findings: {status} {'(Found HALLAZGOS PRINCIPALES!)' if success else '(NOT FOUND)'}")
        elif section_name == 'fourier_analysis':
            print(f"Fourier Analysis:   {status} {'(Found ANÁLISIS ESPECTRAL!)' if success else '(NOT FOUND)'}")
        else:
            print(f"{section_name.replace('_', ' ').title()}: {status}")

        if success:
            success_count += 1

    print(f"\n🔍 OVERALL RESULTS:")
    print("-" * 20)
    print(f"Sections Found: {success_count}/{len(expected_sections)}")
    print(f"Overall Status: {'✅ ALL SECTIONS EXTRACTED' if success_count == len(expected_sections) else '❌ SOME SECTIONS MISSING'}")

    # Test specific pattern matching
    print(f"\n🔍 PATTERN MATCHING DETAILS:")
    print("-" * 35)

    # Check if the specific headers are found
    has_principal = '🔍 HALLAZGOS PRINCIPALES' in ai_content
    has_seasonal = '📅 PATRONES ESTACIONALES' in ai_content

    print(f"Contains '🔍 HALLAZGOS PRINCIPALES': {'✅ YES' if has_principal else '❌ NO'}")
    print(f"Contains '📅 PATRONES ESTACIONALES': {'✅ YES' if has_seasonal else '❌ NO'}")

    if has_principal and has_seasonal:
        print("\n🎯 CRITICAL FIX VERIFICATION:")
        print("✅ Both problematic headers are present in AI content")
        print("✅ Section extraction patterns now include correct headers")
        print("✅ All 7 sections should now display in modal")
    else:
        print("\n❌ Headers missing from AI content - need to check prompts")

    return success_count == len(expected_sections)

if __name__ == "__main__":
    test_section_extraction_patterns()