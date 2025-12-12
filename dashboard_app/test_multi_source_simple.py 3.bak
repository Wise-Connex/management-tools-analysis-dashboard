#!/usr/bin/env python3
"""
Simple test for multi-source K2 AI analysis within dashboard app environment.
"""

import asyncio
import sys

# Use relative imports for dashboard app
from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class SimpleMultiSourceTest:
    """Simple multi-source test for K2 AI."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")

    async def test_multi_source_k2(self):
        """Test K2 AI with multi-source analysis."""
        print("🎯 KIMI K2 MULTI-SOURCE TEST")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
        print("Language: Spanish")
        print("Model: Kimi K2 (moonshotai/kimi-k2-instruct)")
        print("=" * 80)

        # Prepare multi-source test data
        test_data = {
            "tool_name": "Benchmarking",
            "selected_sources": ["Google Trends", "Google Books", "Bain Usability", "Bain Satisfaction", "Crossref"],
            "language": "es",
            "date_range_start": "1950-01-01",
            "date_range_end": "2023-12-31",
            "data_points_analyzed": 888,
            "pca_insights": {
                "dominant_patterns": [{"component": 1, "loadings": {"Google Trends": 0.8, "Google Books": 0.7, "Bain Usability": 0.6, "Bain Satisfaction": 0.5, "Crossref": 0.9}}],
                "total_variance_explained": 78.5
            },
            "heatmap_analysis": {"correlation_matrix": "sample_correlation_data"}
        }

        try:
            print("\n📝 GENERATING MULTI-SOURCE PROMPT...")
            prompt = self.prompt_engineer.create_analysis_prompt(test_data, {})
            print(f"✅ Multi-source prompt created: {len(prompt)} characters")

            print("\n🤖 CALLING KIMI K2 FOR MULTI-SOURCE ANALYSIS...")
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                model="moonshotai/kimi-k2-instruct",
                is_single_source=False  # Explicitly multi-source
            )

            if response and 'content' in response:
                content = response["content"]

                print(f"\n📋 SECTIONS FOUND IN MULTI-SOURCE RESPONSE:")
                sections_found = []
                for section in ['executive_summary', 'principal_findings', 'temporal_analysis',
                               'heatmap_analysis', 'fourier_analysis', 'pca_analysis',
                               'strategic_synthesis', 'conclusions']:
                    if section in content and content[section]:
                        sections_found.append(section)

                print(f"Sections present: {len(sections_found)}/8")
                print(f"Sections: {', '.join(sections_found)}")

                # Check specifically for multi-source sections
                multi_source_sections = ['heatmap_analysis', 'pca_analysis']
                for section in multi_source_sections:
                    if section in content and content[section]:
                        print(f"✅ {section}: {len(str(content[section]))} characters (multi-source content)")
                    else:
                        print(f"⚠️  {section}: Empty (missing multi-source content)")

                print(f"\n🔧 TECHNICAL INFORMATION")
                print(f"Model Used: {response.get('model_used', 'unknown')}")
                print(f"Provider: {response.get('provider_used', 'unknown')}")
                print(f"Response Time: {response.get('response_time_ms', 'unknown')}ms")
                print(f"Token Count: {response.get('token_count', 'unknown')}")
                print(f"Language: {response.get('language', 'unknown')}")

                return response
            else:
                print("❌ No valid response received")
                return None

        except Exception as e:
            print(f"❌ Error with Kimi K2 multi-source: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def run_test(self):
        """Run the multi-source test."""
        print("🚀 STARTING K2 AI MULTI-SOURCE TEST")
        print("=" * 80)

        result = await self.test_multi_source_k2()

        print(f"\n" + "=" * 80)
        if result:
            print("✅ MULTI-SOURCE TEST COMPLETED SUCCESSFULLY!")
        else:
            print("❌ MULTI-SOURCE TEST FAILED")

        return result

if __name__ == "__main__":
    tester = SimpleMultiSourceTest()
    success = asyncio.run(tester.run_test())
    sys.exit(0 if success else 1)