#!/usr/bin/env python3
"""
Debug the actual AI response content to see what headers are being generated
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def debug_ai_response():
    """Debug what the AI actually generates and test section extraction"""

    print("🔍 DEBUGGING AI RESPONSE AND SECTION EXTRACTION")
    print("=" * 60)

    # Import the unified AI service
    from key_findings.unified_ai_service import UnifiedAIService

    # Initialize the AI service
    ai_service = UnifiedAIService()

    # Sample content that simulates what AI should generate
    test_content = """📋 RESUMEN EJECUTIVO
El análisis longitudinal de Benchmarking revela patrones temporales significativos...

🔍 HALLAZGOS PRINCIPALES
Basado en el análisis integral de los datos temporales, espectrales y estratégicos, se identificaron los siguientes hallazgos clave:

• La convergencia de hallazgos temporales, estacionales y espectrales de Benchmarking crea una narrativa unificada...

🔍 ANÁLISIS TEMPORAL
El análisis longitudinal de Benchmarking revela una narrativa de madurez tecnológica...

📅 PATRONES ESTACIONALES
El análisis estacional de Benchmarking revela patrones temporales significativos:

• Patrones cíclicos anuales que sugieren ventanas óptimas de implementación...

🌊 ANÁLISIS ESPECTRAL
El análisis espectral de Fourier de Benchmarking desvela una sinfonía de ciclos temporales...

🎯 SÍNTESIS ESTRATÉGICA
La convergencia de hallazgos temporales, estacionales y espectrales de Benchmarking...

📝 CONCLUSIONES
El timing óptimo para la adopción de Benchmarking, según el análisis temporal integral..."""

    print("🔍 TESTING SECTION EXTRACTION WITH SAMPLE CONTENT")
    print("-" * 50)

    # Test the section extraction
    sections = ai_service._extract_markdown_sections(test_content)

    expected_sections = [
        'executive_summary',
        'principal_findings',
        'temporal_analysis',
        'seasonal_analysis',
        'fourier_analysis',
        'strategic_synthesis',
        'conclusions'
    ]

    print(f"🔍 SECTIONS FOUND: {list(sections.keys())}")
    print(f"🔍 EXPECTED: {expected_sections}")
    print()

    success_count = 0
    for section_name in expected_sections:
        content = sections.get(section_name, '')
        has_content = len(content) > 50  # Should have substantial content
        status = '✅ FOUND' if has_content else '❌ MISSING'

        print(f"{section_name.replace('_', ' ').title()}: {status}")
        if has_content:
            success_count += 1
            # Show first 50 characters of content
            content_preview = content[:50].replace('\n', ' ')
            print(f"  Preview: {content_preview}...")

    print()
    print(f"🔍 RESULTS: {success_count}/{len(expected_sections)} sections found")

    if success_count == len(expected_sections):
        print("🎉 SUCCESS: All 7 sections extracted correctly!")
    else:
        print("❌ FAILURE: Some sections missing from extraction")
        missing = [s for s in expected_sections if s not in sections or len(sections[s]) <= 50]
        print(f"🔍 Missing sections: {missing}")

    return success_count == len(expected_sections)

if __name__ == "__main__":
    debug_ai_response()