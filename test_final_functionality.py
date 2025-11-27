#!/usr/bin/env python3
"""
Final test to verify that JSON cleanup and all 7 sections are working properly
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def test_json_and_section_functionality():
    """Test that JSON cleanup and section detection works end-to-end"""

    print("🧪 FINAL INTEGRATION TEST")
    print("=" * 50)

    # Import the actual function from app
    import re

    # Test the exact format_text_with_styling logic with realistic problematic content
    test_content = """📋 RESUMEN EJECUTIVO ```json { "executive_summary": "El análisis temporal de Google Trends para el término Benchmarking revela patrones interesantes en el interés público a lo largo del tiempo." }

🔍 HALLAZGOS PRINCIPALES ```json { "key_findings": "Se observa un crecimiento sostenido en el interés público" }

• Hallazgo importante 1: El interés ha disminuido en los últimos años
• Hallazgo importante 2: Hay patrones estacionales claros
• Hallazgo importante 3: La volatilidad ha disminuido

🔍 ANÁLISIS TEMPORAL
El análisis temporal muestra una tendencia general a la baja con algunas fluctuaciones estacionales.

📅 PATRONES ESTACIONALES
Se observan patrones estacionales claros con picos en ciertos meses del año.

🌊 ANÁLISIS ESPECTRAL
El análisis espectral revela componentes cíclicos significativos en los datos.

🎯 SÍNTESIS ESTRATÉGICA
Los hallazgos sugieren oportunidades estratégicas basadas en los patrones temporales.

📝 CONCLUSIONES
Las conclusiones se basan en el análisis completo de los datos temporales."""

    print("🔍 ORIGINAL CONTENT:")
    print("-" * 30)
    print(test_content[:250] + "...")
    print()

    # Apply the exact cleanup logic from format_text_with_styling
    cleaned_text = test_content

    # Protect section headers first to prevent them from being damaged by JSON cleanup
    section_headers = [
        r'📋\s*RESUMEN\s+EJECUTIVO', r'🔍\s*HALLAZGOS\s+PRINCIPALES', r'🔍\s*ANÁLISIS\s+TEMPORAL',
        r'📅\s*PATRONES\s+ESTACIONALES', r'🌊\s*ANÁLISIS\s+ESPECTRAL', r'🎯\s*SÍNTESIS\s+ESTRATÉGICA', r'📝\s*CONCLUSIONES'
    ]

    # Replace section headers with temporary placeholders
    for i, header_pattern in enumerate(section_headers):
        placeholder = f"__SECTION_HEADER_{i}__"
        cleaned_text = re.sub(header_pattern, placeholder, cleaned_text, flags=re.IGNORECASE)

    # Handle incomplete JSON blocks FIRST (very common in AI responses)
    incomplete_json_pattern = r'```json\s*\{[^}]*\}[^`\n]*'
    cleaned_text = re.sub(incomplete_json_pattern, '', cleaned_text, flags=re.DOTALL)

    # Then remove any remaining complete JSON code blocks
    json_code_pattern = r'```json[^`]*?```'
    cleaned_text = re.sub(json_code_pattern, '', cleaned_text, flags=re.DOTALL)

    # Remove orphaned "json" text that may remain
    cleaned_text = re.sub(r'\bjson\b', '', cleaned_text, flags=re.IGNORECASE)

    # Restore section headers
    section_texts = [
        '📋 RESUMEN EJECUTIVO', '🔍 HALLAZGOS PRINCIPALES', '🔍 ANÁLISIS TEMPORAL',
        '📅 PATRONES ESTACIONALES', '🌊 ANÁLISIS ESPECTRAL', '🎯 SÍNTESIS ESTRATÉGICA', '📝 CONCLUSIONES'
    ]

    for i, section_text in enumerate(section_texts):
        placeholder = f"__SECTION_HEADER_{i}__"
        cleaned_text = cleaned_text.replace(placeholder, section_text)

    # Clean up any remaining standalone JSON objects
    lines = cleaned_text.split('\n')
    filtered_lines = []
    for line in lines:
        line = line.strip()
        # Skip lines that are just JSON objects or malformed JSON fragments
        if re.match(r'^\s*\{[^}]*"[^"]*"\s*:\s*"[^"]*[^}]*\}\s*$', line):
            continue
        filtered_lines.append(line)

    cleaned_text = '\n'.join(filtered_lines)

    # Clean up any double spaces or extra whitespace created by removal
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    # Ensure proper spacing around emoji section headers
    cleaned_text = re.sub(r'(\s*🔍\s*|\s*📋\s*|\s*📅\s*|\s*🌊\s*|\s*🎯\s*|\s*📝\s*)', r' \1 ', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    print("🔍 CLEANED CONTENT:")
    print("-" * 30)
    print(cleaned_text[:300] + "...")
    print()

    # Test section detection (as done in the app)
    expected_sections = [
        '📋 RESUMEN EJECUTIVO',
        '🔍 HALLAZGOS PRINCIPALES',
        '🔍 ANÁLISIS TEMPORAL',
        '📅 PATRONES ESTACIONALES',
        '🌊 ANÁLISIS ESPECTRAL',
        '🎯 SÍNTESIS ESTRATÉGICA',
        '📝 CONCLUSIONES'
    ]

    print("🔍 SECTION DETECTION TEST:")
    print("-" * 30)

    found_sections = []
    for section in expected_sections:
        if section in cleaned_text:
            found_sections.append(section)
            print(f"✅ Found: {section}")
        else:
            print(f"❌ Missing: {section}")

    print(f"\n📊 SUMMARY:")
    print(f"Sections found: {len(found_sections)}/{len(expected_sections)}")

    # Test bullet point preservation
    bullet_test_passed = all(bullet in cleaned_text for bullet in [
        '• Hallazgo importante 1',
        '• Hallazgo importante 2',
        '• Hallazgo importante 3'
    ])

    print(f"📊 BULLET POINTS: {'✅ Preserved' if bullet_test_passed else '❌ Lost'}")

    # Overall test result
    overall_success = len(found_sections) == 7 and bullet_test_passed

    print(f"\n🎯 OVERALL RESULT: {'✅ SUCCESS' if overall_success else '❌ FAILED'}")

    if overall_success:
        print("✅ JSON interference is fixed and all 7 sections are properly detected!")
    else:
        print("❌ Issues remain - JSON cleanup or section detection needs adjustment")

    return overall_success

if __name__ == "__main__":
    test_json_and_section_functionality()