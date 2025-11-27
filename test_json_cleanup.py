#!/usr/bin/env python3
"""
Test script to verify JSON cleanup functionality
"""
import sys
import os
import re

# Add the dashboard_app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def test_json_cleanup():
    """Test JSON cleanup functionality with sample problematic text"""

    print("🧪 TESTING JSON CLEANUP FUNCTIONALITY")
    print("=" * 50)

    # Sample text with embedded JSON (better matching real debug output)
    test_text = """📋 RESUMEN EJECUTIVO ```json { "executive_summary": "El análisis temporal de Google Trends para el término Alianzas y Capital de Riesgo revela patrones interesantes en el interés público a lo largo del tiempo." }

🔍 HALLAZGOS PRINCIPALES ```json { "key_findings": "Se observa un crecimiento sostenido en el interés público" }

• Hallazgo importante 1: El interés ha aumentado
• Hallazgo importante 2: Hay patrones estacionales

🔍 ANÁLISIS TEMPORAL
El análisis temporal muestra la evolución del interés.

📅 PATRONES ESTACIONALES
Se observan patrones estacionales claros en los datos.

🌊 ANÁLISIS ESPECTRAL
El análisis espectral revela componentes cíclicos.

🎯 SÍNTESIS ESTRATÉGICA
Los hallazgos sugieren oportunidades estratégicas.

📝 CONCLUSIONES
Las conclusiones se basan en el análisis completo."""

    print("🔍 ORIGINAL TEXT:")
    print("-" * 30)
    print(test_text[:300] + "..." if len(test_text) > 300 else test_text)
    print()

    # Apply the same cleanup logic as in format_text_with_styling (improved version)
    cleaned_text = test_text

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
    # More precise pattern that doesn't cross line boundaries aggressively
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

    print("🔍 CLEANED TEXT:")
    print("-" * 30)
    print(cleaned_text[:500] + "..." if len(cleaned_text) > 500 else cleaned_text)
    print()

    # Debug: Let's see exactly what's around the missing section
    print("🔍 DEBUG - Looking for HALLAZGOS PRINCIPALES:")
    print("-" * 30)
    if '🔍 HALLAZGOS PRINCIPALES' in cleaned_text:
        print("✅ Found exact header")
    else:
        print("❌ Header not found. Checking parts...")
        if '🔍' in cleaned_text:
            print("✅ Has 🔍 emoji")
        if 'HALLAZGOS' in cleaned_text:
            print("✅ Has HALLAZGOS text")
        if 'PRINCIPALES' in cleaned_text:
            print("✅ Has PRINCIPALES text")
    print()

    # Count sections to see if we can detect them properly now (all 7 expected sections)
    section_headers = [
        '📋 RESUMEN EJECUTIVO',
        '🔍 HALLAZGOS PRINCIPALES',
        '🔍 ANÁLISIS TEMPORAL',
        '📅 PATRONES ESTACIONALES',
        '🌊 ANÁLISIS ESPECTRAL',
        '🎯 SÍNTESIS ESTRATÉGICA',
        '📝 CONCLUSIONES'
    ]

    print("🔍 SECTION DETECTION:")
    print("-" * 30)

    found_sections = []
    for header in section_headers:
        if header in cleaned_text:
            found_sections.append(header)
            print(f"✅ Found: {header}")
        else:
            print(f"❌ Missing: {header}")

    print(f"\n🔍 SUMMARY:")
    print(f"Found sections: {len(found_sections)}/{len(section_headers)}")

    if len(found_sections) >= 6:  # We expect at least 6-7 sections now
        print("✅ JSON cleanup appears to be working - sections are detectable!")
    else:
        print("❌ JSON cleanup needs more work - sections still not detectable")

    print(f"\n🔍 BULLET POINT TEST:")
    if '• Hallazgo importante 1' in cleaned_text:
        print("✅ Bullet points preserved after cleanup")
    else:
        print("❌ Bullet points were affected by cleanup")

if __name__ == "__main__":
    test_json_cleanup()