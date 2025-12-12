#!/usr/bin/env python3
"""
Debug script to examine the exact single source prompt being sent to AI.
"""

import sys

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.prompt_engineer import PromptEngineer

def debug_single_source_prompt():
    """Debug the single source prompt structure."""

    print("🔍 DEBUGGING SINGLE SOURCE PROMPT STRUCTURE")
    print("=" * 80)

    prompt_engineer = PromptEngineer(language="es")

    # Prepare test data for single source
    test_data = {
        "tool_name": "Benchmarking",
        "source_name": "Google Trends",  # This triggers single source mode
        "language": "es",
        "date_range_start": "1950-01-01",
        "date_range_end": "2023-12-31",
        "data_points_analyzed": 888,
        "temporal_metrics": {
            "trend_direction": "growing",
            "volatility": "moderate",
            "inflection_points": ["1980", "2000", "2015"]
        },
        "seasonal_patterns": {
            "dominant_seasonality": "annual",
            "seasonal_strength": "strong",
            "peak_months": ["March", "September"],
            "variability": "consistent"
        },
        "fourier_analysis": {
            "dominant_frequency": "0.5",
            "spectral_power": "high",
            "secondary_frequencies": ["1.0", "2.0"],
            "noise_level": "low"
        }
    }

    print("📝 GENERATING SINGLE SOURCE PROMPT...")
    prompt = prompt_engineer.create_analysis_prompt(test_data, {})

    print(f"✅ Prompt generated: {len(prompt)} characters")
    print(f"\n🔍 EXAMINING PROMPT STRUCTURE:")
    print("=" * 80)

    # Look for the section structure in the prompt
    lines = prompt.split('\n')
    section_found = False
    section_count = 0

    for i, line in enumerate(lines):
        # Look for section headers
        if 'SECTION' in line and ('SEASONAL' in line or 'TEMPORAL' in line or 'FOURIER' in line):
            section_count += 1
            print(f"\n📋 {line.strip()}")
            section_found = True
            # Print next few lines to see the context
            for j in range(1, 4):
                if i + j < len(lines):
                    print(f"   {lines[i+j].strip()}")

    if not section_found:
        print("❌ No explicit section headers found in prompt")
        print("\n🔍 Looking for section references...")

        # Look for any seasonal references
        seasonal_refs = []
        temporal_refs = []
        fourier_refs = []

        for i, line in enumerate(lines):
            if 'estacional' in line.lower() or 'seasonal' in line.lower():
                seasonal_refs.append((i, line.strip()))
            if 'temporal' in line.lower():
                temporal_refs.append((i, line.strip()))
            if 'fourier' in line.lower():
                fourier_refs.append((i, line.strip()))

        print(f"\n🌊 Seasonal references found: {len(seasonal_refs)}")
        for line_num, line in seasonal_refs[:3]:
            print(f"   Line {line_num}: {line}")

        print(f"\n📈 Temporal references found: {len(temporal_refs)}")
        for line_num, line in temporal_refs[:3]:
            print(f"   Line {line_num}: {line}")

        print(f"\n📊 Fourier references found: {len(fourier_refs)}")
        for line_num, line in fourier_refs[:3]:
            print(f"   Line {line_num}: {line}")

    print(f"\n📊 SECTION SUMMARY:")
    print(f"Total sections found: {section_count}")

    # Show the first 1000 characters to see the overall structure
    print(f"\n📝 PROMPT PREVIEW (First 1000 chars):")
    print("-" * 50)
    print(prompt[:1000])
    print("-" * 50)

    if len(prompt) > 1000:
        print(f"\n📏 Full prompt length: {len(prompt)} characters")
        print("💡 The prompt is quite long. The section structure should be clearly defined.")

if __name__ == "__main__":
    debug_single_source_prompt()

    print("\n" + "="*80)
    print("💡 RECOMMENDATION:")
    print("="*80)
    print("""
If the AI is not creating separate seasonal analysis sections, the issue might be:

1. The AI is combining seasonal patterns into temporal analysis
2. The section structure in the prompt needs to be more explicit
3. The AI needs stronger instructions to create separate sections

Consider:
- Making the section separation more explicit in the prompt
- Adding specific instructions about keeping seasonal analysis separate
- Using more distinct section headers that the AI will recognize
""")