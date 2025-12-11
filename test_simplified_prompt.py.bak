#!/usr/bin/env python3
"""
Fix Seasonal Analysis with Simplified Prompt

This script creates a simplified prompt that explicitly forces the AI
to generate all 7 required sections including seasonal_analysis.
"""

import os
import sys
import asyncio
import logging
import json
from datetime import datetime

# Add the dashboard_app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dashboard_app"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Import required components
from dashboard_app.key_findings.unified_ai_service import UnifiedAIService


async def test_simplified_prompt():
    """Test a simplified prompt that forces all 7 sections."""

    logger.info("=" * 70)
    logger.info("🔧 TESTING SIMPLIFIED PROMPT FOR ALL 7 SECTIONS")
    logger.info("=" * 70)

    # Create a much simpler, more explicit prompt
    simplified_prompt = f"""
ANÁLISIS DE CALIDAD TOTAL - GOOGLE TRENDS (2004-2023)

Genera exactamente 7 secciones con estos encabezados EXACTOS:

## 1. RESUMEN EJECUTIVO
[Contenido del resumen ejecutivo aquí - 400 palabras]

## 2. HALLAZGOS PRINCIPALES  
[Lista de hallazgos principales aquí - 600 palabras]

## 3. ANÁLISIS TEMPORAL
[Análisis de tendencias temporales aquí - 600 palabras]

## 4. ANÁLISIS ESTACIONAL
[Análisis detallado de patrones estacionales aquí - 600 palabras]
IMPORTANTE: Esta sección debe contener contenido específico sobre patrones estacionales, no puede estar vacía.

## 5. ANÁLISIS DE FOURIER
[Análisis espectral de Fourier aquí - 600 palabras]

## 6. SÍNTESIS ESTRATÉGICA
[Síntesis de todos los análisis aquí - 500 palabras]

## 7. CONCLUSIONES
[Conclusiones y recomendaciones aquí - 500 palabras]

INSTRUCCIONES CRÍTICAS:
- DEBES incluir las 7 secciones exactas con estos encabezados
- La sección 4 (ANÁLISIS ESTACIONAL) NO puede estar vacía
- Cada sección debe tener al menos 300 palabras
- Responde SOLO con las 7 secciones, sin introducción adicional
"""

    logger.info(f"📝 Using simplified prompt ({len(simplified_prompt)} characters)")
    logger.info("🎯 Testing if simplified prompt forces all 7 sections...")

    try:
        # Initialize AI service
        ai_service = UnifiedAIService(
            groq_api_key="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"
        )

        # Generate analysis with simplified prompt
        result = await ai_service.generate_analysis(
            prompt=simplified_prompt, language="es", is_single_source=True
        )

        if not result["success"]:
            logger.error(
                f"❌ AI generation failed: {result.get('error', 'Unknown error')}"
            )
            return False

        logger.info(f"✅ AI generation successful!")

        # Check what sections were generated
        content = result["content"]

        logger.info("\n" + "=" * 50)
        logger.info("📋 SIMPLIFIED PROMPT RESULTS")
        logger.info("=" * 50)

        # Check for the 7 required sections
        required_sections = [
            "executive_summary",
            "principal_findings",
            "temporal_analysis",
            "seasonal_analysis",
            "fourier_analysis",
            "strategic_synthesis",
            "conclusions",
        ]

        present_sections = 0
        for section in required_sections:
            section_content = content.get(section, "")
            section_length = len(str(section_content))

            if section_length > 50:  # Minimum viable content
                present_sections += 1
                logger.info(f"✅ {section}: {section_length} chars")
            else:
                logger.error(f"❌ {section}: {section_length} chars (missing/empty)")

        logger.info(f"\n📊 Summary: {present_sections}/7 sections present")

        if present_sections >= 7:
            logger.info("🎉 SUCCESS! All 7 sections generated correctly!")

            # Check specifically for seasonal_analysis
            seasonal_content = content.get("seasonal_analysis", "")
            if seasonal_content and len(str(seasonal_content)) > 100:
                logger.info(
                    f"✅ Seasonal analysis has content: {len(seasonal_content)} chars"
                )
                logger.info("First 200 characters of seasonal_analysis:")
                logger.info("-" * 40)
                logger.info(str(seasonal_content)[:200])
                logger.info("-" * 40)
                return True
            else:
                logger.error("❌ Seasonal analysis still empty!")
                return False
        else:
            logger.error(f"❌ Only {present_sections}/7 sections generated")
            return False

    except Exception as e:
        logger.error(f"❌ Exception during testing: {str(e)}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_simplified_prompt())

    if success:
        logger.info("\n🎉 SIMPLIFIED PROMPT WORKS!")
        logger.info(
            "This confirms the issue is with the complex prompt, not the AI model."
        )
    else:
        logger.info("\n❌ SIMPLIFIED PROMPT ALSO FAILS")
        logger.info(
            "This suggests the AI model has fundamental issues with section generation."
        )
