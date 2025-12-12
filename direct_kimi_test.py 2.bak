#!/usr/bin/env python3
"""
Direct Kimi K2 API Test using standard library
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🚀 DIRECT KIMI K2 API TEST")
print("=" * 50)

# Load environment variables manually
print("🔄 Loading environment variables...")
try:
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                # Remove quotes if present
                value = value.strip('"').strip("'")
                os.environ[key] = value
    print("✅ Environment variables loaded")
except Exception as e:
    print(f"❌ Failed to load .env: {e}")
    exit(1)

# Get API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("❌ GROQ_API_KEY not found in environment")
    exit(1)

print(f"🔑 API Key: {groq_api_key[:15]}...")

# Test database connection
print("\n🗄️ Testing database connection...")
try:
    from database_implementation.precomputed_findings_db import (
        get_precomputed_db_manager,
    )

    db_manager = get_precomputed_db_manager()

    with db_manager.get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) as count FROM precomputed_findings")
        count = cursor.fetchone()["count"]
        print(f"   Database has {count} records")

    print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    exit(1)

# Test Kimi K2 API
print("\n🤖 Testing Kimi K2 API...")

test_prompt = """Analyze trends and patterns for the management tool "Benchmarking" using Google Trends data.

Provide a brief executive analysis with key findings."""

# Prepare request data
data = {
    "messages": [{"role": "user", "content": test_prompt}],
    "model": "moonshotai/kimi-k2-instruct",
    "max_tokens": 1000,
    "temperature": 0.7,
}

# Headers
headers = {
    "Authorization": f"Bearer {groq_api_key}",
    "Content-Type": "application/json",
}

# URL
url = "https://api.groq.com/openai/v1/chat/completions"

try:
    # Create request
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST"
    )

    print("📡 Sending request to Kimi K2...")
    start_time = time.time()

    # Send request
    with urllib.request.urlopen(req, timeout=30) as response:
        response_time = time.time() - start_time

        if response.status == 200:
            result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]

            print("✅ Kimi K2 API test successful!")
            print(f"   Response time: {response_time:.2f} seconds")
            print(f"   Response length: {len(content)} characters")
            print(f"   Response preview:")
            print("   " + content[:150].replace("\n", "\n   ") + "...")

            print("\n🎯 ALL TESTS PASSED!")
            print("\n🚀 Ready for batch processing!")
            print("\nNext steps:")
            print("1. Run real AI batch processing")
            print("2. Replace simulation data with real Kimi K2 analyses")

        else:
            print(f"❌ API test failed: {response.status}")
            error_text = response.read().decode("utf-8")
            print(f"   Error: {error_text}")

except Exception as e:
    print(f"❌ API test failed: {e}")
    import traceback

    traceback.print_exc()
