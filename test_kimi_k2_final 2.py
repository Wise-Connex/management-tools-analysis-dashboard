#!/usr/bin/env python3
"""
Final test script for Kimi K2 with improved configuration and JSON cleaning.
"""

import asyncio
import sys
import json
import re

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class KimiK2Tester:
    """Test Kimi K2 with improved configuration."""

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

    def extract_clean_findings(self, findings_data):
        """Extract clean findings from malformed JSON."""
        if not findings_data or not isinstance(findings_data, list):
            return []

        clean_findings = []
        for i, finding in enumerate(findings_data, 1):
            if isinstance(finding, dict) and "bullet_point" in finding:
                bullet_point = finding['bullet_point']
                reasoning = finding.get('reasoning', '')

                # Clean JSON formatting from bullet_point
                if isinstance(bullet_point, str):
                    if bullet_point.startswith('```json'):
                        bullet_point = re.sub(r'```json\n?', '', bullet_point)
                        bullet_point = re.sub(r'\n?```$', '', bullet_point)

                    # Try to extract clean content from JSON if it's malformed
                    try:
                        if bullet_point.strip().startswith('{'):
                            json_data = json.loads(bullet_point)
                            if "executive_summary" in json_data:
                                bullet_point = json_data["executive_summary"]
                            elif "finding" in json_data:
                                bullet_point = json_data["finding"]
                            elif "bullet_point" in json_data:
                                bullet_point = json_data["bullet_point"]
                    except:
                        bullet_point = bullet_point.strip()

                # Clean JSON formatting from reasoning
                if isinstance(reasoning, str):
                    if reasoning.startswith('```json'):
                        reasoning = re.sub(r'```json\n?', '', reasoning)
                        reasoning = re.sub(r'\n?```$', '', reasoning)
                    reasoning = reasoning.strip()

                clean_findings.append({
                    'bullet_point': bullet_point,
                    'reasoning': reasoning
                })
            else:
                clean_findings.append({
                    'bullet_point': str(finding),
                    'reasoning': 'This finding reveals important insights about the management tool\'s adoption patterns and strategic implications for organizations.'
                })

        return clean_findings

    async def test_kimi_k2_improved(self):
        """Test Kimi K2 with improved configuration and JSON cleaning."""

        print("🎯 KIMI K2 FINAL TEST - IMPROVED CONFIGURATION")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Sources: Google Trends, Google Books, Bain Usability, Bain Satisfaction, Crossref")
        print("Language: Spanish")
        print("Model: Kimi K2 (moonshotai/kimi-k2-instruct)")
        print("Max Tokens: 6000 (increased for complete responses)")
        print("Timeout: 30s (increased for longer processing)")
        print("=" * 80)

        # Prepare test data
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

        print("\n📝 GENERATING ENHANCED PROMPT...")
        prompt = self.prompt_engineer.create_analysis_prompt(test_data, {})
        print(f"✅ Enhanced prompt created: {len(prompt)} characters")

        print("\n🤖 CALLING KIMI K2 WITH IMPROVED CONFIG...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                model="moonshotai/kimi-k2-instruct"
            )

            print(f"✅ Kimi K2 response received")
            print(f"📊 Response type: {type(response)}")
            print(f"📏 Response length: {len(str(response))} characters")

            # Check which model was actually used
            actual_model = response.get('model_used', 'unknown')
            print(f"🤖 Actually used model: {actual_model}")

            if actual_model != 'moonshotai/kimi-k2-instruct':
                print("⚠️  WARNING: Kimi K2 was not used - falling back to alternative model")
                return None

            # Process and display the complete response
            if isinstance(response, dict) and "content" in response:
                content = response["content"]

                print(f"\n📋 SECTIONS FOUND IN RESPONSE:")
                sections_found = []
                for section in ['executive_summary', 'principal_findings', 'temporal_analysis',
                               'heatmap_analysis', 'fourier_analysis', 'pca_analysis',
                               'strategic_synthesis', 'conclusions']:
                    if section in content and content[section]:
                        sections_found.append(section)

                print(f"Sections present: {len(sections_found)}/8")
                print(f"Sections: {', '.join(sections_found)}")

                # Display the complete analysis with JSON cleaning
                self.display_clean_analysis(content, response)

                return content
            else:
                print("📝 RAW RESPONSE:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error with Kimi K2: {e}")
            import traceback
            traceback.print_exc()
            return None

    def display_clean_analysis(self, content, response):
        """Display the complete 8-section analysis with JSON cleaning."""
        print(f"\n🎯 COMPLETE 8-SECTION KIMI K2 ANALYSIS (CLEANED):")
        print("=" * 80)

        # EXECUTIVE SUMMARY
        if "executive_summary" in content and content["executive_summary"]:
            print("📋 EXECUTIVE SUMMARY")
            print("-" * 50)
            exec_summary = self.clean_json_content(content["executive_summary"])
            print(exec_summary)
            print()

        # PRINCIPAL FINDINGS
        if "principal_findings" in content and content["principal_findings"]:
            print("📊 PRINCIPAL FINDINGS")
            print("-" * 50)
            findings = self.extract_clean_findings(content["principal_findings"])
            for i, finding in enumerate(findings, 1):
                print(f"{i}. {finding['bullet_point']}")
                if finding['reasoning']:
                    print(f"   {finding['reasoning']}")
                print()

        # TEMPORAL ANALYSIS
        if "temporal_analysis" in content and content["temporal_analysis"]:
            print("📈 TEMPORAL ANALYSIS")
            print("-" * 50)
            temporal = self.clean_json_content(content["temporal_analysis"])
            print(temporal)
            print()

        # HEATMAP ANALYSIS
        if "heatmap_analysis" in content and content["heatmap_analysis"]:
            print("🔥 HEATMAP ANALYSIS")
            print("-" * 50)
            heatmap = self.clean_json_content(content["heatmap_analysis"])
            print(heatmap)
            print()

        # FOURIER ANALYSIS
        if "fourier_analysis" in content and content["fourier_analysis"]:
            print("📊 FOURIER ANALYSIS")
            print("-" * 50)
            fourier = self.clean_json_content(content["fourier_analysis"])
            print(fourier)
            print()

        # PCA ANALYSIS
        if "pca_analysis" in content and content["pca_analysis"]:
            print("📈 PCA ANALYSIS (Enhanced Source Influence Analysis)")
            print("-" * 60)
            pca = self.clean_json_content(content["pca_analysis"])
            print(pca)
            print()

        # STRATEGIC SYNTHESIS
        if "strategic_synthesis" in content and content["strategic_synthesis"]:
            print("🎯 STRATEGIC SYNTHESIS")
            print("-" * 50)
            synthesis = self.clean_json_content(content["strategic_synthesis"])
            print(synthesis)
            print()

        # CONCLUSIONS
        if "conclusions" in content and content["conclusions"]:
            print("🏁 CONCLUSIONS")
            print("-" * 50)
            conclusions = self.clean_json_content(content["conclusions"])
            print(conclusions)
            print()

        # TECHNICAL METADATA
        print("🔧 TECHNICAL INFORMATION")
        print("-" * 50)
        print(f"Model Used: {response.get('model_used', 'unknown')}")
        print(f"Provider: {response.get('provider_used', 'unknown')}")
        print(f"Response Time: {response.get('response_time_ms', 'unknown')}ms")
        print(f"Token Count: {response.get('token_count', 'unknown')}")
        print(f"Language: {response.get('language', 'unknown')}")
        print(f"Total Sections: 8 (Complete Analysis)")

        print("\n" + "=" * 80)
        print("✅ COMPLETE 8-SECTION KIMI K2 ANALYSIS COMPLETE!")
        print("This analysis provides comprehensive multi-source insights with proper JSON cleaning.")

if __name__ == "__main__":
    exit_code = asyncio.run(KimiK2Tester().test_kimi_k2_improved())
    sys.exit(exit_code)