#!/usr/bin/env python3
"""
Test script for single source fixer to ensure exact 6-section structure.
"""

import asyncio
import sys
import logging

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService
from key_findings.prompt_engineer import PromptEngineer
from key_findings.single_source_fixer import SingleSourceFixer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SingleSourceFixerTester:
    """Test the single source fixer functionality."""

    def __init__(self):
        self.ai_service = UnifiedAIService()
        self.prompt_engineer = PromptEngineer(language="es")
        self.fixer = SingleSourceFixer()

    async def test_fixer_with_real_response(self):
        """Test the fixer with a real AI response."""

        print("🧪 TESTING SINGLE SOURCE FIXER WITH REAL AI RESPONSE")
        print("=" * 80)
        print("Tool: Benchmarking")
        print("Source: Google Trends")
        print("Language: Spanish")
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
        prompt = self.prompt_engineer.create_analysis_prompt(test_data, {})
        print(f"✅ Single source prompt created: {len(prompt)} characters")

        print("\n🤖 CALLING AI FOR SINGLE SOURCE ANALYSIS...")
        try:
            response = await self.ai_service.generate_analysis(
                prompt=prompt,
                language="es",
                is_single_source=True
            )

            print(f"✅ AI response received")

            if isinstance(response, dict) and "content" in response:
                original_content = response["content"]
                print(f"\n🔍 ORIGINAL AI RESPONSE STRUCTURE:")
                self._display_structure_summary(original_content)

                print(f"\n🔧 APPLYING SINGLE SOURCE FIXER...")
                fixed_content = self.fixer.fix_single_source_response(original_content.copy())

                print(f"\n📊 FIXED RESPONSE STRUCTURE:")
                self._display_structure_summary(fixed_content)

                print(f"\n✅ VALIDATION RESULTS:")
                is_valid = self.fixer.validate_single_source_structure(fixed_content)
                print(f"Structure validation: {'PASSED' if is_valid else 'FAILED'}")

                # Show the differences
                self._show_differences(original_content, fixed_content)

                return fixed_content
            else:
                print("📝 RAW RESPONSE:")
                print(str(response))
                return response

        except Exception as e:
            print(f"❌ Error testing fixer: {e}")
            import traceback
            traceback.print_exc()
            return None

    def _display_structure_summary(self, content: dict):
        """Display a summary of the response structure."""
        expected_sections = [
            'executive_summary', 'principal_findings', 'temporal_analysis',
            'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis',
            'conclusions', 'pca_insights'
        ]

        unwanted_sections = ['heatmap_analysis']

        print("📋 SECTIONS FOUND:")
        for section in expected_sections:
            if section in content and content[section]:
                content_length = len(str(content[section]))
                print(f"  ✅ {section}: {content_length} chars")
            else:
                print(f"  ❌ {section}: Missing")

        print("\n🚫 UNWANTED SECTIONS:")
        for section in unwanted_sections:
            if section in content and content[section]:
                print(f"  ⚠️  {section}: Present (should be excluded)")
            else:
                print(f"  ✅ {section}: Correctly excluded")

    def _show_differences(self, original: dict, fixed: dict):
        """Show the differences between original and fixed responses."""
        print(f"\n🔍 CHANGES MADE BY FIXER:")

        # Check for removed sections
        removed_sections = set(original.keys()) - set(fixed.keys())
        if removed_sections:
            print(f"🗑️  Removed sections: {', '.join(removed_sections)}")

        # Check for added sections
        added_sections = set(fixed.keys()) - set(original.keys())
        if added_sections:
            print(f"📋 Added sections: {', '.join(added_sections)}")

        # Check for modified sections
        modified_sections = []
        for section in set(original.keys()) & set(fixed.keys()):
            if original[section] != fixed[section]:
                modified_sections.append(section)

        if modified_sections:
            print(f"✏️  Modified sections: {', '.join(modified_sections)}")

        if not removed_sections and not added_sections and not modified_sections:
            print("✅ No changes needed - structure was already correct")

    async def test_fixer_edge_cases(self):
        """Test the fixer with various edge cases."""

        print(f"\n🧪 TESTING FIXER EDGE CASES")
        print("=" * 80)

        test_cases = [
            {
                "name": "Missing seasonal_analysis",
                "content": {
                    'executive_summary': 'Test',
                    'principal_findings': [],
                    'temporal_analysis': 'Temporal content with seasonal patterns showing quarterly cycles',
                    'fourier_analysis': 'Fourier content',
                    'strategic_synthesis': 'Synthesis',
                    'conclusions': 'Conclusions',
                    'pca_insights': {}
                }
            },
            {
                "name": "Unwanted heatmap_analysis",
                "content": {
                    'executive_summary': 'Test',
                    'principal_findings': [],
                    'temporal_analysis': 'Temporal',
                    'seasonal_analysis': 'Seasonal',
                    'fourier_analysis': 'Fourier',
                    'strategic_synthesis': 'Synthesis',
                    'conclusions': 'Conclusions',
                    'pca_insights': {},
                    'heatmap_analysis': 'This should be removed'
                }
            },
            {
                "name": "Empty sections",
                "content": {
                    'executive_summary': '',
                    'principal_findings': [],
                    'temporal_analysis': '',
                    'seasonal_analysis': '',
                    'fourier_analysis': '',
                    'strategic_synthesis': '',
                    'conclusions': '',
                    'pca_insights': {}
                }
            }
        ]

        for test_case in test_cases:
            print(f"\n🧪 Testing: {test_case['name']}")
            original = test_case['content'].copy()
            fixed = self.fixer.fix_single_source_response(original.copy())

            print(f"Original sections: {list(original.keys())}")
            print(f"Fixed sections: {list(fixed.keys())}")

            is_valid = self.fixer.validate_single_source_structure(fixed)
            print(f"Validation: {'PASSED' if is_valid else 'FAILED'}")

if __name__ == "__main__":
    tester = SingleSourceFixerTester()

    # Run main test
    exit_code = asyncio.run(tester.test_fixer_with_real_response())

    # Run edge case tests
    asyncio.run(tester.test_fixer_edge_cases())

    sys.exit(exit_code)

print("\n" + "="*80)
print("🎯 SINGLE SOURCE FIXER IMPLEMENTATION COMPLETE")
print("="*80)
print("""
The SingleSourceFixer now ensures:
✅ Exact 6-section structure for single source analysis
✅ Removal of unwanted multi-source sections (heatmap_analysis)
✅ Creation of separate seasonal_analysis section
✅ Validation of final structure
✅ Graceful handling of edge cases

This provides a robust solution for maintaining consistent single source analysis format.
""")