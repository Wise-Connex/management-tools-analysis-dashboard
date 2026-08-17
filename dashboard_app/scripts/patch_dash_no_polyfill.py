#!/usr/bin/env python3
"""
Post-install patch: remove @babel/polyfill from Dash's _dash_renderer.

Dash 3.x includes the @babel/polyfill bundle in the component deps list
for IE11 compatibility. Modern browsers don't need it; it adds ~36 KB
to every page load.

Run after 'uv sync' to re-apply the patch:
    uv run python dashboard_app/scripts/patch_dash_no_polyfill.py

Idempotent: safe to run multiple times.
"""
import re
import sys
from pathlib import Path

# Find _dash_renderer.py. Try sys.path first (when run with uv run),
# then look for a sibling .venv directory.
renderer_path = None
try:
    import dash  # noqa: F401

    renderer_path = Path(dash.__file__).parent / "_dash_renderer.py"
except ImportError:
    # Not in current Python's path; search for .venv near this script
    here = Path(__file__).resolve().parent
    for candidate in [
        here.parent.parent / ".venv",
        here.parent / ".venv",
        here / ".venv",
    ]:
        vdash = candidate / "lib" / "python3.12" / "site-packages" / "dash"
        if vdash.exists():
            renderer_path = vdash / "_dash_renderer.py"
            break

if renderer_path is None or not renderer_path.exists():
    print("ERROR: could not find _dash_renderer.py")
    print("Run with: uv run python dashboard_app/scripts/patch_dash_no_polyfill.py")
    sys.exit(1)

src = renderer_path.read_text()
original = src

# Remove polyfill entries from the deps arrays (both prod and dev)
src = re.sub(
    r'(\s*"relative_package_path":\s*\{\s*"prod":\s*\[)\s*"deps/polyfill@7\.12\.1\.min\.js",\s*',
    r"\1",
    src,
)
src = re.sub(
    r'(\s*"dev":\s*\[)\s*"deps/polyfill@7\.12\.1\.min\.js",\s*',
    r"\1",
    src,
)
# Remove the polyfill entry from the deps dict (where URLs are listed)
src = re.sub(
    r'\s*"polyfill@7\.12\.1\.min\.js":\s*\[\s*"https://unpkg\.com/@babel/polyfill@7\.12\.1/dist/polyfill\.min\.js"\s*\]\s*,?',
    "",
    src,
)
# Remove the standalone polyfill URL string
src = src.replace(
    '"https://unpkg.com/@babel/polyfill@7.12.1/dist/polyfill.min.js"', '""'
)

if src == original:
    print(f"Already patched (no polyfill references): {renderer_path}")
    sys.exit(0)

renderer_path.write_text(src)
print(f"Patched {renderer_path}")
print(f"  removed {original.count('polyfill') - src.count('polyfill')} polyfill references")

# Invalidate cached .pyc
import importlib

importlib.invalidate_caches()
print("Cache invalidated. Restart the server to apply.")
