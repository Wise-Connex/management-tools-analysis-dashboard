#!/usr/bin/env python3
"""
Store Benchmarking single-source analysis in the precomputed findings database
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'dashboard_app'))

async def store_benchmarking_analysis():
    """Generate and store Benchmarking analysis in the database"""

    print("🗃️ STORING BENCHMARKING ANALYSIS IN DATABASE")
    print("=" * 60)

    # Import required modules
    from key_findings.key_findings_service import KeyFindingsService
    from key_findings.database_manager import KeyFindingsDBManager
    from database import get_database_manager

    # Initialize both database managers
    print("🗃️ Initializing database managers...")

    # Main database manager for Google Trends data
    main_db_manager = get_database_manager()

    # Key Findings database manager with local path
    local_db_path = os.path.join(os.path.dirname(__file__), 'dashboard_app', 'data', 'key_findings.db')
    kf_db_manager = KeyFindingsDBManager(db_path=local_db_path)

    # Initialize the service with the main database manager and local path config
    print("🔍 Initializing Key Findings service...")
    config = {
        "key_findings_db_path": local_db_path
    }
    key_findings_service = KeyFindingsService(
        db_manager=main_db_manager,
        groq_api_key=None,
        openrouter_api_key=None,
        config=config
    )

    # Parameters for the analysis
    tool_name = "Benchmarking"
    selected_sources = [1]  # Google Trends ID
    language = "es"

    print(f"📊 Generating analysis for: {tool_name}")
    print(f"📊 Source IDs: {selected_sources}")
    print(f"📊 Language: {language}")

    try:
        # Step 1: Generate the analysis
        print("\n🚀 Step 1: Generating AI analysis...")

        # Force refresh to get fresh AI content
        analysis_result = await key_findings_service.generate_key_findings(
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            force_refresh=True
        )

        if not analysis_result.get('success'):
            print("❌ Failed to generate analysis")
            return False

        print("✅ Analysis generated successfully")
        print(f"📊 Generated analysis keys: {list(analysis_result['data'].keys())}")

        # Step 2: Store in precomputed findings database
        print("\n💾 Step 2: Storing in precomputed findings database...")

        # Calculate the hash for the query
        import hashlib
        query_string = f"{tool_name}_{','.join(map(str, selected_sources))}_{language}"
        query_hash = hashlib.md5(query_string.encode()).hexdigest()

        print(f"🔑 Query string: {query_string}")
        print(f"🔑 Query hash: {query_hash}")

        # Prepare the data for storage
        report_data = analysis_result['data']

        # Extract the JSON fields that need to be stored
        storage_data = {
            'tool_name': tool_name,
            'spanish_tool_name': tool_name,
            'sources_text': 'Google Trends',
            'language': language,
            'executive_summary': report_data.get('executive_summary', ''),
            'principal_findings': report_data.get('principal_findings', ''),
            'temporal_analysis': report_data.get('temporal_analysis', ''),
            'seasonal_analysis': report_data.get('seasonal_analysis', ''),
            'fourier_analysis': report_data.get('fourier_analysis', ''),
            'strategic_synthesis': report_data.get('strategic_synthesis', ''),
            'conclusions': report_data.get('conclusions', ''),
            'model_used': report_data.get('model_used', 'unknown'),
            'response_time_ms': report_data.get('api_latency_ms', 0),
            'confidence_score': report_data.get('confidence_score', 0.0),
            'data_points_analyzed': report_data.get('data_points_analyzed', 0),
            'sources_count': len(selected_sources),
            'analysis_depth': report_data.get('analysis_depth', 'comprehensive'),
            'report_type': report_data.get('report_type', 'single_source'),
            'analysis_type': report_data.get('analysis_type', 'temporal_spectral_strategic'),
            'generated_at': '2025-11-27T22:55:00Z'
        }

        # Store in the database
        success = kf_db_manager.store_precomputed_finding(
            query_hash=query_hash,
            tool_name=tool_name,
            spanish_tool_name=tool_name,
            sources_text='Google Trends',
            language=language,
            analysis_data=storage_data
        )

        if success:
            print("✅ Successfully stored in precomputed findings database")

            # Step 3: Verify the storage
            print("\n🔍 Step 3: Verifying storage...")

            # Retrieve the stored data
            stored_data = kf_db_manager.get_precomputed_finding(
                tool_name=tool_name,
                sources_text='Google Trends',
                language=language
            )

            if stored_data:
                print("✅ Successfully retrieved stored data")
                print(f"📊 Retrieved keys: {list(stored_data.keys())}")

                # Check section lengths
                sections = ['executive_summary', 'principal_findings', 'seasonal_analysis',
                           'temporal_analysis', 'fourier_analysis', 'strategic_synthesis', 'conclusions']

                print("\n📊 Section analysis:")
                total_sections = 0
                for section in sections:
                    content = stored_data.get(section, '')
                    length = len(str(content)) if content else 0
                    has_content = length > 50
                    status = '✅' if has_content else '❌'
                    print(f"  {status} {section}: {length} characters")
                    if has_content:
                        total_sections += 1

                print(f"\n📊 Total sections with content: {total_sections}/7")

                if total_sections >= 5:
                    print("🎉 SUCCESS: Analysis stored and ready for dashboard retrieval!")
                    print("\n📋 Next steps:")
                    print("1. Go to the dashboard (http://localhost:8052)")
                    print("2. Select 'Benchmarking' tool")
                    print("3. Select 'Google Trends' source")
                    print("4. Click 'Hallazgos Principales' button")
                    print("5. The analysis should now load instantly from the database")
                else:
                    print("⚠️ WARNING: Some sections may be missing content")

                return True
            else:
                print("❌ Failed to retrieve stored data")
                return False
        else:
            print("❌ Failed to store in database")
            return False

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(store_benchmarking_analysis())
    if result:
        print("\n🎉 Operation completed successfully!")
    else:
        print("\n❌ Operation failed!")