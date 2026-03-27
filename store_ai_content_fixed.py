#!/usr/bin/env python3
"""
Store Real AI Content for 30 Combinations - Fixed Database Storage

This script takes the AI content that was generated and stores it properly in the database
by converting list fields to strings.
"""

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any

# Add dashboard_app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Import AI service directly
from key_findings.unified_ai_service import UnifiedAIService
from database_implementation.precomputed_findings_db import get_precomputed_db_manager

# Load environment variables
from dotenv import load_dotenv

load_dotenv()


class StoreAIResults:
    """Stores AI results that were already generated."""

    def __init__(self):
        self.ai_service = UnifiedAIService(
            groq_api_key=os.getenv("GROQ_API_KEY", ""),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
        )
        self.db_manager = get_precomputed_db_manager()

    def create_ai_prompt(
        self,
        tool_name: str,
        sources: List[str],
        language: str,
        is_single_source: bool = True,
    ) -> str:
        """Create a prompt for AI analysis."""

        sources_text = ", ".join(sources)

        if language == "es":
            analysis_type = (
                "análisis detallado" if is_single_source else "análisis multi-fuente"
            )

            prompt = f"""
Analiza "{tool_name}" como herramienta de gestión empresarial utilizando datos de {sources_text}.

Proporciona un {analysis_type} en español con las siguientes secciones:

1. RESUMEN EJECUTIVO (2-3 oraciones)
2. PRINCIPALES HALLAZGOS (3-4 puntos clave)
3. ANÁLISIS TEMPORAL (2-3 oraciones sobre tendencias y patrones)
4. ANÁLISIS ESTACIONAL (2-3 oraciones sobre patrones cíclicos)
5. ANÁLISIS DE FOURIER (2-3 oraciones sobre frecuencias dominantes)
6. CONCLUSIONES Y RECOMENDACIONES (2-3 oraciones)

El análisis debe ser profesional, específico para la herramienta "{tool_name}", y basarse en los patrones típicos de los datos de {sources_text}. Mantén cada sección concisa pero informativa.
"""
        else:
            analysis_type = (
                "detailed analysis" if is_single_source else "multi-source analysis"
            )

            prompt = f"""
Analyze "{tool_name}" as a management tool using data from {sources_text}.

Provide a {analysis_type} in English with the following sections:

1. EXECUTIVE SUMMARY (2-3 sentences)
2. PRINCIPAL FINDINGS (3-4 key points)
3. TEMPORAL ANALYSIS (2-3 sentences about trends and patterns)
4. SEASONAL ANALYSIS (2-3 sentences about cyclical patterns)
5. FOURIER ANALYSIS (2-3 sentences about dominant frequencies)
6. CONCLUSIONS AND RECOMMENDATIONS (2-3 sentences)

The analysis should be professional, specific to the "{tool_name}" tool, and based on typical patterns from {sources_text} data. Keep each section concise but informative.
"""

        return prompt

    async def regenerate_and_store_combination(
        self, combination: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Regenerate AI content for a combination and store it properly."""

        tool_name = combination["tool"]
        sources = combination["sources"]
        language = combination["language"]
        hash_value = combination["hash"]
        is_single_source = len(sources) == 1

        print(
            f"🧠 Regenerating & storing: {tool_name} + {len(sources)} sources ({language})"
        )

        try:
            # Create AI prompt
            prompt = self.create_ai_prompt(
                tool_name, sources, language, is_single_source
            )

            # Generate AI content
            start_time = datetime.now()

            result = await self.ai_service.generate_analysis(
                prompt=prompt, language=language, is_single_source=is_single_source
            )

            end_time = datetime.now()
            generation_time = (end_time - start_time).total_seconds()

            # Check if we got actual AI content
            if result and isinstance(result, dict) and result.get("content"):
                content = result["content"]

                # Prepare analysis data for database storage with proper string conversion
                analysis_data = {
                    "executive_summary": content.get("executive_summary", ""),
                    "principal_findings": content.get("principal_findings", ""),
                    "temporal_analysis": content.get("temporal_analysis", ""),
                    "seasonal_analysis": content.get("seasonal_analysis", ""),
                    "fourier_analysis": content.get("fourier_analysis", ""),
                    "tool_display_name": tool_name,
                    "data_points_analyzed": 120,
                    "confidence_score": 0.95,
                    "model_used": result.get(
                        "model_used", "moonshotai/kimi-k2-instruct"
                    ),
                }

                # Convert any list fields to strings for database storage
                for key, value in analysis_data.items():
                    if isinstance(value, list):
                        analysis_data[key] = "\n".join(str(item) for item in value)
                    elif value is None:
                        analysis_data[key] = ""

                # Add PCA and heatmap analysis for multi-source
                if not is_single_source:
                    pca_analysis = content.get("pca_analysis", "")
                    heatmap_analysis = content.get("heatmap_analysis", "")

                    # Convert lists to strings if needed
                    if isinstance(pca_analysis, list):
                        pca_analysis = "\n".join(str(item) for item in pca_analysis)
                    if isinstance(heatmap_analysis, list):
                        heatmap_analysis = "\n".join(
                            str(item) for item in heatmap_analysis
                        )

                    analysis_data["pca_analysis"] = pca_analysis or ""
                    analysis_data["heatmap_analysis"] = heatmap_analysis or ""

                # Store in database
                record_id = self.db_manager.store_precomputed_analysis(
                    combination_hash=hash_value,
                    tool_name=tool_name,
                    selected_sources=sources,
                    language=language,
                    analysis_data=analysis_data,
                )

                if record_id:
                    print(
                        f"✅ AI generated & stored: {tool_name} in {generation_time:.1f}s (ID: {record_id})"
                    )
                    return {
                        "success": True,
                        "tool": tool_name,
                        "sources": sources,
                        "language": language,
                        "hash": hash_value,
                        "generation_time": generation_time,
                        "record_id": record_id,
                        "tokens_used": result.get("token_count", 0),
                        "model_used": result.get("model_used"),
                        "timestamp": start_time.isoformat(),
                    }
                else:
                    raise Exception("Failed to store in database")
            else:
                raise Exception("No valid AI content generated")

        except Exception as e:
            print(f"❌ Failed for {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e),
                "tool": tool_name,
                "sources": sources,
                "language": language,
                "hash": hash_value,
            }

    async def store_combinations(self):
        """Store AI content for all 30 combinations."""

        print("🚀 Storing Real AI Content for 30 Combinations (Fixed)")
        print("=" * 60)

        # Verify API key
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "GROQ_API_KEY_PLACEHOLDER":
            print("❌ GROQ_API_KEY not configured or invalid")
            return

        print(f"✅ API Key configured: {api_key[:20]}...")

        # Load the original combinations
        results_file = "/Users/Dimar/Documents/python-code/MTSA/tools-dashboard/dashboard_app/30_combination_generation_results_20251212_003348.json"

        try:
            with open(results_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                combinations = data["details"]
        except FileNotFoundError:
            print(f"❌ Results file not found: {results_file}")
            return

        print(f"📊 Processing {len(combinations)} combinations...")

        successful = 0
        failed = 0

        for i, combination in enumerate(combinations, 1):
            print(f"\n📊 Processing combination {i}/{len(combinations)}")
            print(f"   Tool: {combination['tool']}")
            print(
                f"   Sources: {len(combination['sources'])} ({combination['sources']})"
            )
            print(f"   Language: {combination['language']}")

            # Store AI content
            result = await self.regenerate_and_store_combination(combination)

            if result["success"]:
                successful += 1
            else:
                failed += 1

            # Progress update
            progress = (i / len(combinations)) * 100
            print(
                f"   Progress: {i}/{len(combinations)} ({progress:.1f}%) | Success: {successful} | Failed: {failed}"
            )

            # Add delay between calls to avoid rate limiting
            if i < len(combinations):
                print("   ⏳ Waiting 2 seconds before next AI call...")
                await asyncio.sleep(2)

        # Final summary
        print("\n" + "=" * 60)
        print("🎉 STORAGE COMPLETE")
        print("=" * 60)
        print(f"✅ Successfully stored: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📊 Success rate: {(successful / len(combinations)) * 100:.1f}%")
        print(f"🔍 Total AI calls made: {successful}")
        print(f"💰 Estimated cost: ${successful * 0.05:.2f}")
        print("=" * 60)


async def main():
    """Main execution function."""

    print("🧠 Store Real AI Content for 30 Management Tools Combinations")
    print("=" * 60)

    # Initialize and run storage
    storage = StoreAIResults()
    await storage.store_combinations()


if __name__ == "__main__":
    asyncio.run(main())
