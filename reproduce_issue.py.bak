
import os
import sys
import asyncio
import time
from dashboard_app.app import key_findings_service, initialize_key_findings_service, run_async_in_sync_context
from dashboard_app.key_findings.key_findings_service import KeyFindingsService

# Mock configuration
os.environ["GROQ_API_KEY"] = "mock_key"
os.environ["OPENROUTER_API_KEY"] = "mock_key"

def test_generation():
    print("🚀 Starting reproduction test...")
    
    # Initialize service
    print("1. Initializing service...")
    initialize_key_findings_service()
    
    if key_findings_service is None:
        print("❌ Service failed to initialize")
        return
        
    print("✅ Service initialized")
    
    # Mock parameters
    selected_tool = "Google Trends"
    selected_sources = ["Google Trends"]
    language = "es"
    
    print(f"2. Calling generate_key_findings for {selected_tool}...")
    
    try:
        # Simulate the callback logic
        start_time = time.time()
        result = run_async_in_sync_context(
            key_findings_service.generate_key_findings,
            tool_name=selected_tool,
            selected_sources=selected_sources,
            language=language,
            force_refresh=True
        )
        duration = time.time() - start_time
        
        print(f"✅ Call completed in {duration:.2f}s")
        print(f"Result keys: {result.keys() if result else 'None'}")
        
        if result and not result.get("success", False):
            print(f"❌ Result indicates failure: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Exception caught: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure we are in the right directory
    sys.path.append(os.getcwd())
    test_generation()
