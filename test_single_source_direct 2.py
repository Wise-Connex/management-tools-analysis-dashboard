#!/usr/bin/env python3
"""
Direct test of single-source AI response processing to validate heatmap/PCA exclusion.
"""

import asyncio
import sys
import json

# Add the dashboard_app to path
sys.path.insert(0, '/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

from key_findings.unified_ai_service import UnifiedAIService

class DirectSingleSourceTest:
    """Test single-source processing directly."""

    def __init__(self):
        self.ai_service = UnifiedAIService()

    def test_single_source_normalization(self):
        """Test that single-source normalization excludes heatmap/PCA."""
        print("🧪 TESTING SINGLE-SOURCE NORMALIZATION")
        print("=" * 60)

        # Test data that simulates what AI might return (including heatmap/PCA)
        test_response = {
            "executive_summary": "This is an executive summary for single-source analysis.",
            "principal_findings": [
                {"bullet_point": "Finding 1", "reasoning": "Reasoning 1"},
                {"bullet_point": "Finding 2", "reasoning": "Reasoning 2"}
            ],
            "temporal_analysis": "Temporal analysis content here.",
            "seasonal_analysis": "Seasonal analysis content here.",
            "fourier_analysis": "Fourier analysis content here.",
            "strategic_synthesis": "Strategic synthesis content here.",
            "conclusions": "Conclusions content here.",
            # These should be excluded for single-source
            "heatmap_analysis": "This should be empty for single-source",
            "pca_analysis": "This should also be empty for single-source"
        }

        print("Testing normalization with is_single_source=True...")

        # Test single-source normalization
        normalized = self.ai_service._normalize_parsed_response(test_response, is_single_source=True)

        print(f"\n📋 NORMALIZATION RESULTS:")

        # Check each section
        sections_to_check = [
            'executive_summary', 'principal_findings', 'temporal_analysis',
            'seasonal_analysis', 'fourier_analysis', 'strategic_synthesis',
            'conclusions', 'heatmap_analysis', 'pca_analysis'
        ]

        all_passed = True

        for section in sections_to_check:
            has_content = section in normalized and normalized[section] and len(str(normalized[section])) > 0

            if section in ['heatmap_analysis', 'pca_analysis']:
                if has_content:
                    print(f"❌ {section}: FOUND CONTENT (should be empty for single-source)")
                    print(f"   Content: '{normalized[section]}'")
                    all_passed = False
                else:
                    print(f"✅ {section}: EMPTY (correct for single-source)")
            else:
                if has_content:
                    print(f"✅ {section}: {len(str(normalized[section]))} characters")
                else:
                    print(f"⚠️  {section}: EMPTY")

        # Test with multi-source (should keep heatmap/PCA)
        print(f"\n" + "=" * 60)
        print("Testing normalization with is_single_source=False...")

        normalized_multi = self.ai_service._normalize_parsed_response(test_response, is_single_source=False)

        print(f"\n📋 MULTI-SOURCE NORMALIZATION RESULTS:")

        for section in ['heatmap_analysis', 'pca_analysis']:
            has_content = section in normalized_multi and normalized_multi[section] and len(str(normalized_multi[section])) > 0

            if has_content:
                print(f"✅ {section}: {len(str(normalized_multi[section]))} characters (correct for multi-source)")
            else:
                print(f"❌ {section}: EMPTY (should have content for multi-source)")
                all_passed = False

        return all_passed

    def test_empty_sections_normalization(self):
        """Test normalization when AI doesn't provide heatmap/PCA sections."""
        print(f"\n" + "=" * 60)
        print("🧪 TESTING DEFAULT SECTION HANDLING")
        print("=" * 60)

        # Test data without heatmap/PCA (AI didn't generate them)
        test_response = {
            "executive_summary": "Executive summary content.",
            "principal_findings": [{"bullet_point": "Finding", "reasoning": "Reason"}],
            "temporal_analysis": "Temporal content.",
            "fourier_analysis": "Fourier content.",
            "strategic_synthesis": "Synthesis content.",
            "conclusions": "Conclusions content."
            # Note: No heatmap_analysis or pca_analysis sections
        }

        print("Testing with missing heatmap/PCA sections...")

        # Test single-source (should get empty defaults)
        normalized = self.ai_service._normalize_parsed_response(test_response, is_single_source=True)

        heatmap_empty = not (normalized.get('heatmap_analysis') and len(str(normalized['heatmap_analysis'])) > 0)
        pca_empty = not (normalized.get('pca_analysis') and len(str(normalized['pca_analysis'])) > 0)

        if heatmap_empty and pca_empty:
            print("✅ Single-source correctly gets empty heatmap/PCA sections")
            return True
        else:
            print(f"❌ Single-source default handling failed")
            print(f"   heatmap_analysis empty: {heatmap_empty}")
            print(f"   pca_analysis empty: {pca_empty}")
            return False

    def run_tests(self):
        """Run all validation tests."""
        print("🔬 SINGLE-SOURCE NORMALIZATION VALIDATION")
        print("=" * 80)

        test1_passed = self.test_single_source_normalization()
        test2_passed = self.test_empty_sections_normalization()

        print(f"\n" + "=" * 80)
        print("📊 TEST RESULTS:")
        print(f"Single-source normalization: {'PASSED' if test1_passed else 'FAILED'}")
        print(f"Default section handling: {'PASSED' if test2_passed else 'FAILED'}")

        overall_success = test1_passed and test2_passed

        if overall_success:
            print("\n✅ ALL TESTS PASSED: Single-source normalization correctly excludes heatmap/PCA")
        else:
            print("\n❌ SOME TESTS FAILED: Single-source normalization needs fixes")

        return overall_success

if __name__ == "__main__":
    tester = DirectSingleSourceTest()
    success = tester.run_tests()
    sys.exit(0 if success else 1)