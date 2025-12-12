#!/usr/bin/env python3
"""
Test script to force exact single source structure with explicit JSON format instructions.
"""

import asyncio
import sys

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer

class ExactStructureTester:
    """Test exact single source structure with explicit instructions."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")

    def create_exact_structure_prompt(self, base_prompt):
        """Add explicit instructions for exact JSON structure."""
        exact_structure_instruction = """

⚠️ CRITICAL: RESPOND EXACTAMENTE CON ESTA ESTRUCTURA JSON - NINGUNA OTRA SECCIÓN:

{
  "executive_summary": "[400 palabras - resumen ejecutivo]",
  "principal_findings": [
    {
      "bullet_point": "[Hallazgo clave en 1 frase]",
      "reasoning": "[Explicación detallada en párrafo fluido]"
    }
  ],
  "temporal_analysis": "[1000 palabras - análisis temporal detallado]",
  "seasonal_analysis": "[800 palabras - análisis de patrones estacionales]",
  "fourier_analysis": "[800 palabras - análisis espectral de Fourier]",
  "strategic_synthesis": "[600 palabras - síntesis estratégica]",
  "conclusions": "[400 palabras - conclusiones y recomendaciones]",
  "pca_insights": {
    "analysis": "[Datos técnicos de PCA]",
    "reasoning": "[Interpretación de PCA]"
  }
}

🚨 INSTRUCCIONES OBLIGATORIAS:
1. Usar EXACTAMENTE estos nombres de secciones - ningún otro
2. NO incluir heatmap_analysis (solo para múltiples fuentes)
3. CREAR seasonal_analysis como sección separada - no combinar con temporal_analysis
4. Cada sección debe ser un ensayo narrativo completo
5. Enfocarse en patrones temporales, estacionales y espectrales únicamente
6. Mantener el formato JSON exacto mostrado arriba
"""
        return base_prompt + exact_structure_instruction

    async def test_exact_structure(self):
        """Test with exact structure instructions."""

        print("🎯 EXACT SINGLE SOURCE STRUCTURE TEST")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Source: Google Trends")
        print("Language: Spanish")
        print("Expected: Exact 6-section JSON structure")
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

        print("\n📝 GENERATING SINGLE SOURCE PROMPT...")
        base_prompt = self.prompt_engineer.create_analysis_prompt(test_data, {})
        exact_prompt = self.create_exact_structure_prompt(base_prompt)
        print(f"✅ Enhanced prompt created: {len(exact_prompt)} characters")

        print("\n🤖 CALLING AI WITH EXACT STRUCTURE INSTRUCTIONS...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=exact_prompt,
                language="es",
                is_single_source=True
            )

            print(f"✅ AI response received")

            if isinstance(response, dict) and "content" in response:
                content = response["content"]

                print(f"\n📋 SECTIONS FOUND IN EXACT STRUCTURE RESPONSE:")
                expected_sections = [
                    'executive_summary', 'principal_findings', 'temporal_analysis',
                    'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions'
                ]

                sections_found = []
                for section in expected_sections:
                    if section in content and content[section]:
                        sections_found.append(section)
                        print(f"✅ {section}: Present ({len(str(content[section]))} chars)")
                    else:
                        print(f"❌ {section}: Missing")

                # Check for unwanted sections
                unwanted_sections = ['heatmap_analysis', 'pca_analysis']
                print(f"\n🚫 UNWANTED SECTIONS CHECK:")
                for section in unwanted_sections:
                    if section in content and content[section]:
                        print(f"⚠️  {section}: Present (should be excluded)")
                    else:
                        print(f"✅ {section}: Correctly excluded")

                print(f"\n📊 COMPLETION ANALYSIS:")
                print(f"Expected sections: {len(expected_sections)}")
                print(f"Found sections: {len(sections_found)}")
                print(f"Completion rate: {len(sections_found)/len(expected_sections)*100:.1f}%")

                # Display the complete analysis
                self.display_exact_analysis(content)

                return content
            else:
                print("📝 RAW RESPONSE:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error with exact structure test: {e}")
            import traceback
            traceback.print_exc()
            return None

    def display_exact_analysis(self, content):
        """Display the exact structure analysis."""
        print(f"\n🎯 EXACT SINGLE SOURCE ANALYSIS RESULTS:")
        print("=" * 80)

        for section_name in ['executive_summary', 'principal_findings', 'temporal_analysis',
                           'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']:
            if section_name in content and content[section_name]:
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

                if section_name == 'principal_findings' and isinstance(content[section_name], list):
                    # Handle findings array
                    for i, finding in enumerate(content[section_name], 1):
                        if isinstance(finding, dict) and 'bullet_point' in finding:
                            print(f"{i}. {finding['bullet_point']}")
                            if finding.get('reasoning'):
                                print(f"   {finding['reasoning'][:200]}...")
                            print()
                else:
                    # Handle regular sections
                    section_content = str(content[section_name])
                    print(section_content[:400] + "..." if len(section_content) > 400 else section_content)
                print()

        print("🔧 Exact structure test with explicit JSON formatting instructions")
        print("=" * 80)

if __name__ == "__main__":
    exit_code = asyncio.run(ExactStructureTester().test_exact_structure())
    sys.exit(exit_code)

# ALSO: Let me create a summary of what we've learned
print("\n" + "="*80)
print("📋 SUMMARY OF SINGLE SOURCE STRUCTURE ISSUES:")
print("="*80)
print("""
PROBLEMS IDENTIFIED:
1. AI still includes heatmap_analysis and pca_analysis (should be excluded for single source)
2. AI combines seasonal content into temporal_analysis instead of separate seasonal_analysis section
3. System prompt changes work but AI needs stronger explicit instructions

SOLUTIONS IMPLEMENTED:
1. ✅ Separate system prompts for single vs multi-source analysis
2. ✅ Updated _get_system_prompt() to accept is_single_source parameter
3. ✅ Modified generate_analysis() to pass is_single_source flag
4. ✅ Added seasonal_analysis to parsing patterns
5. ✅ Updated key_findings_service to properly route single source analysis

NEXT STEPS:
- Test with more explicit JSON structure instructions
- Consider using a different model that follows instructions better
- Potentially add post-processing to force correct structure
""")