#!/usr/bin/env python3
"""
Batch generation of Key Findings reports using z.ai GLM-5.1.

Generates bilingual (es/en) analysis reports for all tool + source
combinations and stores them in the v2 database.

Usage:
    # Sample run: one tool, all source combos
    uv run python scripts/generate_kf_reports.py --tool "Benchmarking"

    # Full batch: all 23 tools x 31 source combos = 713 reports
    uv run python scripts/generate_kf_reports.py

    # Dry run: show what would be generated
    uv run python scripts/generate_kf_reports.py --dry-run

    # Custom delay between API calls (seconds)
    uv run python scripts/generate_kf_reports.py --delay 2.0
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from itertools import combinations
from typing import Dict, List, Any, Optional

import httpx

# Add project paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, "dashboard_app"))
sys.path.insert(0, project_root)

# Load .env
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(project_root, ".env"))
except ImportError:
    pass

from tools import tool_file_dic
from database import get_database_manager
from key_findings.kf_report_db import KFReportDB, generate_report_hash
from key_findings.kf_sections import get_applicable_sections, SECTIONS
from fix_source_mapping import DISPLAY_NAMES, DBASE_OPTIONS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(project_root, "data", "generation.log")),
    ],
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# API configuration
# ---------------------------------------------------------------------------
API_ENDPOINT = "https://api.z.ai/api/coding/paas/v4/chat/completions"
MODEL = "glm-5.1"

# Source metadata
SOURCE_ID_TO_DISPLAY = {1: "Google Trends", 2: "Google Books", 3: "Bain Usability", 4: "Crossref", 5: "Bain Satisfaction"}
DISPLAY_TO_SOURCE_ID = {v: k for k, v in SOURCE_ID_TO_DISPLAY.items()}
ALL_SOURCE_IDS = [1, 2, 3, 4, 5]


def get_api_key() -> str:
    key = os.environ.get("ZAI_API_KEY", "")
    if not key:
        raise RuntimeError(
            "ZAI_API_KEY environment variable not set. "
            "Add it to .env or export it before running."
        )
    return key


# ---------------------------------------------------------------------------
# Source combination generation
# ---------------------------------------------------------------------------

def generate_all_source_combos() -> List[List[int]]:
    """Generate all 31 non-empty subsets of 5 sources."""
    combos = []
    for r in range(1, len(ALL_SOURCE_IDS) + 1):
        for combo in combinations(ALL_SOURCE_IDS, r):
            combos.append(sorted(list(combo)))
    return combos


# ---------------------------------------------------------------------------
# Data collection (simplified — pulls stats from DB)
# ---------------------------------------------------------------------------

def collect_data_context(tool_name: str, source_ids: List[int]) -> Dict[str, Any]:
    """Collect data context from the database for prompt construction."""
    db_manager = get_database_manager()
    datasets, valid_sources = db_manager.get_data_for_keyword(tool_name, source_ids)

    if not datasets:
        return {"error": "No data found", "tool_name": tool_name}

    # Build summary statistics per source
    source_summaries = {}
    total_points = 0
    date_min = None
    date_max = None

    for sid, df in datasets.items():
        if df.empty:
            continue
        display_name = SOURCE_ID_TO_DISPLAY.get(sid, str(sid))
        vals = df["value"]
        total_points += len(vals)

        idx = df.index
        if date_min is None or idx.min() < date_min:
            date_min = idx.min()
        if date_max is None or idx.max() > date_max:
            date_max = idx.max()

        source_summaries[display_name] = {
            "count": len(vals),
            "mean": round(float(vals.mean()), 2),
            "std": round(float(vals.std()), 2),
            "min": round(float(vals.min()), 2),
            "max": round(float(vals.max()), 2),
            "trend_direction": "increasing" if len(vals) > 1 and float(vals.iloc[-1]) > float(vals.iloc[0]) else "decreasing",
        }

    return {
        "tool_name": tool_name,
        "sources": [SOURCE_ID_TO_DISPLAY.get(s, str(s)) for s in source_ids],
        "source_ids": source_ids,
        "total_data_points": total_points,
        "date_range_start": str(date_min.date()) if date_min is not None else "N/A",
        "date_range_end": str(date_max.date()) if date_max is not None else "N/A",
        "source_summaries": source_summaries,
        "valid_sources": [SOURCE_ID_TO_DISPLAY.get(s, str(s)) for s in valid_sources],
    }


# ---------------------------------------------------------------------------
# Prompt construction (per-section)
# ---------------------------------------------------------------------------

def build_section_prompt(
    section_key: str,
    tool_name: str,
    source_names: List[str],
    data_context: Dict[str, Any],
) -> str:
    """Build a bilingual prompt for a single section."""

    section_info = SECTIONS[section_key]
    _, _, emoji, title_es, title_en = section_info
    sources_str = ", ".join(source_names)
    is_single = len(source_names) == 1
    analysis_type = "single-source" if is_single else "multi-source"

    # Data context summary
    summaries_text = ""
    for src, stats in data_context.get("source_summaries", {}).items():
        summaries_text += f"  - {src}: {stats['count']} data points, mean={stats['mean']}, std={stats['std']}, range=[{stats['min']}, {stats['max']}], trend={stats['trend_direction']}\n"

    prompt = f"""You are a doctoral-level management research analyst writing a bilingual report section.

TASK: Write the "{title_en}" section for a {analysis_type} analysis of the management tool "{tool_name}".

DATA CONTEXT:
- Tool: {tool_name}
- Data Sources: {sources_str}
- Period: {data_context.get('date_range_start', 'N/A')} to {data_context.get('date_range_end', 'N/A')}
- Total Data Points: {data_context.get('total_data_points', 0)}
- Source Statistics:
{summaries_text}

SECTION: {emoji} {title_en} / {title_es}

SECTION-SPECIFIC INSTRUCTIONS:
"""

    # Add section-specific guidance
    section_instructions = {
        "executive_summary": """Write a high-level executive summary (400-500 words per language).
Cover: strategic implications, key patterns, theory-practice insights, adoption recommendations.
This should be accessible to executives while maintaining academic rigor.""",

        "temporal_2d": """Analyze temporal trends from the data (600-800 words per language).
Cover: trend interpretation, momentum signals, volatility indicators, inflection points, lifecycle positioning.
Focus on what the temporal patterns mean for business strategy, not raw numbers.""",

        "mean_analysis": """Analyze the mean values and central tendencies (400-600 words per language).
Cover: average adoption levels, comparison between sources if multi-source, what mean levels indicate about market maturity.
Interpret what average values reveal about the tool's positioning in the management landscape.""",

        "seasonal_analysis": """Analyze seasonal patterns (600-800 words per language).
Cover: seasonal strength, periodicity, peak/valley timing, planning implications.
Focus on when organizations should implement based on cyclical patterns.""",

        "fourier_analysis": """Analyze spectral/frequency patterns (600-800 words per language).
Cover: dominant cycles, spectral power, harmonics, signal vs noise, future cycle prediction.
Interpret frequency analysis in terms of business adoption waves.""",

        "temporal_3d": """Analyze 3D temporal patterns across multiple sources (600-800 words per language).
Cover: synchronized vs divergent trends across sources, adoption timing from different perspectives.
Focus on how different data sources tell complementary stories about the tool's evolution.""",

        "heatmap_analysis": """Analyze correlation patterns between sources (600-800 words per language).
Cover: correlation clusters, complementary vs contradictory sources, market signal patterns.
Interpret what correlations between sources reveal about stakeholder alignment.""",

        "regression_analysis": """Analyze regression and predictive patterns (600-800 words per language).
Cover: predictive relationships between sources, growth trajectories, projection confidence.
Focus on what regression models reveal about future adoption trends.""",

        "pca_analysis": """Analyze Principal Component Analysis results (600-800 words per language).
Cover: source influence analysis, stakeholder alignment, relative weights, identified tensions, strategic interpretation.
Interpret PCA loadings in terms of which stakeholders drive the narrative.""",

        "conclusions": """Write comprehensive conclusions (500-700 words per language).
Cover: optimal timing, risk factors, opportunities, implementation strategy.
Provide actionable recommendations grounded in the analysis.""",
    }

    prompt += section_instructions.get(section_key, "Provide a thorough analysis for this section.")

    prompt += f"""

OUTPUT FORMAT:
You MUST respond with a valid JSON object containing exactly two keys: "es" and "en".
Each value must be a string with the section content in that language.
Use markdown formatting within the content (bold, headers, paragraphs).
Do NOT include the section title/header in the content — it will be added automatically.

IMPORTANT:
- Write substantive analysis, not generic filler
- Reference the actual data context provided above
- Maintain doctoral-level rigor while being accessible
- Each language version should be 400-800 words
- Do NOT wrap the JSON in markdown code blocks
- Do NOT include any text before or after the JSON

Example response format:
{{"es": "El analisis de {tool_name} revela...", "en": "The analysis of {tool_name} reveals..."}}
"""

    return prompt


# ---------------------------------------------------------------------------
# API calling
# ---------------------------------------------------------------------------

def call_glm_api(prompt: str, api_key: str, timeout: float = 300.0, max_retries: int = 5) -> Optional[str]:
    """Call z.ai GLM-5.1 API and return the content field. Retries on 429."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4096,
    }

    for attempt in range(max_retries):
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(API_ENDPOINT, json=payload, headers=headers)
                if response.status_code == 429:
                    wait = min(2 ** attempt * 5, 120)  # 5, 10, 20, 40, 80 seconds
                    logger.warning(f"Rate limited (429), waiting {wait}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(wait)
                    continue
                response.raise_for_status()
                data = response.json()

                # Extract content (ignore reasoning_content)
                choice = data.get("choices", [{}])[0]
                message = choice.get("message", {})
                content = message.get("content", "")
                return content

        except httpx.TimeoutException:
            logger.error(f"API call timed out (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(5)
                continue
            return None
        except httpx.HTTPStatusError as e:
            logger.error(f"API HTTP error {e.response.status_code}: {e.response.text[:500]}")
            return None
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return None

    logger.error(f"All {max_retries} retries exhausted")
    return None


def parse_bilingual_response(raw: str) -> Optional[Dict[str, str]]:
    """Parse the API response as bilingual JSON {es: ..., en: ...}."""
    if not raw:
        return None

    # Try direct JSON parse
    text = raw.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines if they're fences
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict) and "es" in parsed and "en" in parsed:
            return {"es": str(parsed["es"]), "en": str(parsed["en"])}
    except json.JSONDecodeError:
        pass

    # Fallback: try to find JSON object in the text
    import re
    match = re.search(r'\{[^{}]*"es"\s*:', text, re.DOTALL)
    if match:
        # Find the matching closing brace
        start = match.start()
        depth = 0
        for i in range(start, len(text)):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(text[start:i+1])
                        if "es" in parsed and "en" in parsed:
                            return {"es": str(parsed["es"]), "en": str(parsed["en"])}
                    except json.JSONDecodeError:
                        pass
                    break

    logger.warning("Could not parse bilingual JSON from response")
    logger.debug(f"Raw response: {text[:500]}")

    # Last resort: use the whole text as both languages
    if len(text) > 50:
        return {"es": text, "en": text}

    return None


# ---------------------------------------------------------------------------
# Main generation pipeline
# ---------------------------------------------------------------------------

def generate_report_for_combo(
    tool_name: str,
    source_ids: List[int],
    db: KFReportDB,
    api_key: str,
    delay: float = 1.0,
) -> bool:
    """Generate and store a full report for one tool + source combination."""
    source_names = [SOURCE_ID_TO_DISPLAY[s] for s in source_ids]
    num_sources = len(source_names)
    applicable_sections = get_applicable_sections(num_sources)

    logger.info(f"  Generating: {tool_name} + {source_names} ({len(applicable_sections)} sections)")

    # Collect data context
    data_context = collect_data_context(tool_name, source_ids)
    if data_context.get("error"):
        logger.warning(f"  Skipping — no data: {data_context['error']}")
        return False

    # Create/update report record
    report_id = db.upsert_report(
        tool_name=tool_name,
        source_names=source_names,
        source_ids=source_ids,
        model_used=MODEL,
    )

    success_count = 0
    for section_key in applicable_sections:
        prompt = build_section_prompt(section_key, tool_name, source_names, data_context)

        raw_response = call_glm_api(prompt, api_key)
        if raw_response is None:
            logger.error(f"    Section '{section_key}' — API call failed, skipping")
            time.sleep(delay)
            continue

        bilingual = parse_bilingual_response(raw_response)
        if bilingual is None:
            logger.error(f"    Section '{section_key}' — parse failed, skipping")
            time.sleep(delay)
            continue

        db.upsert_section(
            report_id=report_id,
            section_key=section_key,
            content_es=bilingual["es"],
            content_en=bilingual["en"],
        )
        success_count += 1
        logger.info(f"    Section '{section_key}' — OK (es: {len(bilingual['es'])} chars, en: {len(bilingual['en'])} chars)")

        time.sleep(delay)

    logger.info(f"  Done: {success_count}/{len(applicable_sections)} sections generated")
    return success_count > 0


def main():
    parser = argparse.ArgumentParser(description="Generate Key Findings reports")
    parser.add_argument("--tool", type=str, help="Generate for a single tool (Spanish name)")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between API calls (seconds)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without calling API")
    parser.add_argument("--db-path", type=str, help="Override database path")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Key Findings Report Generation")
    logger.info(f"Started: {datetime.now().isoformat()}")
    logger.info("=" * 60)

    # Determine tools to process
    if args.tool:
        if args.tool not in tool_file_dic:
            logger.error(f"Unknown tool: '{args.tool}'")
            logger.info(f"Available tools: {list(tool_file_dic.keys())}")
            sys.exit(1)
        tools = [args.tool]
    else:
        tools = list(tool_file_dic.keys())

    # Generate all source combinations (31 total)
    all_combos = generate_all_source_combos()
    total = len(tools) * len(all_combos)

    logger.info(f"Tools: {len(tools)}, Source combos: {len(all_combos)}, Total reports: {total}")

    if args.dry_run:
        logger.info("DRY RUN — showing what would be generated:")
        for tool in tools:
            for combo in all_combos:
                names = [SOURCE_ID_TO_DISPLAY[s] for s in combo]
                sections = get_applicable_sections(len(combo))
                logger.info(f"  {tool} + {names} -> {len(sections)} sections")
        logger.info(f"Total: {total} reports, ~{total * 8} API calls")
        return

    # Get API key
    api_key = get_api_key()

    # Initialize database
    db = KFReportDB(args.db_path)
    stats_before = db.get_stats()
    logger.info(f"DB before: {stats_before}")

    # Process
    completed = 0
    skipped = 0
    failed = 0

    for tool_idx, tool in enumerate(tools, 1):
        logger.info(f"\n{'='*40}")
        logger.info(f"Tool {tool_idx}/{len(tools)}: {tool}")
        logger.info(f"{'='*40}")

        for combo_idx, combo in enumerate(all_combos, 1):
            source_names = [SOURCE_ID_TO_DISPLAY[s] for s in combo]

            # Skip if already generated
            if db.has_report(tool, source_names):
                skipped += 1
                logger.info(f"  [{combo_idx}/{len(all_combos)}] Already exists: {source_names} — skipping")
                continue

            logger.info(f"  [{combo_idx}/{len(all_combos)}] Generating...")
            success = generate_report_for_combo(tool, combo, db, api_key, args.delay)
            if success:
                completed += 1
            else:
                failed += 1

            # Progress update every 10 reports
            if (completed + failed) % 10 == 0:
                elapsed = time.time()
                logger.info(f"  Progress: {completed} completed, {skipped} skipped, {failed} failed")

    # Final stats
    stats_after = db.get_stats()
    logger.info(f"\n{'='*60}")
    logger.info(f"Generation Complete: {datetime.now().isoformat()}")
    logger.info(f"  Completed: {completed}")
    logger.info(f"  Skipped (existing): {skipped}")
    logger.info(f"  Failed: {failed}")
    logger.info(f"  DB after: {stats_after}")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    main()
