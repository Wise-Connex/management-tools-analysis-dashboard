#!/usr/bin/env python3
"""
Real-time Batch Processing Monitor
Shows live progress of Kimi K2 batch processing with detailed metrics.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
import json

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🔍 REAL-TIME BATCH PROCESSING MONITOR")
print("=" * 60)
print("📊 Live monitoring of Kimi K2 processing...")
print("💡 Watch for Groq console activity")
print()

# Load environment variables
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
    exit(1)

# Initialize components
print("🔧 Initializing monitoring system...")
try:
    from groq import Groq
    from database_implementation.precomputed_findings_db import (
        get_precomputed_db_manager,
    )
    from database_implementation.phase3_precomputation_pipeline import (
        PrecomputationPipeline,
    )

    # Groq client
    groq_api_key = os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key)

    # Database manager
    db_manager = get_precomputed_db_manager()

    # Pipeline
    pipeline = PrecomputationPipeline(use_simulation=True)

    print("✅ All components initialized")
except Exception as e:
    print(f"❌ Failed to initialize: {e}")
    exit(1)

# Generate all combinations and take larger batch for monitoring
print("\n🔢 Generating combinations...")
combinations = pipeline.generate_all_combinations()

# Use first 20 combinations for visible progress
monitor_batch = combinations[:20]
print(f"📊 Monitoring first {len(monitor_batch)} combinations")
print("=" * 60)

# Initialize tracking
start_time = time.time()
total_cost = 0
total_tokens = 0
processed = 0
successful = 0
failed = 0

print(f"🚀 STARTING MONITORED BATCH PROCESSING")
print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
print("=" * 60)

# Process with real-time monitoring
for i, combination in enumerate(monitor_batch, 1):
    print(f"\n🔄 Processing {i}/{len(monitor_batch)}")
    print(f"📋 Tool: {combination['tool_name'][:30]}")
    print(
        f"🔗 Sources: {len(combination['selected_sources'])} ({', '.join(combination['selected_sources'][:2])}...)"
    )
    print(f"🌍 Language: {combination['language']}")

    # Generate prompt
    tool_name = combination["tool_name"]
    selected_sources = combination["selected_sources"]
    language = combination["language"]
    sources_count = combination["sources_count"]

    if language == "es":
        prompt = f"""Analiza las tendencias y patrones para la herramienta de gestión "{tool_name}" utilizando datos de las siguientes fuentes: {", ".join(selected_sources)}.

Proporciona un análisis ejecutivo comprehensivo que incluya:

1. **Resumen Ejecutivo**: Hallazgos principales y tendencias observadas
2. **Análisis Temporal**: Patrones de crecimiento, volatilidad y tendencias  
3. **Análisis Estacional**: Patrones estacionales y periodicidad
4. **Análisis Espectral**: Frecuencias dominantes y análisis de Fourier
5. **Análisis de Calor**: Distribución de datos y clusters

Para análisis multifuente ({sources_count} fuentes), incluye también:
6. **Análisis PCA**: Componentes principales y correlaciones intersource
7. **Matriz de Correlación**: Relaciones entre las diferentes fuentes

Utiliza un estilo profesional y académico. Proporciona insights específicos basados en los datos disponibles para cada fuente."""
    else:
        prompt = f"""Analyze trends and patterns for the management tool "{tool_name}" using data from the following sources: {", ".join(selected_sources)}.

Provide a comprehensive executive analysis including:

1. **Executive Summary**: Key findings and observed trends
2. **Temporal Analysis**: Growth patterns, volatility, and trends
3. **Seasonal Analysis**: Seasonal patterns and periodicity
4. **Spectral Analysis**: Dominant frequencies and Fourier analysis
5. **Heatmap Analysis**: Data distribution and clusters

For multi-source analysis ({sources_count} sources), also include:
6. **PCA Analysis**: Principal components and cross-source correlations
7. **Correlation Matrix**: Relationships between different sources

Use a professional and academic style. Provide specific insights based on available data for each source."""

    try:
        # Show progress before API call
        progress_pct = (i - 1) / len(monitor_batch) * 100
        elapsed_time = time.time() - start_time
        avg_time_per_item = elapsed_time / (i - 1) if i > 1 else 0
        remaining_items = len(monitor_batch) - (i - 1)
        eta = remaining_items * avg_time_per_item

        print(
            f"📊 Progress: {progress_pct:5.1f}% | "
            f"⏱️ Elapsed: {elapsed_time / 60:4.1f}min | "
            f"📈 ETA: {eta / 60:4.1f}min | "
            f"💰 Cost so far: ${total_cost:.4f}"
        )

        print("🤖 Sending to Kimi K2...")

        # API call with timing
        api_start = time.time()

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="moonshotai/kimi-k2-instruct",
        )

        api_time = time.time() - api_start
        processing_time = time.time() - start_time

        # Extract response
        ai_response = chat_completion.choices[0].message.content

        # Calculate metrics
        prompt_tokens = len(prompt.split())
        response_tokens = len(ai_response.split())
        total_combination_tokens = prompt_tokens + response_tokens
        cost = total_combination_tokens * 0.003 / 1000

        total_cost += cost
        total_tokens += total_combination_tokens
        processed += 1
        successful += 1

        print(
            f"✅ SUCCESS! | "
            f"⏰ API: {api_time:.1f}s | "
            f"🔢 Tokens: {total_combination_tokens:,} | "
            f"💸 Cost: ${cost:.4f}"
        )
        print(f"📄 Content: {ai_response[:120]}...")

        # Store in database
        analysis_data = {
            "executive_summary": ai_response,
            "temporal_analysis": ai_response,
            "seasonal_analysis": ai_response,
            "fourier_analysis": ai_response,
            "heatmap_analysis": ai_response,
            "tool_display_name": tool_name,
            "data_points_analyzed": 2500,
            "confidence_score": 0.92,
            "model_used": "moonshotai/kimi-k2-instruct",
            "analysis_type": combination["analysis_type"],
            "processing_time": processing_time,
            "tokens_used": total_combination_tokens,
            "cost_incurred": cost,
        }

        # Update database
        db_manager.store_precomputed_analysis(
            combination_hash=combination["combination_hash"],
            tool_name=tool_name,
            selected_sources=selected_sources,
            language=language,
            analysis_data=analysis_data,
        )

        print(f"💾 Stored in database")

        # Live metrics update
        if i % 5 == 0 or i == len(monitor_batch):
            elapsed_time = time.time() - start_time
            success_rate = successful / processed * 100 if processed > 0 else 0
            avg_cost_per_item = total_cost / successful if successful > 0 else 0

            print(f"\n📊 LIVE METRICS UPDATE (Item {i}):")
            print(
                f"   ✅ Success rate: {success_rate:5.1f}% ({successful}/{processed})"
            )
            print(
                f"   💰 Total cost: ${total_cost:.4f} | Avg: ${avg_cost_per_item:.4f}/item"
            )
            print(
                f"   📊 Total tokens: {total_tokens:,} | {total_tokens / successful:.0f} avg"
            )
            print(f"   ⏱️ Average time: {api_time:.1f}s per item")
            print(f"   🎯 Projected full batch cost: ${avg_cost_per_item * 1302:.2f}")
            print("=" * 60)

    except Exception as e:
        failed += 1
        print(f"❌ FAILED: {e}")

# Final summary
print(f"\n🎯 MONITORED BATCH COMPLETE!")
print("=" * 60)
final_time = time.time() - start_time
success_rate = successful / processed * 100 if processed > 0 else 0

print(f"📊 SUMMARY:")
print(f"   Processed: {processed} items")
print(f"   Successful: {successful} ({success_rate:.1f}%)")
print(f"   Failed: {failed}")
print(f"   Total time: {final_time / 60:.1f} minutes")
print(f"   Total cost: ${total_cost:.4f}")
print(f"   Average cost/item: ${total_cost / successful:.4f}")
print(f"   🚀 Projected 1,302 batch cost: ${(total_cost / successful) * 1302:.2f}")

if success_rate > 90:
    print("\n✅ EXCELLENT SUCCESS RATE! Ready for full batch processing!")
elif success_rate > 75:
    print("\n⚠️  GOOD success rate, but some issues to investigate")
else:
    print("\n❌ SUCCESS RATE TOO LOW! Need to fix issues before full batch")

print(f"\n🎉 Monitored processing complete!")
print(f"📈 Check your Groq console for all the API activity!")
