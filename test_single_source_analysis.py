#!/usr/bin/env python3
"""
Test script for single source analysis structure.
Verifies the 7-section format: Summary -> Findings -> Temporal -> Seasonal -> Fourier -> Synthesis -> Conclusions
"""

import asyncio
import sys

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class SingleSourceTester:
    """Test single source analysis structure."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")

    async def test_single_source_structure(self):
        """Test single source analysis with proper 7-section structure."""

        print("🎯 SINGLE SOURCE ANALYSIS TEST - 7 SECTION STRUCTURE")
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

        # Show prompt preview to verify single source structure
        print(f"\n📝 PROMOT PREVIEW (First 500 chars):")
        print("-" * 50)
        print(prompt[:500] + "...")
        print("-" * 50)

        print("\n🤖 CALLING AI FOR SINGLE SOURCE ANALYSIS...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                model="meta-llama/llama-4-scout-17b-16e-instruct"  # Using reliable model for testing
            )

            print(f"✅ AI response received")
            print(f"📊 Response type: {type(response)}")
            print(f"📏 Response length: {len(str(response))} characters")

            # Check which model was used
            actual_model = response.get('model_used', 'unknown')
            print(f"🤖 Used model: {actual_model}")

            # Process response
            if isinstance(response, dict) and "content" in response:
                content = response["content"]

                print(f"\n📋 SECTIONS FOUND IN SINGLE SOURCE RESPONSE:")
                sections_found = []
                expected_sections = [
                    'executive_summary', 'principal_findings', 'temporal_analysis',
                    'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions'
                ]

                for section in expected_sections:
                    if section in content and content[section]:
                        sections_found.append(section)
                        print(f"✅ {section}: Present")
                    else:
                        print(f"❌ {section}: Missing")

                print(f"\n📊 SECTION ANALYSIS:")
                print(f"Expected sections: {len(expected_sections)}")
                print(f"Found sections: {len(sections_found)}")
                print(f"Completion rate: {len(sections_found)/len(expected_sections)*100:.1f}%")

                # Display the complete analysis
                self.display_single_source_analysis(content)

                return content
            else:
                print("📝 RAW RESPONSE:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error with single source analysis: {e}")
            import traceback
            traceback.print_exc()
            return None

    def display_single_source_analysis(self, content):
        """Display the single source analysis with proper formatting."""
        print(f"\n🎯 SINGLE SOURCE ANALYSIS RESULTS:")
        print("=" * 80)

        # EXECUTIVE SUMMARY
        if "executive_summary" in content and content["executive_summary"]:
            print("📋 EXECUTIVE SUMMARY")
            print("-" * 50)
            print(content["executive_summary"][:300] + "..." if len(content["executive_summary"]) > 300 else content["executive_summary"])
            print()

        # PRINCIPAL FINDINGS
        if "principal_findings" in content and content["principal_findings"]:
            print("📊 PRINCIPAL FINDINGS")
            print("-" * 50)
            findings = content["principal_findings"]
            if isinstance(findings, list):
                for i, finding in enumerate(findings[:2], 1):  # Show first 2 findings
                    if isinstance(finding, dict) and "bullet_point" in finding:
                        print(f"{i}. {finding['bullet_point']}")
                        if finding.get('reasoning'):
                            print(f"   {finding['reasoning'][:100]}...")
                        print()

        # TEMPORAL ANALYSIS
        if "temporal_analysis" in content and content["temporal_analysis"]:
            print("📈 TEMPORAL ANALYSIS")
            print("-" * 50)
            temporal = content["temporal_analysis"]
            print(temporal[:300] + "..." if len(temporal) > 300 else temporal)
            print()

        # SEASONAL ANALYSIS
        if "seasonal_analysis" in content and content["seasonal_analysis"]:
            print("🌊 SEASONAL ANALYSIS")
            print("-" * 50)
            seasonal = content["seasonal_analysis"]
            print(seasonal[:300] + "..." if len(seasonal) > 300 else seasonal)
            print()

        # FOURIER ANALYSIS
        if "fourier_analysis" in content and content["fourier_analysis"]:
            print("📊 FOURIER ANALYSIS")
            print("-" * 50)
            fourier = content["fourier_analysis"]
            print(fourier[:300] + "..." if len(fourier) > 300 else fourier)
            print()

        # STRATEGIC SYNTHESIS
        if "strategic_synthesis" in content and content["strategic_synthesis"]:
            print("🎯 STRATEGIC SYNTHESIS")
            print("-" * 50)
            synthesis = content["strategic_synthesis"]
            print(synthesis[:300] + "..." if len(synthesis) > 300 else synthesis)
            print()

        # CONCLUSIONS
        if "conclusions" in content and content["conclusions"]:
            print("🏁 CONCLUSIONS")
            print("-" * 50)
            conclusions = content["conclusions"]
            print(conclusions[:300] + "..." if len(conclusions) > 300 else conclusions)
            print()

        print("🔧 Single source analysis focuses on temporal patterns, seasonality, and spectral analysis")
        print("=" * 80)

if __name__ == "__main__":
    exit_code = asyncio.run(SingleSourceTester().test_single_source_structure())
    sys.exit(exit_code)