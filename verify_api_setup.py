#!/usr/bin/env python3
"""
API Key Setup Verification Script

Verifies that Groq API key is properly configured and loaded.
This script tests the environment variable loading mechanism.
"""

import os
import sys
from pathlib import Path


def verify_api_key_setup():
    """Verify API key configuration and loading."""
    print("🔍 API Key Setup Verification")
    print("=" * 50)

    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")

    # Check .env file
    env_file = current_dir / ".env"
    env_example_file = current_dir / ".env.example"

    print(f"\n📋 Environment Files Check:")
    print(f"   .env exists: {env_file.exists()}")
    print(f"   .env.example exists: {env_example_file.exists()}")

    if env_file.exists():
        # Check .env file size and permissions
        stat = env_file.stat()
        print(f"   .env file size: {stat.st_size} bytes")
        print(f"   .env permissions: {oct(stat.st_mode)[-3:]}")

        # Read first few lines of .env
        try:
            with open(env_file, "r") as f:
                lines = f.readlines()[:5]
            print(f"   .env content preview:")
            for i, line in enumerate(lines, 1):
                if "API_KEY" in line.upper():
                    # Mask the key for security
                    key_name = line.split("=")[0]
                    print(f"     Line {i}: {key_name}=***[REDACTED]***")
                else:
                    print(f"     Line {i}: {line.strip()}")
        except Exception as e:
            print(f"   ❌ Error reading .env: {e}")

    # Test environment variable loading
    print(f"\n🔑 API Key Loading Test:")

    # Before dotenv loading
    groq_key_before = os.getenv("GROQ_API_KEY")
    openrouter_key_before = os.getenv("OPENROUTER_API_KEY")

    print(
        f"   GROQ_API_KEY (before dotenv): {'✅ Found' if groq_key_before else '❌ Not found'}"
    )
    print(
        f"   OPENROUTER_API_KEY (before dotenv): {'✅ Found' if openrouter_key_before else '❌ Not found'}"
    )

    # Try to load dotenv
    print(f"\n📦 Dotenv Loading Test:")
    print(
        f"   💡 IMPORTANT: Always use 'uv run python {__file__}' to ensure dotenv is available"
    )

    dotenv_available = False
    loaded = False

    # Manual .env loading (since dotenv import has issues)
    print(f"   Manual .env loading will be attempted...")

    # Manual .env loading (no dotenv dependency)

    # After dotenv loading (or manual)
    if not loaded and env_file.exists():
        # Manual loading fallback
        try:
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip().strip("\"'")
                        os.environ[key] = value
            print(f"   Manual .env loading: ✅ Success")
        except Exception as e:
            print(f"   Manual .env loading: ❌ Error: {e}")

    # Check after loading
    groq_key_after = os.getenv("GROQ_API_KEY")
    openrouter_key_after = os.getenv("OPENROUTER_API_KEY")

    print(f"\n🔑 API Key Status (after loading):")
    print(f"   GROQ_API_KEY: {'✅ Loaded' if groq_key_after else '❌ Not loaded'}")
    print(
        f"   OPENROUTER_API_KEY: {'✅ Loaded' if openrouter_key_after else '❌ Not loaded'}"
    )

    # Validate key format
    if groq_key_after:
        if groq_key_after.startswith("gsk_"):
            print(f"   GROQ_API_KEY format: ✅ Valid (starts with 'gsk_')")
        else:
            print(
                f"   GROQ_API_KEY format: ⚠️ Unusual format (doesn't start with 'gsk_')"
            )
        print(f"   GROQ_API_KEY length: {len(groq_key_after)} characters")

    # Test dashboard app loading
    print(f"\n🚀 Dashboard App Loading Test:")
    try:
        # Add dashboard_app to path
        dashboard_path = current_dir / "dashboard_app"
        if dashboard_path.exists():
            sys.path.insert(0, str(dashboard_path))

            # Test key loading from app context
            groq_key_app = os.getenv("GROQ_API_KEY", "")
            print(
                f"   Dashboard app context: {'✅ API key available' if groq_key_app else '❌ No API key'}"
            )

            # Test database-first service availability
            try:
                from database_implementation.precomputed_findings_db import (
                    get_precomputed_db_manager,
                )

                db_manager = get_precomputed_db_manager()
                stats = db_manager.get_statistics()
                total_combinations = stats.get("total_combinations", 0)
                print(
                    f"   Precomputed database: ✅ Available ({total_combinations} combinations)"
                )
                print(
                    f"   Database-first mode: {'✅ Ready' if total_combinations > 0 else '⚠️ Empty database'}"
                )
            except Exception as e:
                print(f"   Precomputed database: ❌ Error: {e}")
        else:
            print(f"   Dashboard app path: ❌ Not found")

    except Exception as e:
        print(f"   Dashboard app test: ❌ Error: {e}")

    # Summary
    print(f"\n📊 Summary:")
    api_ready = bool(groq_key_after)
    db_ready = False

    try:
        from database_implementation.precomputed_findings_db import (
            get_precomputed_db_manager,
        )

        db_manager = get_precomputed_db_manager()
        stats = db_manager.get_statistics()
        db_ready = stats.get("total_combinations", 0) > 0
    except:
        pass

    if api_ready and db_ready:
        print("✅ FULLY OPERATIONAL - Both API and database are ready")
    elif db_ready:
        print("✅ DATABASE-ONLY MODE - Database-first functionality available")
    elif api_ready:
        print("⚠️ API-ONLY MODE - Live AI generation available, no cached data")
    else:
        print("❌ NOT READY - Neither API nor database fully configured")

    return api_ready or db_ready


if __name__ == "__main__":
    success = verify_api_key_setup()
    sys.exit(0 if success else 1)
