#!/usr/bin/env python3
"""
Compare AI response content with what's displayed in the modal to find the missing sections
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def debug_ai_vs_modal():
    """Debug the difference between AI response and modal display"""

    print("🔍 DEBUGGING: AI Response vs Modal Display")
    print("=" * 60)

    # Sample AI response that matches what we see in the logs
    ai_response_content = """📋 RESUMEN EJECUTIVO
El análisis temporal integral de la herramienta de gestión Benchmarking, abarcando casi dos décadas desde 2004, revela una evolución madura con patrones cíclicos predecibles que ofrecen oportunidades estratégicas de timing para su adopción empresarial.

🔍 HALLAZGOS PRINCIPALES
Basado en el análisis integral de los datos temporales, espectrales y estratégicos, se identificaron los siguientes hallazgos clave:
• La convergencia de hallazgos temporales, estacionales y espectrales de Benchmarking crea una narrativa unificada sobre el estado actual y trayectoria futura.

🔍 ANÁLISIS TEMPORAL
El análisis temporal de Benchmarking revela una narrativa de evolución y madurez que refleja el viaje de esta herramienta desde una práctica nicho hasta una disciplina de gestión ampliamente aceptada.

📅 PATRONES ESTACIONALES
El análisis estacional de Benchmarking revela patrones temporales significativos:
• Patrones cíclicos anuales que sugieren ventanas óptimas de implementación en los primeros meses del año fiscal.

🌊 ANÁLISIS ESPECTRAL
El análisis espectral de Fourier desvela la arquitectura oculta de ciclos dentro de la adopción de Benchmarking, identificando frecuencias dominantes que operan en múltiples escalas temporales.

🎯 SÍNTESIS ESTRATÉGICA
La convergencia de hallazgos temporales, estacionales y espectrales crea una narrativa cohesiva sobre el estado actual y trayectoria futura de Benchmarking.

📝 CONCLUSIONES
El análisis temporal integral de Benchmarking concluye que esta herramienta de gestión ha alcanzado un estado de madurez que ofrece oportunidades únicas de timing estratégico."""

    print("🔍 TESTING: AI Response Content")
    print("-" * 40)
    print("AI Response contains these headers:")
    headers = []
    for line in ai_response_content.split('\n'):
        if line.strip() and line.strip().startswith('📋') or line.strip().startswith('🔍') or line.strip().startswith('📅') or line.strip().startswith('🌊') or line.strip().startswith('🎯') or line.strip().startswith('📝'):
            headers.append(line.strip())
            print(f"  ✅ {line.strip()}")

    print(f"\nTotal headers in AI response: {len(headers)}")

    # Test section extraction
    print("\n" + "=" * 60)
    print("🔍 TESTING: Section Extraction")
    print("-" * 40)

    from key_findings.unified_ai_service import UnifiedAIService
    ai_service = UnifiedAIService()

    # Test the section extraction
    sections = ai_service._extract_markdown_sections(ai_response_content)

    print(f"Sections extracted: {list(sections.keys())}")

    expected_sections = [
        'executive_summary',
        'principal_findings',
        'temporal_analysis',
        'seasonal_analysis',
        'fourier_analysis',
        'strategic_synthesis',
        'conclusions'
    ]

    print("\nSection extraction results:")
    success_count = 0
    for section_name in expected_sections:
        content = sections.get(section_name, '')
        has_content = len(content) > 50
        status = '✅ FOUND' if has_content else '❌ MISSING'
        print(f"  {section_name.replace('_', ' ').title()}: {status}")
        if has_content:
            success_count += 1

    print(f"\nExtracted: {success_count}/{len(expected_sections)} sections")

    # Test the response parsing pipeline
    print("\n" + "=" * 60)
    print("🔍 TESTING: Full Response Parsing Pipeline")
    print("-" * 40)

    # Parse the response as the service does
    parsed_response = ai_service._parse_ai_response(ai_response_content, is_single_source=True)

    print(f"Parsed response keys: {list(parsed_response.keys())}")

    # Check which critical sections are present
    critical_sections = ['executive_summary', 'principal_findings', 'seasonal_analysis', 'temporal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']

    print("\nCritical sections in parsed response:")
    for section in critical_sections:
        value = parsed_response.get(section)
        if value and len(str(value)) > 50:
            print(f"  ✅ {section}: Present (length: {len(str(value))})")
        else:
            print(f"  ❌ {section}: Missing or Empty")

    print("\n" + "=" * 60)
    print("🔍 ROOT CAUSE ANALYSIS")
    print("-" * 40)

    if success_count == len(expected_sections):
        print("🎉 SUCCESS: All sections extracted correctly by _extract_markdown_sections")
        print("🔍 The issue is in the _parse_ai_response method")
        print("🔍 specifically in the _combine_section_responses mapping")
    else:
        print("❌ FAILURE: Section extraction is failing")
        print("🔍 The issue is in _extract_markdown_sections patterns")

    return success_count == len(expected_sections)

if __name__ == "__main__":
    debug_ai_vs_modal()