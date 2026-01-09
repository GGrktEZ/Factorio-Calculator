# Factorio Recipe Calculator

An interactive tool for calculating production chains in Factorio.

## Features

- **Interactive Wizard Interface**: Browse recipes organized by planet and category
- **Production Chain Calculation**: Automatically calculates required machines and ingredient rates
- **Multi-level Tree View**: Shows complete production chains with nested ingredient requirements
- **Belt Speed Options**: Calculate for Yellow, Red, Blue, or Green belts
- **File Output**: Saves calculation trees to nicely formatted text files with ASCII art
- **Verbose & Compact Modes**: Choose between detailed or simplified output
- **Clean Logging**: Logs show important decisions without cluttering with calculation details

## Installation

1. Ensure Python 3.10+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Optional: create a .env (copy from .env.example) to override defaults

## Usage

### Wizard Mode (Interactive - Default)

Run the program with the interactive wizard:

```bash
python main.py
```

**How to use the wizard:**

1. **Select a Recipe**: Navigate the tree on the left using arrow keys or mouse
   - Expand categories by clicking the arrows or pressing Space/Enter
   - Click on a recipe name to select it
   
2. **Choose Belt Color**: Use the dropdown to select:
   - Yellow Belt (15 items/s)
   - Red Belt (30 items/s)
   - Blue Belt (45 items/s)
   - Green Belt (60 items/s)

3. **Calculate**: Press `Enter` or click the "Calculate" button

4. **View Results**: The wizard closes and creates a formatted text file in the `calculation trees` folder
   - Contains a nicely formatted ASCII tree structure
   - Shows all machines, production rates, and ingredient dependencies
   - Verbose mode shows detailed machine configurations
   - Compact mode shows essential information only

**Keyboard Shortcuts:**
- `Enter` - Calculate selected recipe
- `q` - Quit application
- `d` - Toggle dark/light mode
- Arrow keys - Navigate recipe tree
- Space - Expand/collapse tree nodes

### CLI Mode (Legacy)

Run the program using configuration from Config.json:

```bash
python main.py --cli
```

This mode reads settings from `Config.json` and outputs results to the console.

## Configuration (CLI Mode Only)

Edit `Config.json` to set:

```json
{
    "belt_color": "green",
    "product": "transport_belt",
    "verbose": true,
    "consoleLogging": false
}
```

## Project Structure

- `Main.py` - Entry point for both wizard and CLI modes
- `calculator.py` - Production chain calculation logic
- `file_output.py` - ASCII tree file generation
- `loader.py` - JSON data loading utilities (.env-configurable)
- `logger_config.py` - Central logging setup
- `models.py` - Data models for recipes, machines, and products
- `settings.py` - Environment-based settings loader (.env)
- `textual_wizzard.py` - Interactive wizard interface
- `utils.py` - Shared utility functions
- `base.json` - Game data (recipes, machines, belts)
- `Config.json` - User configuration (CLI mode)
- `calculation trees/` - Output folder for generated calculation files
- `.env.example` / `.env` - Environment configuration
- `requirements.txt` - Python dependencies
- `documentation.md` - Development history and design decisions
- `__pycache__/` - Python bytecode cache (auto-generated)


## Development History

### Version 2.0 - Interactive Wizard Interface
- Added Textual-based TUI wizard for interactive recipe selection
- Implemented tree-based recipe browser with category hierarchies
- Made wizard mode the default, CLI mode available via `--cli` flag
- Added file output for calculation trees

### Version 1.5 - Recipe Category Refactoring
- Separated machine selection (`preferred_machine`) from UI categorization (`category`)
- Transformed `category` into hierarchical array for better UI organization
- Maintained backward compatibility for legacy data structures
- See [documentation.md](documentation.md) for detailed migration notes

### Version 1.0 - CLI Calculator
- Basic command-line calculator using `Config.json`
- Machine selection and production rate calculations
- Console output with tree-structured production plans

## Example Output

When you calculate "Electronic Circuit" with a Green Belt (60 items/s) in verbose mode,
a file is created in the `calculation trees` folder:

```
════════════════════════════════════════════════════════════════════════════════
  FACTORIO PRODUCTION CALCULATOR
════════════════════════════════════════════════════════════════════════════════

Recipe:      Electronic Circuit
Belt:        Green Belt (60 items/s)
Generated:   2026-01-06 10:12:34
Mode:        Verbose

════════════════════════════════════════════════════════════════════════════════

└──  Electronic Circuit
    ┌─ Machine Configuration
    │  Type:         Assembling Machine
    │  Speed:        1.25x
    │  Productivity: 0%
    │
    ├─ Production Details
    │  Target Rate:  60.00 items/s
    │  Per Machine:  2.50 items/s
    │  Machines:     24.00
    │
    └─ Required Ingredients (2)
       ├──  Copper Cable (180.00/s) [Crafted]
       │   └──  Copper Cable
       │       (... nested tree continues ...)
       └──   Iron Plate (60.00/s) [Raw]

════════════════════════════════════════════════════════════════════════════════
  End of calculation
════════════════════════════════════════════════════════════════════════════════
```

## Future Improvements
- Sort recipes alphabetically in the wizard tree
- Add custom belt speeds support
- Add belt balancer and ammount calculations

## Development

This project was developed as part of Module M122 Python Project at GIBZ.

## License

Educational project - no license specified.
