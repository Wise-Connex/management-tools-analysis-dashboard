#!/usr/bin/env python3
"""
Groq API Activity Monitor
Confirms API calls are being made by checking your Groq usage.
"""

import os
import sys
from pathlib import Path
import time

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔍 GROQ API ACTIVITY MONITOR")
print("=" * 50)

# Load environment
try:
    with open("../.env", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                value = value.strip('"').strip("'")
                os.environ[key] = value
except Exception as e:
    print(f"❌ Failed to load .env: {e}")
    sys.exit(1)

# Test API call
print("🧪 Testing Groq API call...")
try:
    from groq import Groq

    groq_api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key)

    start_time = time.time()

    # Simple test call
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello"}],
        model="moonshotai/kimi-k2-instruct",
        max_tokens=10,
    )

    api_time = time.time() - start_time

    print("✅ API CALL SUCCESSFUL!")
    print(f"⏱️ Response time: {api_time:.1f} seconds")
    print(f"📊 Model: Kimi K2 (moonshotai/kimi-k2-instruct)")
    print(f"💡 Content: {chat_completion.choices[0].message.content}")

    print("\n🎯 CONFIRMATION:")
    print("This API call should now appear in your Groq console!")
    print("If you don't see it, try:")
    print("1. Refreshing the Groq console")
    print("2. Checking 'Recent Activity' section")
    print("3. Waiting a few minutes for the request to appear")

except Exception as e:
    print(f"❌ API call failed: {e}")

print(f"\n📋 CURRENT BATCH STATUS:")
print("Your batch processor should show similar successful API calls")
print("If you see ✅ symbols and cost tracking, the calls are working!")
print("The Groq console might just have a delay in showing them.")
