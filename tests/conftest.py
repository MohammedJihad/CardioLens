"""Make `import src...` work no matter how pytest is invoked.

Adds the project root to sys.path so `pytest -q` works directly, without
requiring `PYTHONPATH=.`. (pyproject.toml also sets pythonpath for pytest >= 7;
this conftest is the belt-and-suspenders fallback for any version/invocation.)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
