#!/usr/bin/env python3
"""
Debug and Fix Multi-Source AI Response Parsing

This script will:
1. Test what the AI actually returns for multi-source
2. Identify the parsing issue
3. Fix the parsing to extract real content
4. Generate and store real AI content
"""

import os
import sys
import asyncio
import logging
from datetime import datetime

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Import required components
from key_findings.unified_ai_service import UnifiedAIService


async def debug_multi_source_ai_response():
    """Debug what the AI actually returns for multi-source analysis."""

    logger.info("=" * 70)
    logger.info("🔍 DEBUGGING MULTI-SOURCE AI RESPONSE")
    logger.info("=" * 70)

    # Initialize AI service
    ai_service = UnifiedAIService(
        groq_api_key="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"
    )

    # Simple test prompt for multi-source
    simple_prompt = """
Analiza Calidad Total usando 2 fuentes: Google Books y Bain Satisfaction.

Genera exactamente estas secciones:

## 1. RESUMEN EJECUTIVO
[Contenido del resumen ejecutivo]

## 2. HALLAZGOS PRINCIPALES
[Lista de hallazgos principales]

## 3. ANÁLISIS TEMPORAL  
[Análisis temporal]

## 4. ANÁLISIS ESTACIONAL
[Análisis estacional]

## 5. ANÁLISIS DE FOURIER
[Análisis de Fourier]

## 6. ANÁLISIS PCA
[Análisis de componentes principales]

## 7. ANÁLISIS DE MAPA DE CALOR
[Análisis de correlaciones]

Responde SOLO con estas 7 secciones en español.
"""

    logger.info("📝 Testing AI response with simple prompt...")
    logger.info(f"Prompt length: {len(simple_prompt)} characters")

    try:
        result = await ai_service.generate_analysis(
            prompt=simple_prompt, language="es", is_single_source=False
        )

        if result["success"]:
            logger.info("✅ AI generation successful!")
            content = result["content"]
            logger.info(f"Content type: {type(content)}")

            if isinstance(content, dict):
                logger.info(f"Content keys: {list(content.keys())}")

                # Show raw content for each key
                for key, value in content.items():
                    logger.info(f"\n--- {key} ({len(str(value))} chars) ---")
                    logger.info(
                        str(value)[:500] + "..."
                        if len(str(value)) > 500
                        else str(value)
                    )
            else:
                logger.info(f"Raw content ({len(str(content))} chars):")
                logger.info(
                    str(content)[:1000] + "..."
                    if len(str(content)) > 1000
                    else str(content)
                )

        else:
            logger.error(
                f"❌ AI generation failed: {result.get('error', 'Unknown error')}"
            )

    except Exception as e:
        logger.error(f"❌ Exception: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(debug_multi_source_ai_response())
