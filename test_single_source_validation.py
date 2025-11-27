#!/usr/bin/env python3
"""
Test script to validate that single-source analysis properly excludes heatmap and PCA sections.
"""

import asyncio
import sys
import json

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.key_findings_service import KeyFindingsService
from database import get_database_manager

class SingleSourceValidator:
    """Validate single-source analysis content."""

    def __init__(self):
        self.key_findings_service = KeyFindingsService(get_database_manager())

    async def test_single_source_content(self):
        """Test that single-source analysis excludes multi-variable sections."""
        print("🧪 VALIDATING SINGLE-SOURCE CONTENT")
        print("=" * 80)
        print("Testing: Benchmarking + Google Trends (Single Source)")
        print("Expected: NO heatmap_analysis, NO pca_analysis")
        print("=" * 80)

        # Prepare single-source test data
        analysis_data = {
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

        try:
            print("\n🤖 GENERATING SINGLE-SOURCE ANALYSIS...")

            # Generate analysis using the key findings service
            result = await self.key_findings_service.generate_key_findings(
                tool_name="Benchmarking",
                selected_sources=["Google Trends"],
                language="es",
                date_range_start="1950-01-01",
                date_range_end="2023-12-31",
                analysis_data=analysis_data
            )

            if result and result.get("success"):
                print("✅ Analysis generated successfully!")

                content = result.get("content", {})
                if not content:
                    print("❌ No content found in result")
                    return False

                print(f"\n📋 CONTENT VALIDATION:")

                # Check each section
                sections_to_check = [
                    'executive_summary', 'principal_findings', 'temporal_analysis',
                    'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis',
                    'conclusions', 'heatmap_analysis', 'pca_analysis'
                ]

                validation_results = {}

                for section in sections_to_check:
                    has_content = section in content and content[section] and len(str(content[section])) > 10
                    validation_results[section] = has_content

                    if section in ['heatmap_analysis', 'pca_analysis']:
                        if has_content:
                            print(f"❌ {section}: FOUND CONTENT (SHOULD BE EMPTY)")
                            print(f"   Content preview: {str(content[section])[:100]}...")
                        else:
                            print(f"✅ {section}: EMPTY (CORRECT)")
                    else:
                        if has_content:
                            print(f"✅ {section}: {len(str(content[section]))} characters")
                        else:
                            print(f"⚠️  {section}: EMPTY")

                # Summary
                print(f"\n📊 VALIDATION SUMMARY:")
                multi_source_sections_found = 0
                for section in ['heatmap_analysis', 'pca_analysis']:
                    if validation_results.get(section, False):
                        multi_source_sections_found += 1

                if multi_source_sections_found == 0:
                    print("✅ PERFECT: No multi-source sections found in single-source analysis")
                    return True
                else:
                    print(f"❌ FAILED: Found {multi_source_sections_found} multi-source sections in single-source analysis")
                    return False

            else:
                print(f"❌ Failed to generate analysis: {result}")
                return False

        except Exception as e:
            print(f"❌ Error during validation: {e}")
            import traceback
            traceback.print_exc()
            return False

    def validate_content_logic(self):
        """Validate the fundamental logic of single vs multi-source analysis."""
        print(f"\n🔍 VALIDATING ANALYSIS LOGIC:")
        print("=" * 60)

        print("Mathematical Requirements:")
        print("• Single-source: 1 variable → NO correlation possible")
        print("• Multi-source: 2+ variables → correlation analysis possible")
        print("• PCA requires: Multiple variables for component extraction")
        print("• Heatmap requires: Multiple variables for correlation matrix")
        print()

        print("Expected Sections:")
        print("• Single-source (7 sections): Executive Summary, Principal Findings,")
        print("  Temporal Analysis, Seasonal Analysis, Fourier Analysis,")
        print("  Strategic Synthesis, Conclusions")
        print("• Multi-source (8+ sections): All above PLUS Heatmap Analysis,")
        print("  PCA Analysis")
        print()

    async def run_validation(self):
        """Run complete validation."""
        print("🔬 SINGLE-SOURCE ANALYSIS VALIDATION")
        print("=" * 80)

        self.validate_content_logic()

        success = await self.test_single_source_content()

        print(f"\n" + "=" * 80)
        if success:
            print("✅ VALIDATION PASSED: Single-source analysis correctly excludes multi-variable sections")
        else:
            print("❌ VALIDATION FAILED: Single-source analysis incorrectly includes multi-variable sections")

        return success

if __name__ == "__main__":
    validator = SingleSourceValidator()
    success = asyncio.run(validator.run_validation())
    sys.exit(0 if success else 1)