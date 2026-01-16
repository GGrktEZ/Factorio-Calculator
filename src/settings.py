"""Central settings module. 

Loads environment variables from .env file and provides app-wide configuration
with sensible defaults. All paths and behaviors can be customized via .env.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    _ROOT = Path(__file__).resolve().parent.parent
    load_dotenv(dotenv_path=_ROOT / ".env", override=False)
except Exception:
    pass

# Project root directory (parent of src folder)
ROOT_DIR: Path = Path(__file__).resolve().parent.parent

# Data files (loaded from data/ folder)
BASE_JSON: str = os.getenv("BASE_JSON", str(ROOT_DIR / "data" / "base.json"))
CONFIG_JSON: str = os.getenv("CONFIG_JSON", str(ROOT_DIR / "data" / "Config.json"))

# Logging configuration
LOG_DIR: str = os.getenv("LOG_DIR", str(ROOT_DIR))
LOG_CONSOLE: bool = os.getenv("LOG_CONSOLE", "false").lower() == "true"

# Wizard mode defaults
DEFAULT_BELT: str = os.getenv("DEFAULT_BELT", "green")
DEFAULT_VERBOSE: bool = os.getenv("DEFAULT_VERBOSE", "false").lower() == "true"

# Output folder for calculation results
OUTPUT_FOLDER_NAME: str = os.getenv("OUTPUT_FOLDER", "calculation trees")
