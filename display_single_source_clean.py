#!/usr/bin/env python3
"""
Clean display of single source analysis with properly formatted section headers.
"""

import asyncio
import sys

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class CleanSingleSourceDisplay:
    """Display single source analysis with clean, consistent formatting."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")

    async def display_clean_analysis(self):
        """Display the complete single source analysis with clean formatting."""

        print("🎯 SINGLE SOURCE ANALYSIS - CLEAN DISPLAY")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Source: Google Trends")
        print("Language: Spanish")
        print("Structure: 6 exact sections (temporal/seasonal/spectral focus)")
        print("=" * 80)

        # Prepare test data for single source
        test_data = {
            "tool_name": "Benchmarking",
            "source_name": "Google Trends",
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

        print("\n📝 Generating single source prompt...")
        prompt = self.prompt_engineer.create_analysis_prompt(test_data, {})
        print(f"✅ Prompt created: {len(prompt)} characters")

        print("\n🤖 Calling AI for single source analysis...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                is_single_source=True
            )

            print(f"✅ AI response received")

            if isinstance(response, dict) and "content" in response:
                content = response["content"]

                print(f"\n📊 Structure Verification:")
                expected_sections = [
                    'executive_summary', 'principal_findings', 'temporal_analysis',
                    'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions'
                ]

                for section in expected_sections:
                    if section in content and content[section]:
                        content_length = len(str(content[section]))
                        print(f"  ✅ {section}: {content_length} chars")
                    else:
                        print(f"  ❌ {section}: Missing")

                # Display with clean, consistent formatting
                self.display_sections_clean(content)

                return content
            else:
                print("📝 Raw response:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def display_sections_clean(self, content):
        """Display sections with clean, consistent formatting."""
        print(f"\n🎯 Complete Single Source Analysis Results:")
        print("=" * 80)

        sections = [
            ('executive_summary', '📋 EXECUTIVE SUMMARY'),
            ('principal_findings', '📊 PRINCIPAL FINDINGS'),
            ('temporal_analysis', '📈 TEMPORAL ANALYSIS'),
            ('seasonal_analysis', '🌊 SEASONAL ANALYSIS'),
            ('fourier_analysis', '📊 FOURIER ANALYSIS'),
            ('strategic_synthesis', '🎯 STRATEGIC SYNTHESIS'),
            ('conclusions', '🏁 CONCLUSIONS')
        ]

        for section_key, section_title in sections:
            if section_key in content and content[section_key]:
                print(f"\n{section_title}")
                print("-" * 60)

                if section_key == 'principal_findings' and isinstance(content[section_key], list):
                    # Handle findings array
                    findings = content[section_key]
                    for i, finding in enumerate(findings, 1):
                        if isinstance(finding, dict) and 'bullet_point' in finding:
                            print(f"{i}. {finding['bullet_point']}")
                            if finding.get('reasoning'):
                                print(f"   {finding['reasoning']}")
                            print()
                else:
                    # Handle regular sections
                    section_content = str(content[section_key])
                    # Clean up any formatting issues
                    section_content = section_content.replace('------------------------------------------------------------', '')
                    section_content = section_content.replace('\n\n\n', '\n\n')

                    if len(section_content) > 1000:
                        # For long sections, show first part with indication
                        print(section_content[:800] + "...")
                        print(f"\n   [Content continues - {len(section_content)} characters total]")
                    else:
                        print(section_content)
                    print()

        print("=" * 80)
        print("✅ Single Source Analysis Complete!")
        print("This analysis provides temporal, seasonal, and spectral insights from a single data source.")

if __name__ == "__main__":
    exit_code = asyncio.run(CleanSingleSourceDisplay().display_clean_analysis())
    sys.exit(exit_code)

print("\n" + "="*80)
print("🎯 Clean Single Source Analysis Ready")
print("="*80)
print("Ready to display with clean, consistent section formatting!")