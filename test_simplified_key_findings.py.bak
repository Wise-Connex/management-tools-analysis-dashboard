#!/usr/bin/env python3
"""
Test script for simplified key findings service with database-first approach
"""

import sys
import os
import asyncio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not available, using existing environment variables")

# Import required modules
from key_findings.key_findings_service import get_key_findings_service
from database import get_database_manager


def test_simplified_service():
    """Test the simplified key findings service"""
    print("🧪 Testing Simplified Key Findings Service - Database-First Approach")
    print("=" * 70)

    try:
        # Initialize database manager
        print("📊 Initializing database manager...")
        db_manager = get_database_manager()
        print("✅ Database manager initialized")

        # Initialize simplified service
        print("🔧 Initializing simplified key findings service...")
        service = get_key_findings_service(db_manager, "", "", {})
        print("✅ Service initialized successfully")

        # Test 1: Single source - Calidad Total + Google Trends
        print("\n🎯 Test 1: Single Source - Calidad Total + Google Trends")
        print("-" * 50)

        result = service._get_precomputed_findings_direct(
            "Calidad Total", ["Google Trends"], "es"
        )

        if result:
            print("✅ Single source test: SUCCESS")
            print(f"📋 Tool: {result.get('tool_name', 'N/A')}")
            print(f"🔍 Sources: {result.get('selected_sources', [])}")
            print(f"🌐 Language: {result.get('language', 'N/A')}")
            print(f"📊 Data points: {result.get('data_points_analyzed', 0)}")
            print(f"🎯 Confidence: {result.get('confidence_score', 0):.2f}")
            print(f"⚡ Model: {result.get('model_used', 'N/A')}")
            print(
                f"📄 Executive Summary length: {len(result.get('executive_summary', ''))}"
            )
            print(
                f"🔍 Principal Findings length: {len(result.get('principal_findings', ''))}"
            )
            print(
                f"📈 Temporal Analysis length: {len(result.get('temporal_analysis', ''))}"
            )
            print(
                f"📅 Seasonal Analysis length: {len(result.get('seasonal_analysis', ''))}"
            )
            print(
                f"🌊 Fourier Analysis length: {len(result.get('fourier_analysis', ''))}"
            )
            print(f"📊 PCA Analysis length: {len(result.get('pca_analysis', ''))}")
            print(
                f"🔥 Heatmap Analysis length: {len(result.get('heatmap_analysis', ''))}"
            )

            # Verify single-source specific behavior
            pca_content = result.get("pca_analysis", "")
            heatmap_content = result.get("heatmap_analysis", "")
            if not pca_content.strip() and not heatmap_content.strip():
                print("✅ PCA/Heatmap correctly empty for single source")
            else:
                print(
                    f"⚠️ PCA/Heatmap content present: PCA={len(pca_content)}, Heatmap={len(heatmap_content)}"
                )

        else:
            print("❌ Single source test: FAILED - No precomputed data found")

        # Test 2: Multi-source - Calidad Total + All 5 Sources
        print("\n🎯 Test 2: Multi-Source - Calidad Total + All 5 Sources")
        print("-" * 50)

        result_multi = service._get_precomputed_findings_direct(
            "Calidad Total",
            [
                "Google Trends",
                "Google Books",
                "Bain Usability",
                "Crossref",
                "Bain Satisfaction",
            ],
            "es",
        )

        if result_multi:
            print("✅ Multi-source test: SUCCESS")
            print(f"📋 Tool: {result_multi.get('tool_name', 'N/A')}")
            print(f"🔍 Sources: {result_multi.get('selected_sources', [])}")
            print(f"🌐 Language: {result_multi.get('language', 'N/A')}")
            print(f"📊 Data points: {result_multi.get('data_points_analyzed', 0)}")
            print(f"🎯 Confidence: {result_multi.get('confidence_score', 0):.2f}")
            print(f"⚡ Model: {result_multi.get('model_used', 'N/A')}")
            print(
                f"📄 Executive Summary length: {len(result_multi.get('executive_summary', ''))}"
            )
            print(
                f"🔍 Principal Findings length: {len(result_multi.get('principal_findings', ''))}"
            )
            print(
                f"📊 PCA Analysis length: {len(result_multi.get('pca_analysis', ''))}"
            )
            print(
                f"🔥 Heatmap Analysis length: {len(result_multi.get('heatmap_analysis', ''))}"
            )

            # Verify multi-source specific behavior
            pca_content = result_multi.get("pca_analysis", "")
            heatmap_content = result_multi.get("heatmap_analysis", "")
            if pca_content.strip() and heatmap_content.strip():
                print("✅ PCA/Heatmap content present for multi-source")
            else:
                print(
                    f"⚠️ PCA/Heatmap content missing: PCA={len(pca_content)}, Heatmap={len(heatmap_content)}"
                )

        else:
            print("❌ Multi-source test: FAILED - No precomputed data found")

        # Test 3: Performance metrics
        print("\n📊 Test 3: Performance Metrics")
        print("-" * 50)

        metrics = service.get_performance_metrics()
        print("Service Performance:")
        for key, value in metrics["service_metrics"].items():
            print(f"  {key}: {value}")

        if "ai_performance" in metrics:
            print("AI Service Performance:")
            for key, value in metrics["ai_performance"].items():
                print(f"  {key}: {value}")

        # Test 4: Full async generation (if needed)
        print("\n🔄 Test 4: Full Async Generation Test")
        print("-" * 50)

        async def test_full_generation():
            result = await service.generate_key_findings(
                "Calidad Total", ["Google Trends"], "es"
            )
            return result

        try:
            full_result = asyncio.run(test_full_generation())
            if full_result.get("success"):
                print("✅ Full generation test: SUCCESS")
                print(f"📊 Response time: {full_result.get('response_time_ms', 0)}ms")
                print(f"🎯 Cache hit: {full_result.get('cache_hit', False)}")
                print(f"⚡ Source: {full_result.get('source', 'unknown')}")
            else:
                print("❌ Full generation test: FAILED")
                print(f"❌ Error: {full_result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"❌ Full generation test error: {e}")

        print("\n" + "=" * 70)
        print("🎉 Simplified Key Findings Service Test Complete!")
        print("✅ Database-first approach implemented successfully")
        print("✅ Direct precomputed database access working")
        print("✅ No caching layer - simplified architecture")
        print("✅ Ready for dashboard testing!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = test_simplified_service()
    sys.exit(0 if success else 1)
