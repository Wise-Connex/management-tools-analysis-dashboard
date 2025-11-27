#!/usr/bin/env python3
"""
Test script with fixed seasonal analysis parsing for single source.
"""

import asyncio
import sys
import re

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class FixedSingleSourceTester:
    """Test single source with fixed seasonal analysis parsing."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")

    def extract_sections_fixed(self, content):
        """Extract sections with fixed seasonal analysis support."""
        sections = {}

        # Fixed section patterns with seasonal_analysis added
        section_patterns = {
            'executive_summary': [
                '📋 Resumen Ejecutivo',
                '📋 Executive Summary',
                'Resumen Ejecutivo',
                'Executive Summary'
            ],
            'principal_findings': [
                '🔍 Hallazgos Principales',
                '🔍 Principal Findings',
                'Hallazgos Principales',
                'Principal Findings'
            ],
            'temporal_analysis': [
                '📈 Análisis Temporal',
                '📈 Temporal Analysis',
                'Análisis Temporal',
                'Temporal Analysis'
            ],
            'seasonal_analysis': [  # FIXED: Added missing seasonal analysis patterns
                '🌊 Análisis Estacional',
                '🌊 Seasonal Analysis',
                'Análisis de Patrones Estacionales',
                'Seasonal Pattern Analysis',
                'Análisis Estacional',
                'Seasonal Analysis'
            ],
            'fourier_analysis': [
                '📊 Análisis de Fourier',
                '📊 Fourier Analysis',
                'Análisis de Fourier',
                'Fourier Analysis'
            ],
            'strategic_synthesis': [
                '🎯 Síntesis Estratégica',
                '🎯 Strategic Synthesis',
                'Síntesis Estratégica',
                'Strategic Synthesis'
            ],
            'conclusions': [
                '🏁 Conclusiones',
                '🏁 Conclusions',
                'Conclusiones',
                'Conclusions',
                'CONCLUSIONES',
                'CONCLUSIONS'
            ]
        }

        lines = content.split('\n')
        current_section = None
        section_content = []

        for line in lines:
            line = line.strip()

            # Check if this line starts a new section
            section_started = False
            for section_key, patterns in section_patterns.items():
                if any(pattern in line for pattern in patterns):
                    # Save previous section if exists
                    if current_section and section_content:
                        sections[current_section] = '\n'.join(section_content).strip()
                        section_content = []

                    current_section = section_key
                    section_content = []
                    section_started = True
                    break

            if not section_started and current_section:
                # Continue accumulating content for current section
                section_content.append(line)

        # Save the last section
        if current_section and section_content:
            sections[current_section] = '\n'.join(section_content).strip()

        return sections

    async def test_fixed_single_source(self):
        """Test single source with fixed parsing."""

        print("🎯 FIXED SINGLE SOURCE ANALYSIS TEST")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Source: Google Trends")
        print("Language: Spanish")
        print("Expected Structure: Summary → Findings → Temporal → Seasonal → Fourier → Synthesis → Conclusions")
        print("=" * 80)

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

        print("\n📝 GENERATING SINGLE SOURCE PROMPT...")
        prompt = self.prompt_engineer.create_analysis_prompt(test_data, {})
        print(f"✅ Single source prompt created: {len(prompt)} characters")

        print("\n🤖 CALLING AI FOR SINGLE SOURCE ANALYSIS...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )

            print(f"✅ AI response received")

            if isinstance(response, dict) and "content" in response:
                content = response["content"]

                # The content might be a dict or string, handle both
                if isinstance(content, dict):
                    # If it's already a parsed dict, use it directly
                    sections = content
                elif isinstance(content, str):
                    # If it's a string, extract sections
                    sections = self.extract_sections_fixed(content)
                else:
                    # Fallback - try to convert to string
                    sections = self.extract_sections_fixed(str(content))

                print(f"\n📋 SECTIONS FOUND WITH FIXED PARSING:")
                expected_sections = [
                    'executive_summary', 'principal_findings', 'temporal_analysis',
                    'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions'
                ]

                found_sections = []
                for section in expected_sections:
                    if section in sections and sections[section]:
                        found_sections.append(section)
                        print(f"✅ {section}: Present ({len(sections[section])} chars)")
                    else:
                        print(f"❌ {section}: Missing")

                print(f"\n📊 SECTION ANALYSIS:")
                print(f"Expected sections: {len(expected_sections)}")
                print(f"Found sections: {len(found_sections)}")
                print(f"Completion rate: {len(found_sections)/len(expected_sections)*100:.1f}%")

                # Display the complete analysis
                self.display_sections(sections)

                return sections
            else:
                print("📝 RAW RESPONSE:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error with single source analysis: {e}")
            import traceback
            traceback.print_exc()
            return None

    def display_sections(self, sections):
        """Display the extracted sections."""
        print(f"\n🎯 SINGLE SOURCE ANALYSIS RESULTS:")
        print("=" * 80)

        for section_name, content in sections.items():
            # Map section names to display names
            display_names = {
                'executive_summary': '📋 EXECUTIVE SUMMARY',
                'principal_findings': '📊 PRINCIPAL FINDINGS',
                'temporal_analysis': '📈 TEMPORAL ANALYSIS',
                'seasonal_analysis': '🌊 SEASONAL ANALYSIS',
                'fourier_analysis': '📊 FOURIER ANALYSIS',
                'strategic_synthesis': '🎯 STRATEGIC SYNTHESIS',
                'conclusions': '🏁 CONCLUSIONS'
            }

            display_name = display_names.get(section_name, section_name.upper())
            print(f"{display_name}")
            print("-" * 50)
            print(content[:400] + "..." if len(content) > 400 else content)
            print()

        print("🔧 Single source analysis with proper seasonal analysis section")
        print("=" * 80)

if __name__ == "__main__":
    exit_code = asyncio.run(FixedSingleSourceTester().test_fixed_single_source())
    sys.exit(exit_code)

# ALSO: Let me create a patch for the actual unified_ai_service.py to fix the parsing permanently
print("\n" + "="*80)
print("📝 TO FIX THE ACTUAL CODE, ADD THIS TO unified_ai_service.py:")
print("="*80)
print("""
# In the section_patterns dictionary around line 585, add:

'seasonal_analysis': [
    '🌊 Análisis Estacional',
    '🌊 Seasonal Analysis',
    'Análisis de Patrones Estacionales',
    'Seasonal Pattern Analysis',
    'Análisis Estacional',
    'Seasonal Analysis'
],
""")