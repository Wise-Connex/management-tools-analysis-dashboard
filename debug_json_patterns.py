#!/usr/bin/env python3
"""
Debug script to test JSON patterns step by step
"""
import re

def debug_json_patterns():
    """Debug JSON removal patterns step by step"""

    print("🔍 DEBUGGING JSON PATTERNS")
    print("=" * 40)

    # Simulate the problematic text
    test_text = """📋 RESUMEN EJECUTIVO ```json { "executive_summary": "El análisis temporal" }
🔍 HALLAZGOS PRINCIPALES ```json { "key_findings": "Se observa un crecimiento" }"""

    print("ORIGINAL TEXT:")
    print(repr(test_text))
    print()

    # Test pattern 1: Complete JSON blocks
    print("PATTERN 1: Complete JSON blocks")
    pattern1 = r'```json[^`]*?```'
    result1 = re.sub(pattern1, '', test_text, flags=re.DOTALL)
    print("Result:", repr(result1))
    print()

    # Test pattern 2: Incomplete JSON blocks (missing closing ```)
    print("PATTERN 2: Incomplete JSON blocks")
    pattern2 = r'```json\s*\{[^}]*\}[^`]*'
    result2 = re.sub(pattern2, '', test_text, flags=re.DOTALL)
    print("Result:", repr(result2))
    print()

    # Test pattern 3: More aggressive incomplete JSON
    print("PATTERN 3: More aggressive incomplete JSON")
    pattern3 = r'```json[^}]*\}[^}]*}'
    result3 = re.sub(pattern3, '', test_text, flags=re.DOTALL)
    print("Result:", repr(result3))
    print()

    # Test pattern 4: Even more aggressive
    print("PATTERN 4: Very aggressive JSON removal")
    pattern4 = r'```json\s*\{[^}]*\}'
    result4 = re.sub(pattern4, '', test_text, flags=re.DOTALL)
    print("Result:", repr(result4))
    print()

    # Test with section header protection
    print("TEST WITH SECTION HEADER PROTECTION:")
    protected = test_text

    # Protect section headers
    section_headers = [
        r'📋\s*RESUMEN\s+EJECUTIVO', r'🔍\s*HALLAZGOS\s+PRINCIPALES'
    ]

    for i, header_pattern in enumerate(section_headers):
        placeholder = f"__SECTION_HEADER_{i}__"
        protected = re.sub(header_pattern, placeholder, protected, flags=re.IGNORECASE)

    print("After protection:", repr(protected))

    # Apply improved incomplete JSON pattern
    improved_pattern = r'```json\s*\{[^}]*\}[^`\n]*'
    protected = re.sub(improved_pattern, '', protected, flags=re.DOTALL)
    print("After JSON removal (improved):", repr(protected))

    # Restore headers
    section_texts = ['📋 RESUMEN EJECUTIVO', '🔍 HALLAZGOS PRINCIPALES']
    for i, section_text in enumerate(section_texts):
        placeholder = f"__SECTION_HEADER_{i}__"
        protected = protected.replace(placeholder, section_text)

    print("After restoration:", repr(protected))

    # Remove orphaned "json"
    protected = re.sub(r'\bjson\b', '', protected, flags=re.IGNORECASE)
    protected = re.sub(r'\s+', ' ', protected).strip()
    print("Final result:", repr(protected))

if __name__ == "__main__":
    debug_json_patterns()