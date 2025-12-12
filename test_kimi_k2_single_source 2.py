#!/usr/bin/env python3
"""
Single-source test script for Kimi K2 with single-source analysis.
"""

import asyncio
import sys
import json
import re

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class KimiK2SingleSourceTester:
    """Test Kimi K2 with single-source analysis."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")

    def clean_json_content(self, content):
        """Clean JSON formatting from content."""
        if not content:
            return content

        if isinstance(content, str):
            # Remove JSON code blocks
            if content.startswith('```json'):
                content = re.sub(r'```json\n?', '', content)
                content = re.sub(r'\n?```$', '', content)

            # Try to extract clean content from JSON if it's malformed
            try:
                if content.strip().startswith('{'):
                    json_data = json.loads(content)
                    if "executive_summary" in json_data:
                        content = json_data["executive_summary"]
                    elif "finding" in json_data:
                        content = json_data["finding"]
                    elif "bullet_point" in json_data:
                        content = json_data["bullet_point"]
            except:
                pass

            return content.strip()
        else:
            return str(content)

    async def test_single_source_k2(self):
        """Test Kimi K2 with single-source analysis (Benchmarking + Google Trends)."""

        print("🎯 KIMI K2 SINGLE-SOURCE TEST")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Sources: Google Trends (Single Source)")
        print("Language: Spanish")
        print("Model: Kimi K2 (moonshotai/kimi-k2-instruct)")
        print("Max Tokens: 6000")
        print("Timeout: 30s")
        print("=" * 80)

        # Prepare single-source test data
        test_data = {
            "tool_name": "Benchmarking",
            "selected_sources": ["Google Trends"],
            "language": "es",
            "date_range_start": "1950-01-01",
            "date_range_end": "2023-12-31",
            "data_points_analyzed": 240,
            "temporal_analysis": {
                "trend_direction": "increasing",
                "key_periods": ["1995", "2008", "2015"],
                "overall_growth": "significant"
            },
            "seasonal_analysis": {
                "patterns": ["quarterly", "annual"],
                "volatility": "moderate"
            },
            "fourier_analysis": {
                "dominant_cycles": ["36-month", "12-month"],
                "spectral_power": "concentrated"
            }
        }

        print("\n📝 GENERATING SINGLE-SOURCE PROMPT...")
        prompt = self.prompt_engineer.create_analysis_prompt(test_data, {})
        print(f"✅ Single-source prompt created: {len(prompt)} characters")

        print("\n🤖 CALLING KIMI K2 FOR SINGLE-SOURCE ANALYSIS...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                model="moonshotai/kimi-k2-instruct"
            )

            print(f"✅ Kimi K2 single-source response received")
            print(f"📊 Response type: {type(response)}")
            print(f"📏 Response length: {len(str(response))} characters")

            # Check which model was actually used
            actual_model = response.get('model_used', 'unknown')
            print(f"🤖 Actually used model: {actual_model}")

            if actual_model != 'moonshotai/kimi-k2-instruct':
                print("⚠️  WARNING: Kimi K2 was not used - falling back to alternative model")
                return None

            # Process and display the single-source response
            if isinstance(response, dict) and "content" in response:
                content = response["content"]

                print(f"\n📋 SECTIONS FOUND IN SINGLE-SOURCE RESPONSE:")
                sections_found = []
                for section in ['executive_summary', 'principal_findings', 'temporal_analysis',
                               'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']:
                    if section in content and content[section]:
                        sections_found.append(section)

                print(f"Sections present: {len(sections_found)}/7")
                print(f"Sections: {', '.join(sections_found)}")

                # Check for multi-source sections (should be empty)
                multi_source_sections = ['heatmap_analysis', 'pca_analysis']
                for section in multi_source_sections:
                    if section in content and content[section]:
                        print(f"⚠️  WARNING: {section} found in single-source analysis!")

                # Display the complete single-source analysis
                self.display_single_source_analysis(content, response)

                return content
            else:
                print("📝 RAW SINGLE-SOURCE RESPONSE:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error with Kimi K2 single-source: {e}")
            import traceback
            traceback.print_exc()
            return None

    def display_single_source_analysis(self, content, response):
        """Display the single-source analysis with proper formatting."""
        print(f"\n🎯 SINGLE-SOURCE KIMI K2 ANALYSIS:")
        print("=" * 80)

        # EXECUTIVE SUMMARY
        if "executive_summary" in content and content["executive_summary"]:
            print("📋 EXECUTIVE SUMMARY")
            print("-" * 50)
            exec_summary = self.clean_json_content(content["executive_summary"])
            print(exec_summary[:500] + "..." if len(exec_summary) > 500 else exec_summary)
            print()

        # PRINCIPAL FINDINGS (combined temporal + seasonal + fourier)
        if "principal_findings" in content and content["principal_findings"]:
            print("🔍 PRINCIPAL FINDINGS (Combined Analysis)")
            print("-" * 50)
            principal = self.clean_json_content(content["principal_findings"])
            print(principal[:800] + "..." if len(principal) > 800 else principal)
            print()

        # Check individual analysis sections (should be empty for single-source)
        individual_sections = ['temporal_analysis', 'seasonal_analysis', 'fourier_analysis']
        for section in individual_sections:
            if section in content and content[section]:
                print(f"⚠️  {section.upper()}: Found content (should be empty for single-source)")
                print(content[section][:200] + "...")
                print()

        # STRATEGIC SYNTHESIS
        if "strategic_synthesis" in content and content["strategic_synthesis"]:
            print("🎯 STRATEGIC SYNTHESIS")
            print("-" * 50)
            synthesis = self.clean_json_content(content["strategic_synthesis"])
            print(synthesis[:500] + "..." if len(synthesis) > 500 else synthesis)
            print()

        # CONCLUSIONS
        if "conclusions" in content and content["conclusions"]:
            print("📝 CONCLUSIONS")
            print("-" * 50)
            conclusions = self.clean_json_content(content["conclusions"])
            print(conclusions[:300] + "..." if len(conclusions) > 300 else conclusions)
            print()

        # TECHNICAL METADATA
        print("🔧 TECHNICAL INFORMATION")
        print("-" * 50)
        print(f"Model Used: {response.get('model_used', 'unknown')}")
        print(f"Provider: {response.get('provider_used', 'unknown')}")
        print(f"Response Time: {response.get('response_time_ms', 'unknown')}ms")
        print(f"Token Count: {response.get('token_count', 'unknown')}")
        print(f"Language: {response.get('language', 'unknown')}")
        print(f"Analysis Type: Single-Source")
        print(f"Expected Sections: 7 (no heatmap/PCA)")

        print("\n" + "=" * 80)
        print("✅ SINGLE-SOURCE KIMI K2 ANALYSIS COMPLETE!")

if __name__ == "__main__":
    exit_code = asyncio.run(KimiK2SingleSourceTester().test_single_source_k2())
    sys.exit(0 if exit_code else 1)