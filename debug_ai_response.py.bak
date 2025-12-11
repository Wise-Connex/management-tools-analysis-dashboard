#!/usr/bin/env python3
"""Debug script to check AI response content."""

import sys
import os
import asyncio
import json
from datetime import datetime

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

from key_findings.key_findings_service import get_key_findings_service
from database import get_database_manager
from config import get_config


async def debug_ai_response():
    """Debug the AI response to see what sections are generated."""

    print("🔍 Debugging AI response for Calidad Total + Google Trends...")

    config = get_config()
    db_manager = get_database_manager()
    key_findings_service = get_key_findings_service(
        db_manager=db_manager,
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
        config={
            "max_retries": 3,
            "enable_pca_emphasis": True,
            "confidence_threshold": 0.7,
        },
    )

    result = await key_findings_service.generate_key_findings(
        tool_name="Calidad Total",
        selected_sources=["Google Trends"],
        language="es",
        force_refresh=True,
        source_display_names=["Google Trends"],
    )

    if result.get("success") and result.get("data"):
        data = result["data"]
        print(f"\n✅ AI query successful!")
        print(f"📊 Response time: {result.get('response_time_ms', 0)}ms")
        print(f"🤖 Model used: {data.get('model_used', 'unknown')}")
        print(f"📈 Confidence score: {data.get('confidence_score', 0):.2f}")

        print(f"\n📋 All sections in response:")
        for key in sorted(data.keys()):
            content = data.get(key, "")
            if isinstance(content, str):
                length = len(content)
                preview = (
                    content[:100].replace("\n", " ") + "..." if content else "EMPTY"
                )
                print(f"   {key}: {length:,} chars - {preview}")
            else:
                print(f"   {key}: {type(content).__name__} - {str(content)[:100]}...")

        # Check specific sections
        sections_to_check = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

        print(f"\n🔍 Detailed section analysis:")
        for section in sections_to_check:
            content = data.get(section, "")
            if content and len(str(content)) > 10:
                print(f"   ✅ {section}: {len(str(content)):,} characters")
                # Show first few lines
                lines = str(content).split("\n")[:3]
                for line in lines:
                    if line.strip():
                        print(f"      {line.strip()}")
            else:
                print(f"   ❌ {section}: MISSING or empty")

        # Save the full response for detailed analysis
        output_file = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/ai_analysis_exports/debug_ai_response.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        debug_data = {
            "query_metadata": {
                "tool_name": "Calidad Total",
                "selected_sources": ["Google Trends"],
                "language": "es",
                "generated_at": datetime.now().isoformat(),
                "response_time_ms": result.get("response_time_ms", 0),
                "model_used": data.get("model_used", "unknown"),
                "confidence_score": data.get("confidence_score", 0),
            },
            "ai_response": {k: v for k, v in data.items() if isinstance(v, str)},
            "section_lengths": {
                section: len(str(data.get(section, "")))
                for section in sections_to_check
            },
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(debug_data, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Full debug data saved to: {output_file}")

    else:
        print(f"\n❌ AI query failed: {result.get('error', 'Unknown error')}")


if __name__ == "__main__":
    asyncio.run(debug_ai_response())
