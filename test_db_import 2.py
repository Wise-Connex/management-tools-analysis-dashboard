#!/usr/bin/env python3

import sys
from pathlib import Path

# Test import path
tools_dashboard_root = Path(__file__).parent.parent.parent
print("Tools dashboard root:", tools_dashboard_root)
if str(tools_dashboard_root) not in sys.path:
    sys.path.insert(0, str(tools_dashboard_root))
    print("Added to path")

try:
    from database_implementation.precomputed_findings_db import (
        get_precomputed_db_manager,
    )

    print("✅ Import successful")
    db_manager = get_precomputed_db_manager()
    print("✅ Database manager created")
    print(
        "Test hash generation:",
        db_manager.generate_combination_hash("Test", ["Google Trends"], "es"),
    )
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback

    traceback.print_exc()
