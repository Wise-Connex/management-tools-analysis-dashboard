#!/usr/bin/env python3
"""
Final test to display complete single source analysis with exact 6-section structure.
"""

import asyncio
import sys

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class SingleSourceFinalTest:
    """Display complete single source analysis results."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")

    async def test_single_source_display(self):
        """Test and display complete single source analysis."""

        print("🎯 COMPLETE SINGLE SOURCE ANALYSIS - 6 SECTION STRUCTURE")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Source: Google Trends")
        print("Language: Spanish")
        print("Expected Structure: 6 exact sections (no heatmap, no multi-source correlation)")
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
        print(f"✅ Prompt created: {len(prompt)} characters")

        print("\n🤖 CALLING KIMI K2 FOR SINGLE SOURCE ANALYSIS...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                is_single_source=True
            )

            print(f"✅ AI response received")

            if isinstance(response, dict) and "content" in response:
                content = response["content"]

                print(f"\n📊 STRUCTURE VERIFICATION:")
                expected_sections = [
                    'executive_summary', 'principal_findings', 'temporal_analysis',
                    'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions'
                ]

                unwanted_sections = ['heatmap_analysis', 'pca_analysis']

                sections_found = []
                for section in expected_sections:
                    if section in content and content[section]:
                        sections_found.append(section)
                        print(f"✅ {section}: Present ({len(str(content[section]))} chars)")
                    else:
                        print(f"❌ {section}: Missing")

                print(f"\n🚫 UNWANTED SECTIONS CHECK:")
                for section in unwanted_sections:
                    if section in content and content[section]:
                        print(f"⚠️  {section}: Present (should be excluded)")
                    else:
                        print(f"✅ {section}: Correctly excluded")

                completion_rate = len(sections_found) / len(expected_sections) * 100
                print(f"\n📈 COMPLETION RATE: {completion_rate:.1f}%")

                # Display the complete analysis
                self.display_complete_analysis(content)

                return content
            else:
                print("📝 RAW RESPONSE:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return None

    def display_complete_analysis(self, content):
        """Display the complete single source analysis with all 6 sections."""
        print(f"\n🎯 COMPLETE SINGLE SOURCE ANALYSIS RESULTS:")
        print("=" * 80)

        # EXECUTIVE SUMMARY
        if "executive_summary" in content and content["executive_summary"]:
            print("\n📋 EXECUTIVE SUMMARY")
            print("-" * 60)
            print(content["executive_summary"])
            print()

        # PRINCIPAL FINDINGS
        if "principal_findings" in content and content["principal_findings"]:
            print("\n📊 PRINCIPAL FINDINGS")
            print("-" * 60)
            findings = content["principal_findings"]
            if isinstance(findings, list):
                for i, finding in enumerate(findings, 1):
                    if isinstance(finding, dict) and "bullet_point" in finding:
                        print(f"{i}. {finding['bullet_point']}")
                        if finding.get('reasoning'):
                            print(f"   {finding['reasoning']}")
                        print()

        # TEMPORAL ANALYSIS
        if "temporal_analysis" in content and content["temporal_analysis"]:
            print("\n📈 TEMPORAL ANALYSIS")
            print("-" * 60)
            print(content["temporal_analysis"])
            print()

        # SEASONAL ANALYSIS
        if "seasonal_analysis" in content and content["seasonal_analysis"]:
            print("\n🌊 SEASONAL ANALYSIS")
            print("-" * 60)
            print(content["seasonal_analysis"])
            print()

        # FOURIER ANALYSIS
        if "fourier_analysis" in content and content["fourier_analysis"]:
            print("\n📊 FOURIER ANALYSIS")
            print("-" * 60)
            print(content["fourier_analysis"])
            print()

        # STRATEGIC SYNTHESIS
        if "strategic_synthesis" in content and content["strategic_synthesis"]:
            print("\n🎯 STRATEGIC SYNTHESIS")
            print("-" * 60)
            print(content["strategic_synthesis"])
            print()

        # CONCLUSIONS
        if "conclusions" in content and content["conclusions"]:
            print("\n🏁 CONCLUSIONS")
            print("-" * 60)
            print(content["conclusions"])
            print()

        print("=" * 80)
        print("✅ SINGLE SOURCE ANALYSIS COMPLETE!")
        print("This analysis focuses exclusively on temporal, seasonal, and spectral patterns")
        print("from a single data source (Google Trends) without multi-source correlation analysis.")

if __name__ == "__main__":
    exit_code = asyncio.run(SingleSourceFinalTest().test_single_source_display())
    sys.exit(exit_code)

print("\n" + "="*80)
print("🎯 SINGLE SOURCE ANALYSIS READY FOR REVIEW")
print("="*80)
print("The 6-section structure provides:")
print("• Executive-level insights on temporal patterns")
print("• Seasonal cycle analysis for optimal timing")
print("• Spectral analysis for cycle prediction")
print("• Strategic synthesis combining all temporal insights")
print("• Doctoral-level academic rigor")
print("• Complete exclusion of multi-source correlation analysis")
print("="*80)
print("Ready to display the complete single source analysis!")