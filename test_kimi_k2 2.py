#!/usr/bin/env python3
"""
Simple Kimi K2 Test and Batch Processing
Direct test of Kimi K2 API without complex dependencies.
"""

import os
import sys
import json
import asyncio
import aiohttp
import time
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

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
    sys.exit(1)

# Get API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("❌ GROQ_API_KEY not found in environment")
    sys.exit(1)

print(f"🔑 API Key found: {groq_api_key[:15]}...")

# Test database connection
print("\\n🗄️ Testing database connection...")
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
    sys.exit(1)

# Test Kimi K2 API
print("\\n🤖 Testing Kimi K2 API...")


async def test_kimi_k2():
    test_prompt = """Analyze trends and patterns for the management tool "Benchmarking" using Google Trends data.

Provide a brief executive analysis with key findings."""

    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "messages": [{"role": "user", "content": test_prompt}],
        "model": "moonshotai/kimi-k2-instruct",
        "max_tokens": 1000,
        "temperature": 0.7,
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result["choices"][0]["message"]["content"]
                    print("✅ Kimi K2 API test successful!")
                    print(f"   Response length: {len(content)} characters")
                    print(f"   Response preview: {content[:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API test failed: {response.status}")
                    print(f"   Error: {error_text}")
                    return False
        except Exception as e:
            print(f"❌ API test failed: {e}")
            return False


# Run the test
if __name__ == "__main__":
    success = asyncio.run(test_kimi_k2())

    if success:
        print("\\n🎯 All tests passed! Ready for real batch processing.")
        print("\\n🚀 Next step: Run the full batch processing")
        print("   python3 real_ai_batch_processor.py --full")
    else:
        print("\\n❌ Tests failed. Cannot proceed with batch processing.")
