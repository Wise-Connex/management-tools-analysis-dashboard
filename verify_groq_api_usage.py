#!/usr/bin/env python3
"""
Live AI Generation for Calidad Total Combinations using Groq API

Performs actual live AI generation using real API calls to Groq for:
1. Calidad Total + Google Trends (single-source)
2. Calidad Total + All 5 sources (multi-source)
3. Calidad Total + Google Books, Bain Satisfaction (multi-source)

This will make actual API calls to Groq and generate fresh AI content.
"""

import asyncio
import os
import time
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure detailed logging for API tracking
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("groq_api_generation.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Set up Groq API key with detailed tracking
os.environ["GROQ_API_KEY"] = "GROQ_API_KEY_PLACEHOLDER"

# Import required modules
from database_implementation.precomputed_findings_db import get_precomputed_db_manager
from dashboard_app.key_findings.key_findings_service import get_key_findings_service


class LiveAIGenerationTracker:
    """Tracker for live AI generation using Groq API with comprehensive logging."""

    def __init__(self):
        """Initialize the tracker with detailed logging."""
        self.db_manager = get_precomputed_db_manager()
        self.key_findings_service = get_key_findings_service()
        self.api_calls = []
        self.start_time = datetime.now()

        logger.info("🚀 Live AI Generation Tracker initialized")
        logger.info(f"🕐 Start time: {self.start_time}")
        logger.info(
            f"🔑 API Key configured: {os.environ.get('GROQ_API_KEY', 'Not found')[:20]}..."
        )

    async def generate_live_ai_analysis(
        self, tool_name: str, sources: list, language: str
    ) -> Dict[str, Any]:
        """Perform actual live AI generation using Groq API with comprehensive tracking."""

        logger.info(
            f"🚀 Performing LIVE AI generation: {tool_name} + {len(sources)} sources ({language})"
        )
        logger.info(f"🎯 This will make ACTUAL API calls to Groq!")
        logger.info(f"📊 Results should appear in your Groq console!")

        # Track API call details
        api_call = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "sources": sources,
            "language": language,
            "api_key_used": os.environ.get("GROQ_API_KEY", "Not found")[:20] + "...",
            "status": "initiated",
        }

        try:
            start_time = time.time()

            # Log the exact API call being made
            logger.info(
                f"📞 Making API call to key_findings_service.generate_key_findings()"
            )
            logger.info(
                f"📋 Parameters: tool='{tool_name}', sources={sources}, language='{language}', force_refresh=True"
            )

            # Perform the actual live AI generation
            result = await self.key_findings_service.generate_key_findings(
                tool_name=tool_name,
                selected_sources=sources,
                language=language,
                force_refresh=True,  # Force fresh AI generation
            )

            generation_time = time.time() - start_time

            # Track the result
            api_call["status"] = "success" if result["success"] else "failed"
            api_call["generation_time"] = generation_time
            api_call["result_summary"] = {
                "success": result["success"],
                "error": result.get("error", None),
                "sections_count": len(
                    [k for k in result.get("data", {}).keys() if result["data"].get(k)]
                ),
                "content_lengths": {
                    k: len(str(v))
                    for k, v in result.get("data", {}).items()
                    if isinstance(v, str)
                },
            }

            self.api_calls.append(api_call)

            if result["success"]:
                logger.info(
                    f"✅ Live AI generation successful in {generation_time:.2f}s"
                )
                logger.info(f"✅ This should appear in your Groq console!")

                # Log detailed content info
                data = result.get("data", {})
                logger.info(f"📊 Content summary:")
                for section, content in data.items():
                    if isinstance(content, str) and len(content.strip()) > 10:
                        logger.info(
                            f"   {section}: {len(content)} chars - {content[:50]}..."
                        )

                return result
            else:
                logger.error(
                    f"❌ Live AI generation failed: {result.get('error', 'Unknown error')}"
                )
                return result

        except Exception as e:
            logger.error(f"❌ Error in live AI generation: {e}")
            api_call["status"] = "error"
            api_call["error"] = str(e)
            self.api_calls.append(api_call)
            return {"success": False, "error": f"Live AI generation failed: {str(e)}"}

    def verify_groq_console_entry(self, combination_hash: str) -> bool:
        """Verify the AI-generated content appears in database."""
        logger.info(f"🔍 Verifying Groq console entry for hash: {combination_hash}")

        try:
            result = self.db_manager.get_combination_by_hash(combination_hash)

            if result:
                logger.info(f"✅ Entry found in database!")
                logger.info(f"   Tool: {result.get('tool_name')}")
                logger.info(f"   Sources: {result.get('sources_text')}")
                logger.info(f"   Language: {result.get('language')}")
                logger.info(f"   Analysis type: {result.get('analysis_type')}")

                # Check if this looks like real AI vs. template content
                exec_summary = result.get("executive_summary", "")
                principal_findings = result.get("principal_findings", "")

                if len(exec_summary) > 100 and len(principal_findings) > 100:
                    logger.info(f"   ✅ Content appears substantial (likely real AI)")
                    logger.info(f"   Executive Summary: {len(exec_summary)} chars")
                    logger.info(
                        f"   Principal Findings: {len(principal_findings)} chars"
                    )
                    return True
                else:
                    logger.info(f"   ⚠️ Content appears short (may be template)")
                    return False
            else:
                logger.warning(f"⚠️ No entry found for hash: {combination_hash}")
                return False

        except Exception as e:
            logger.error(f"❌ Error verifying database entry: {e}")
            return False

    def generate_verification_report(self) -> str:
        """Generate comprehensive verification report."""
        report = []
        report.append("=" * 70)
        report.append("📊 GROQ API VERIFICATION REPORT")
        report.append("=" * 70)
        report.append(f"📅 Report generated: {datetime.now()}")
        report.append(
            f"🔑 API Key used: {os.environ.get('GROQ_API_KEY', 'Not found')[:20]}..."
        )
        report.append(f"⏱️ Total API calls made: {len(self.api_calls)}")
        report.append(
            f"✅ Successful calls: {sum(1 for call in self.api_calls if call['status'] == 'success')}"
        )
        report.append(
            f"❌ Failed calls: {sum(1 for call in self.api_calls if call['status'] == 'failed')}"
        )
        report.append(
            f"⚠️ Error calls: {sum(1 for call in self.api_calls if call['status'] == 'error')}"
        )

        for i, call in enumerate(self.api_calls, 1):
            report.append(f"\n📞 API Call {i}:")
            report.append(f"   Timestamp: {call['timestamp']}")
            report.append(f"   Tool: {call['tool']}")
            report.append(f"   Sources: {call['sources']}")
            report.append(f"   Language: {call['language']}")
            report.append(f"   Status: {call['status']}")
            if "generation_time" in call:
                report.append(f"   Generation time: {call['generation_time']:.2f}s")
            if "result_summary" in call:
                summary = call["result_summary"]
                report.append(f"   Sections generated: {summary['sections_count']}")
                report.append(f"   Success: {summary['success']}")
                if summary["success"]:
                    report.append(f"   Content lengths: {summary['content_lengths']}")

        report.append("\n" + "=" * 70)
        report.append("✅ VERIFICATION COMPLETE")
        report.append("=" * 70)
        report.append("🎯 Check your Groq console to see the actual API calls!")
        report.append("=" * 70)

        return "\n".join(report)


async def main():
    """Main execution function."""
    print("🚀 Groq API Verification - Starting")
    print("=" * 70)
    print("🎯 This will make ACTUAL API calls to Groq!")
    print("📊 Results should appear in your Groq console!")
    print("=" * 70)

    verifier = GroqAPIVerifier()

    # Define combinations to test
    test_combinations = [
        ("Calidad Total", ["Google Trends"], "es"),
        (
            "Calidad Total",
            [
                "Google Trends",
                "Google Books",
                "Bain Usability",
                "Bain Satisfaction",
                "Crossref",
            ],
            "es",
        ),
        ("Calidad Total", ["Google Books", "Bain Satisfaction"], "es"),
    ]

    results = []

    for i, (tool, sources, language) in enumerate(test_combinations, 1):
        print(f"\n{'=' * 60}")
        print(f"🎯 Test {i}: {tool} + {len(sources)} sources ({language})")
        print(f"{'=' * 60}")

        # Perform live AI query
        result = await verifier.perform_live_ai_query(tool, sources, language)

        if result["success"]:
            # Generate combination hash for verification
            combination_hash = verifier.db_manager.generate_combination_hash(
                tool_name=tool, selected_sources=sources, language=language
            )

            # Verify the entry appears in database
            verification_result = verifier.verify_groq_console_entry(combination_hash)

            results.append(
                {
                    "combination": (tool, sources, language),
                    "api_success": True,
                    "db_verification": verification_result,
                    "hash": combination_hash,
                }
            )
        else:
            results.append(
                {
                    "combination": (tool, sources, language),
                    "api_success": False,
                    "error": result.get("error", "Unknown error"),
                }
            )

    # Generate final report
    report = verifier.generate_verification_report()
    print(report)

    print("\n✅ Groq API Verification Complete!")
    print("=" * 70)
    print("🎯 Check your Groq console to see the actual API calls!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
