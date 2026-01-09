"""
Factorio Calculator - Entry Point

This is a launcher that imports and runs the main application from the src folder.
"""
import sys
from pathlib import Path

# Add src folder to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Import and run the main module
from Main import run_cli_mode, run_wizard_mode

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli_mode()
    else:
        run_wizard_mode()
