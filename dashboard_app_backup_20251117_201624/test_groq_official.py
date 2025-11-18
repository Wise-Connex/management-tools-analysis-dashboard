#!/usr/bin/env python3
"""
Official Groq Client Test
Using the sample code from Groq documentation.
"""

import os
import sys
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("🚀 OFFICIAL GROQ CLIENT TEST")
print("=" * 50)

# Load environment variables manually
print("🔄 Loading environment variables...")
try:
    with open("../.env", "r") as f:  # Go up one level to find .env
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

# Import Groq client
print("\n📦 Importing Groq client...")
try:
    from groq import Groq

    print("✅ Groq client imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Groq: {e}")
    exit(1)

# Check API key
groq_api_key = os.environ.get("GROQ_API_KEY")
if not groq_api_key:
    print("❌ GROQ_API_KEY not found in environment")
    exit(1)

print(f"🔑 API Key: {groq_api_key[:15]}...")

# Create Groq client
print("\n🤖 Creating Groq client...")
try:
    client = Groq(api_key=groq_api_key)
    print("✅ Groq client created successfully")
except Exception as e:
    print(f"❌ Failed to create Groq client: {e}")
    exit(1)

# Test simple query using sample prompt
print("\n🧪 Testing simple query...")
test_prompt = """Analyze trends and patterns for the management tool "Benchmarking" using Google Trends data.

Provide a brief executive analysis with key findings."""

try:
    print("📡 Sending request to Kimi K2...")
    start_time = time.time()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": test_prompt,
            }
        ],
        model="moonshotai/kimi-k2-instruct",
    )

    response_time = time.time() - start_time

    # Extract response
    response_content = chat_completion.choices[0].message.content

    print("✅ Kimi K2 API test successful!")
    print(f"   Response time: {response_time:.2f} seconds")
    print(f"   Response length: {len(response_content)} characters")
    print(f"   Response preview:")
    print("   " + response_content[:200].replace("\n", "\n   ") + "...")

    print("\n🎯 GROQ CLIENT TEST PASSED!")
    print("\n🚀 Ready for batch processing!")

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

    print("\n📋 ALL SYSTEMS READY!")
    print("Next: Run batch processing with real Kimi K2 AI")

except Exception as e:
    print(f"❌ Groq API test failed: {e}")
    import traceback

    traceback.print_exc()
