#!/usr/bin/env python3
"""
Direct AI Test - Verify Groq API is Working

This script makes a direct call to Groq API to verify connectivity and generate real AI content.
"""

import os
import sys
import asyncio
import json
from datetime import datetime

# Add dashboard_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Import AI service directly
from key_findings.unified_ai_service import UnifiedAIService

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


async def test_direct_ai():
    """Test direct AI generation."""

    print("🧠 Direct AI Test - Groq API Verification")
    print("=" * 50)

    # Verify API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "GROQ_API_KEY_PLACEHOLDER":
        print("❌ GROQ_API_KEY not configured or invalid")
        return

    print(f"✅ API Key: {api_key[:20]}...")

    # Initialize AI service
    ai_service = UnifiedAIService(groq_api_key=api_key, openrouter_api_key="")

    print("🔧 AI Service initialized")

    # Simple test prompt
    test_prompt = """
    Analyze Benchmarking as a management tool using Google Trends data.
    
    Provide a brief analysis in Spanish with these sections:
    1. Executive Summary (2-3 sentences)
    2. Principal Findings (2-3 bullet points)
    3. Temporal Analysis (2-3 sentences about trends)
    4. Conclusions (2-3 sentences)
    
    Keep each section concise but informative.
    """

    print("📡 Making direct AI call to Groq...")
    start_time = datetime.now()

    try:
        # Make the AI call
        result = await ai_service.generate_analysis(
            prompt=test_prompt, language="es", is_single_source=True
        )

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print(f"✅ AI Response received in {duration:.1f} seconds!")
        print(f"📊 Model used: {result.get('model_used', 'Unknown')}")
        print(f"🔧 Provider: {result.get('provider_used', 'Unknown')}")
        print(f"🧮 Tokens used: {result.get('token_count', 0)}")

        # Display content preview
        content = result.get("content", {})
        if content:
            print(f"\n📋 Content Preview:")
            print(
                f"   Executive Summary: {content.get('executive_summary', 'N/A')[:100]}..."
            )
            print(
                f"   Principal Findings: {len(content.get('principal_findings', []))} items"
            )
            print(
                f"   Has temporal analysis: {'Yes' if content.get('temporal_analysis') else 'No'}"
            )

        print(f"\n🎯 SUCCESS: Real AI call made to Groq!")
        print(f"🔍 Check your Groq console: https://console.groq.com/usage")

        # Save result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"direct_ai_test_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "test_timestamp": timestamp,
                    "duration_seconds": duration,
                    "success": True,
                    "model_used": result.get("model_used"),
                    "provider_used": result.get("provider_used"),
                    "token_count": result.get("token_count"),
                    "content_preview": {
                        "executive_summary": content.get("executive_summary", "")[:200],
                        "principal_findings_count": len(
                            content.get("principal_findings", [])
                        ),
                        "has_temporal_analysis": bool(content.get("temporal_analysis")),
                    },
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"💾 Test results saved to: {filename}")

    except Exception as e:
        print(f"❌ AI call failed: {e}")
        print(f"🔍 Check error details and Groq console")

        # Save error result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"direct_ai_test_{timestamp}.json"

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {"test_timestamp": timestamp, "success": False, "error": str(e)},
                f,
                indent=2,
            )

        print(f"💾 Error details saved to: {filename}")


async def main():
    """Main execution."""
    await test_direct_ai()


if __name__ == "__main__":
    asyncio.run(main())
