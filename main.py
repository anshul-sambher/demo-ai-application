"""Entry point for running the Gen Z investment advisor demo."""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure the src directory is on the path when running as a script.
SRC_PATH = Path(__file__).resolve().parent / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from investment_app.app import main as _main


def main() -> None:  # pragma: no cover - thin wrapper
    _main()


if __name__ == "__main__":
    main()
