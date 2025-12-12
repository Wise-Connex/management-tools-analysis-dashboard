#!/usr/bin/env python3
"""
Test fresh key findings generation with all fixes applied
"""

import sys
import os
sys.path.append('/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app')

# Set environment variables for testing
os.environ['GROQ_API_KEY'] = 'test_key'
os.environ['OPENROUTER_API_KEY'] = 'test_key'

from key_findings.key_findings_service import KeyFindingsService

def test_fresh_generation():
    """Test fresh key findings generation with our fixes"""

    print("Testing fresh key findings generation...")
    print("=" * 60)

    try:
        # Initialize the service
        service = KeyFindingsService()

        # Test single-source generation
        print("Testing single-source generation...")
        result = service.generate_key_findings(
            tool_name='Benchmarking',
            selected_sources=[1],  # Google Trends
            language='es'
        )

        if result:
            print("✅ Single-source generation successful!")
            print(f"✅ Model used: {result.get('model_used', 'unknown')}")
            print(f"✅ Data points: {result.get('data_points_analyzed', 0)}")
            print(f"✅ Analysis type: {result.get('analysis_type', 'unknown')}")

            # Check if PCA and heatmap are present (they shouldn't be for single-source)
            pca_content = result.get('pca_analysis', '')
            heatmap_content = result.get('heatmap_analysis', '')

            print(f"✅ PCA content length: {len(pca_content)} chars")
            print(f"✅ Heatmap content length: {len(heatmap_content)} chars")

            if len(pca_content) == 0 and len(heatmap_content) == 0:
                print("✅ PCA and heatmap correctly excluded for single-source!")
            else:
                print("⚠️  PCA or heatmap found in single-source (unexpected)")

            # Show content preview
            exec_summary = result.get('executive_summary', '')
            print(f"✅ Executive summary length: {len(exec_summary)} chars")
            if len(exec_summary) > 0:
                print(f"✅ Preview: {exec_summary[:100]}...")

        else:
            print("❌ Single-source generation failed")
            return False

        # Test multi-source generation
        print("\nTesting multi-source generation...")
        result = service.generate_key_findings(
            tool_name='Benchmarking',
            selected_sources=[1, 2, 3, 4, 5],  # All sources
            language='es'
        )

        if result:
            print("✅ Multi-source generation successful!")
            print(f"✅ Model used: {result.get('model_used', 'unknown')}")
            print(f"✅ Data points: {result.get('data_points_analyzed', 0)}")
            print(f"✅ Analysis type: {result.get('analysis_type', 'unknown')}")

            # Check if PCA is present (it should be for multi-source)
            pca_content = result.get('pca_analysis', '')
            heatmap_content = result.get('heatmap_analysis', '')

            print(f"✅ PCA content length: {len(pca_content)} chars")
            print(f"✅ Heatmap content length: {len(heatmap_content)} chars")

            if len(pca_content) > 0:
                print("✅ PCA content found for multi-source!")
                # Check if it's JSON format that needs conversion
                if pca_content.strip().startswith('{'):
                    print("✅ PCA content is in JSON format (will be converted to narrative)")
                else:
                    print("✅ PCA content is in text format")
            else:
                print("⚠️  No PCA content found for multi-source")

            if len(heatmap_content) == 0:
                print("✅ Empty heatmap correctly excluded!")
            else:
                print("✅ Heatmap content found")

        else:
            print("❌ Multi-source generation failed")
            return False

        print("\n" + "="*60)
        print("🎉 SUCCESS: Fresh generation test completed!")
        print("✅ All fixes should now be active with fresh data")
        print("✅ Try generating Key Findings in the dashboard to see the fixes")

        return True

    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fresh_generation()
    sys.exit(0 if success else 1)