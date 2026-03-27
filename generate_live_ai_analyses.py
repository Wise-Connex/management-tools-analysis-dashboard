#!/usr/bin/env python3
"""
Generate Live AI Analyses for 30 Combinations

This script triggers actual live AI generation using Groq API for the 30 combinations
and stores the real AI responses in the database.
"""

import os
import sys
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Add dashboard_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Import required components
from key_findings.key_findings_service import get_key_findings_service
from database_implementation.precomputed_findings_db import get_precomputed_db_manager

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


class LiveAIGenerator:
    """Generates live AI analyses for combinations."""

    def __init__(self):
        self.db_manager = get_precomputed_db_manager()
        self.start_time = None
        self.results = {
            "total_combinations": 0,
            "successful": 0,
            "failed": 0,
            "ai_calls_made": 0,
            "cost_estimate": 0.0,
            "details": [],
        }

    def get_test_combinations(self) -> List[Dict[str, Any]]:
        """Get a subset of combinations for live AI testing."""

        # Test with a smaller set first to verify AI integration works
        test_combinations = [
            # Single source tests
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends"],
                "language": "es",
                "category": "test_single",
            },
            {
                "tool": "Competencias Centrales",
                "sources": ["Google Trends"],
                "language": "en",
                "category": "test_single",
            },
            # Multi-source tests
            {
                "tool": "Benchmarking",
                "sources": ["Google Trends", "Google Books"],
                "language": "es",
                "category": "test_multi",
            },
            {
                "tool": "Experiencia del Cliente",
                "sources": ["Bain Usability", "Bain Satisfaction"],
                "language": "en",
                "category": "test_multi",
            },
        ]

        return test_combinations

    async def generate_live_ai_analysis(
        self, combination: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate live AI analysis for a combination."""

        tool_name = combination["tool"]
        sources = combination["sources"]
        language = combination["language"]
        category = combination["category"]

        print(
            f"🧠 Generating live AI analysis: {tool_name} + {len(sources)} sources ({language})"
        )

        try:
            # Initialize key findings service
            key_findings_service = get_key_findings_service(
                self.db_manager,
                os.getenv("GROQ_API_KEY", ""),
                os.getenv("OPENROUTER_API_KEY", ""),
                {},
            )

            # Generate the analysis using force_refresh to ensure live AI
            start_time = datetime.now()

            result = await key_findings_service.generate_key_findings(
                tool_name=tool_name,
                selected_sources=sources,
                language=language,
                force_refresh=True,  # Force live AI generation
            )

            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()

            # Check if we got actual AI content
            if result and isinstance(result, dict):
                # Count AI calls made
                self.results["ai_calls_made"] += 1

                print(f"✅ Live AI generated: {tool_name} in {generation_time:.1f}s")

                return {
                    "success": True,
                    "tool": tool_name,
                    "sources": sources,
                    "language": language,
                    "category": category,
                    "generation_time": generation_time,
                    "has_ai_content": bool(result.get("content")),
                    "content_preview": str(result.get("content", {}))[:200] + "..."
                    if result.get("content")
                    else "No content",
                    "timestamp": start_time.isoformat(),
                }
            else:
                raise Exception("No valid AI content generated")

        except Exception as e:
            print(f"❌ Live AI failed for {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
                "sources": sources,
                "language": language,
                "category": category,
            }

    async def generate_all_combinations(self):
        """Generate live AI analyses for test combinations."""

        print("🚀 Starting Live AI Generation for Test Combinations")
        print("=" * 60)

        # Verify API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "GROQ_API_KEY_PLACEHOLDER":
            print("❌ GROQ_API_KEY not configured or invalid")
            print("   Please ensure GROQ_API_KEY is set in your .env file")
            return

        print(f"✅ API Key configured: {api_key[:20]}...")

        self.start_time = datetime.now()
        combinations = self.get_test_combinations()
        self.results["total_combinations"] = len(combinations)

        print(f"📊 Processing {len(combinations)} test combinations...")

        for i, combination in enumerate(combinations, 1):
            print(f"\n📊 Processing combination {i}/{len(combinations)}")
            print(f"   Category: {combination['category']}")
            print(f"   Tool: {combination['tool']}")
            print(
                f"   Sources: {len(combination['sources'])} ({combination['sources']})"
            )
            print(f"   Language: {combination['language']}")

            # Generate the combination
            result = await self.generate_live_ai_analysis(combination)

            # Update results
            self.results["details"].append(result)

            if result["success"]:
                self.results["successful"] += 1
                self.results["cost_estimate"] += 0.03  # Estimated cost per AI call
            else:
                self.results["failed"] += 1

            # Progress update
            progress = (i / len(combinations)) * 100
            print(
                f"   Progress: {i}/{len(combinations)} ({progress:.1f}%) | Success: {self.results['successful']} | Failed: {self.results['failed']}"
            )

            # Add delay between calls to avoid rate limiting
            if i < len(combinations):
                print("   ⏳ Waiting 2 seconds before next AI call...")
                await asyncio.sleep(2)

        # Final statistics
        self.results["actual_time"] = round(
            (datetime.now() - self.start_time).total_seconds() / 60, 1
        )

        self.print_final_summary()
        self.save_results()

    def print_final_summary(self):
        """Print the final generation summary."""

        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds() / 60

        print("\n" + "=" * 80)
        print("🧠 LIVE AI GENERATION COMPLETE")
        print("=" * 80)

        print(f"📊 SUMMARY STATISTICS:")
        print(f"   Total combinations: {self.results['total_combinations']}")
        print(f"   Successful: {self.results['successful']}")
        print(f"   Failed: {self.results['failed']}")
        print(f"   AI calls made: {self.results['ai_calls_made']}")
        print(
            f"   Success rate: {(self.results['successful'] / self.results['total_combinations']) * 100:.1f}%"
        )

        print(f"\n💰 COST & TIME:")
        print(f"   Estimated cost: ${self.results['cost_estimate']:.2f}")
        print(f"   Actual time: {total_duration:.1f} minutes")

        print(f"\n🔍 GROQ CONSOLE VERIFICATION:")
        print(
            f"   You should see {self.results['ai_calls_made']} API calls in your Groq console"
        )
        print(f"   Check: https://console.groq.com/usage")

        print("=" * 80)

    def save_results(self):
        """Save generation results to file."""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"live_ai_generation_results_{timestamp}.json"

        # Add metadata
        self.results["generation_started"] = self.start_time.isoformat()
        self.results["generation_completed"] = datetime.now().isoformat()
        self.results["duration_minutes"] = round(
            (datetime.now() - self.start_time).total_seconds() / 60, 1
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"💾 Results saved to: {filename}")


async def main():
    """Main execution function."""

    print("🧠 Live AI Generator for Management Tools Analysis")
    print("=" * 60)

    # Initialize and run generator
    generator = LiveAIGenerator()
    await generator.generate_all_combinations()


if __name__ == "__main__":
    asyncio.run(main())
