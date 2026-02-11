"""Pytest configuration. Adds project root to path for imports."""

import sys
from pathlib import Path

# Add project root so `from agent import ...` works
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
