#!/usr/bin/env python3
"""
Simple validation test to verify the seasonal_analysis fix worked.
This tests the specific fix we made to include seasonal_analysis in single-source analysis.
"""

import sys
import os

# Add the dashboard_app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Load environment variables from .env file
import subprocess

result = subprocess.run(
    [
        "bash",
        "-c",
        "cd /Users/Dimar/Documents/python-code/MTSA/tools-dashboard && source .env && env",
    ],
    capture_output=True,
    text=True,
)
for line in result.stdout.split("\n"):
    if "=" in line and ("GROQ_API_KEY" in line or "OPENROUTER_API_KEY" in line):
        key, value = line.split("=", 1)
        os.environ[key] = value


# Now test the fix
def validate_seasonal_analysis_fix():
    """Validate that seasonal_analysis is now properly included in single-source analysis."""

    print("🔍 Validating seasonal_analysis fix for single-source analysis")
    print("=" * 65)

    # Test the validation logic directly
    from key_findings.unified_ai_service import UnifiedAIService

    # Create a mock AI service to test the parsing logic
    ai_service = UnifiedAIService(
        groq_api_key=os.getenv("GROQ_API_KEY", "test_key"),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", "test_key"),
        config={
            "max_retries": 3,
            "enable_pca_emphasis": True,
            "confidence_threshold": 0.7,
        },
    )

    # Test the validation function with proper content length
    test_result = {
        "executive_summary": "Test executive summary content with sufficient length to pass validation requirements",
        "principal_findings": [
            {
                "bullet_point": "Test finding with detailed reasoning",
                "reasoning": "Test reasoning with comprehensive analysis and strategic implications for business decision making",
            }
        ],
        "temporal_analysis": "Test temporal analysis content with detailed insights about trends, patterns, and strategic timing recommendations for organizational implementation",
        "seasonal_analysis": "Test seasonal analysis content with comprehensive examination of cyclical patterns, quarterly variations, and optimal timing windows for strategic initiatives",  # This should now be required
        "fourier_analysis": "Test fourier analysis content with detailed spectral examination, frequency domain insights, and cyclical pattern recognition for predictive modeling",
        "strategic_synthesis": "Test strategic synthesis content that integrates all analytical findings into coherent business recommendations and actionable strategic guidance",
        "conclusions": "Test conclusions content with comprehensive summary of key findings, strategic recommendations, implementation timing, and risk assessment for decision makers",
    }

    # Test the validation function
    is_valid = ai_service._validate_complete_response(
        test_result, is_single_source=True
    )

    print(f"✅ Test result with all 7 sections:")
    for section, content in test_result.items():
        print(f"   {section}: {'✅ Present' if content else '❌ Missing'}")

    print(f"\n🎯 Validation result: {'✅ PASSED' if is_valid else '❌ FAILED'}")

    # Test with missing seasonal_analysis (should fail)
    test_result_missing = test_result.copy()
    test_result_missing["seasonal_analysis"] = ""

    is_valid_missing = ai_service._validate_complete_response(
        test_result_missing, is_single_source=True
    )

    print(f"\n⚠️  Test result with missing seasonal_analysis:")
    for section, content in test_result_missing.items():
        print(f"   {section}: {'✅ Present' if content else '❌ Missing'}")

    print(
        f"\n🎯 Validation result (missing seasonal): {'❌ FAILED (as expected)' if not is_valid_missing else '❌ UNEXPECTED PASS'}"
    )

    # Test the normalization function
    normalized = ai_service._normalize_parsed_response(
        test_result, is_single_source=True
    )

    print(f"\n🔧 Normalized result keys:")
    for key in sorted(normalized.keys()):
        content = normalized[key]
        if isinstance(content, str):
            status = "✅ Present" if content else "❌ Empty"
            print(f"   {key}: {status} ({len(content)} chars)")
        elif isinstance(content, list):
            status = "✅ Present" if content else "❌ Empty"
            print(f"   {key}: {status} ({len(content)} items)")
        else:
            print(f"   {key}: {type(content).__name__}")

    # Verify seasonal_analysis is included
    has_seasonal = "seasonal_analysis" in normalized and normalized["seasonal_analysis"]

    print(f"\n📊 Final Assessment:")
    print(
        f"   ✅ seasonal_analysis in required sections: {'✅ YES' if is_valid else '❌ NO'}"
    )
    print(
        f"   ✅ seasonal_analysis properly normalized: {'✅ YES' if has_seasonal else '❌ NO'}"
    )
    print(
        f"   ✅ Validation logic working correctly: {'✅ YES' if is_valid and not is_valid_missing else '❌ NO'}"
    )

    overall_success = is_valid and not is_valid_missing and has_seasonal

    print(
        f"\n🎉 Overall Result: {'✅ SUCCESS - Fix is working!' if overall_success else '❌ FAILURE - Fix needs adjustment'}"
    )

    return overall_success


if __name__ == "__main__":
    success = validate_seasonal_analysis_fix()
    sys.exit(0 if success else 1)
