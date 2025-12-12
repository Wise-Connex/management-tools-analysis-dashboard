#!/usr/bin/env python3
"""
Debug the prompt generation to see why seasonal and fourier sections are missing
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

def debug_prompt_generation():
    """Debug what's happening in prompt generation"""
    print("🔍 DEBUGGING PROMPT GENERATION")
    print("=" * 50)

    from key_findings.prompt_engineer import PromptEngineer

    # Create a prompt engineer instance
    pe = PromptEngineer("es")

    # Simulate the data structure that would be passed
    test_data = {
        'tool_name': 'Benchmarking',
        'source_name': 'Google Trends',
        'date_range_start': '2004-01-01',
        'date_range_end': '2023-12-01',
        'data_points_analyzed': 240,
        'temporal_metrics': {
            'trend_direction': 'decreasing',
            'volatility': 1.0,
            'momentum': 0.697
        },
        'seasonal_patterns': {
            'seasonal_strength': 0.107,
            'peak_season': 'Q2',
            'seasonal_periodicity': 12.0
        },
        'fourier_analysis': {
            'dominant_frequency': 0.0083,
            'dominant_period': 120.0
        }
    }

    context = {}

    # Generate the prompt
    prompt = pe.create_improved_single_source_prompt(test_data, context)

    print(f"🔍 Generated prompt length: {len(prompt)} characters")
    print()

    # Check for the presence of all required sections
    required_sections = [
        "SECCIÓN 1: RESUMEN EJECUTIVO",
        "SECCIÓN 2: HALLAZGOS PRINCIPALES",
        "SECCIÓN 3: ANÁLISIS TEMPORAL",
        "SECCIÓN 4: ANÁLISIS DE PATRONES ESTACIONALES",
        "SECCIÓN 5: ANÁLISIS ESPECTRAL DE FOURIER",
        "SECCIÓN 6: SÍNTESIS ESTRATÉGICA",
        "SECCIÓN 7: CONCLUSIONES"
    ]

    print("🔍 CHECKING SECTIONS IN PROMPT:")
    print("-" * 40)
    for i, section in enumerate(required_sections, 1):
        if section in prompt:
            print(f"✅ Section {i}: {section} - FOUND")
        else:
            print(f"❌ Section {i}: {section} - MISSING")

    print()

    # If any sections are missing, let's see what's around those areas
    missing_sections = []
    for section in required_sections:
        if section not in prompt:
            missing_sections.append(section)

    if missing_sections:
        print("🔍 DEBUGGING MISSING SECTIONS:")
        print("-" * 40)
        for section in missing_sections:
            print(f"\n🔍 Looking for: {section}")
            # Try to find partial matches
            if "SECCIÓN 4" in prompt:
                print("✅ Found 'SECCIÓN 4' in prompt")
            if "ESTACIONALES" in prompt:
                print("✅ Found 'ESTACIONALES' in prompt")
            if "PATRONES" in prompt:
                print("✅ Found 'PATRONES' in prompt")

            if "SECCIÓN 5" in prompt:
                print("✅ Found 'SECCIÓN 5' in prompt")
            if "FOURIER" in prompt:
                print("✅ Found 'FOURIER' in prompt")
            if "ESPECTRAL" in prompt:
                print("✅ Found 'ESPECTRAL' in prompt")

    # Show a snippet of the prompt around the missing sections
    print("\n🔍 PROMPT CONTENT ANALYSIS:")
    print("-" * 40)

    # Find where section 3 ends
    if "SECCIÓN 3:" in prompt:
        section3_start = prompt.find("SECCIÓN 3:")
        snippet3 = prompt[section3_start:section3_start + 500]
        print(f"📄 After SECCIÓN 3:\n{snippet3}...")
        print()

    # Show the end of the prompt
    print(f"📄 Last 500 characters of prompt:\n{prompt[-500:]}")

if __name__ == "__main__":
    debug_prompt_generation()