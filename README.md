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

### Option 1: Using Docker (Recommended)

1. Ensure Docker is installed on your system
2. Pull or download the repository
3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

**Docker Benefits:**
- No Python installation required
- Consistent environment across all systems
- Automatic dependency management
- Output files saved to your local `calculation trees` folder

### Option 2: Local Python Installation

1. Ensure Python 3.10+ is installed
2. Pull or download the repository
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Optional: create a .env (copy from .env.example) to override defaults

## Usage

### Wizard Mode (Interactive - Default)

**With Docker:**
```bash
docker-compose run --rm factorio-calculator
```

**Local Python:**
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

**With Docker:**
```bash
docker-compose run --rm factorio-calculator python Main.py --cli
```

**Local Python:**
```bash
python main.py --cli
```

This mode reads settings directly from `Config.json` and outputs results to the console.

## Docker Commands

### Build the Docker image
```bash
docker-compose build
```

### Run in interactive wizard mode
```bash
docker-compose run --rm factorio-calculator
```

### Run in CLI mode
```bash
docker-compose run --rm factorio-calculator python Main.py --cli
```

### Run with custom configuration
```bash
# Edit data/Config.json first, then:
docker-compose run --rm factorio-calculator python Main.py --cli
```

### View output files
Output files are automatically saved to the `calculation trees` folder on your host machine.

### Clean up Docker resources
```bash
docker-compose down
docker rmi factorio-calculator:latest
```

## Project Structure

### Root Directory
- `Main.py` - Entry point launcher (calls src/Main.py)
- `README.md` - This file
- `testing.md` - Test protocol and cases
- `requirements.txt` - Python dependencies
- `documentation.md` - Development history and design decisions
- `.env.example` / `.env` - Environment configuration
- `factorio_calculator.log` - Application log file

### src/ - Python Source Code
- `Main.py` - Application entry point for both wizard and CLI modes
- `calculator.py` - Production chain calculation logic
- `file_output.py` - ASCII tree file generation
- `loader.py` - JSON data loading utilities
- `logger_config.py` - Central logging setup
- `models.py` - Data models for recipes, machines, and products
- `settings.py` - Environment-based settings loader
- `textual_wizzard.py` - Interactive wizard interface
- `utils.py` - Shared utility functions

### data/ - Configuration and Game Data
- `base.json` - Game data (recipes, machines, belts)
- `Config.json` - User configuration (CLI mode)

### calculation trees/ - Output Folder
- Generated calculation files with timestamped names
- Format: `{recipe}_{belt}_belt_{mode}_{timestamp}.txt`


## Development History

### Version 1.0 - CLI Calculator
- Basic command-line calculator using `Config.json`
- Machine selection and production rate calculations
- Console output with tree-structured production plans

### Version 1.5 - Recipe Category Refactoring
- Separated machine selection (`preferred_machine`) from UI categorization (`category`)
- Transformed `category` into hierarchical array for better UI organization
- Maintained backward compatibility for legacy data structures
- See [documentation.md](documentation.md) for detailed migration notes

### Version 2.0 - Interactive Wizard Interface
- Added Textual-based TUI wizard for interactive recipe selection
- Implemented tree-based recipe browser with category hierarchies
- Made wizard mode the default, CLI mode available via `--cli` flag
- Added file output for calculation trees

### Version 2.1 - File structure & code quality improvements
- better seperation of logic into packages and modules
- added .env, requirements and settings.py for configuration
- pydocstring improvements and code cleanup
- logging improvements
- add multiple test scenarios for valuation

## Example Output

When you calculate "Electronic Circuit" with a Green Belt (60 items/s) in non verbose mode,
a file is created in the `calculation trees` folder:

```
════════════════════════════════════════════════════════════════════════════════
  FACTORIO PRODUCTION CALCULATOR
════════════════════════════════════════════════════════════════════════════════

Recipe:      Advanced Circuit
Belt:        Green Belt (60 items/s)
Generated:   2026-01-09 10:07:52
Mode:        Compact

════════════════════════════════════════════════════════════════════════════════

└── [Product] Advanced Circuit
    Machine: Electromagnetic Plant x120.00
    Target:  60.00 items/s
    
    Ingredients:
       ├── [Crafted] Copper Cable (240.00/s)
       │   ├── [Product] Copper Cable
       │   │   Machine: Electromagnetic Plant x20.00
       │   │   Target:  240.00 items/s
       │   │   
       │   │   Ingredients:
       │   │      └── [Raw] Copper Plate (120.00/s)
       ├── [Crafted] Electronic Circuit (120.00/s)
       │   ├── [Product] Electronic Circuit
       │   │   Machine: Electromagnetic Plant x20.00
       │   │   Target:  120.00 items/s
       │   │   
       │   │   Ingredients:
       │   │      ├── [Crafted] Copper Cable (360.00/s)
       │   │      │   ├── [Product] Copper Cable
       │   │      │   │   Machine: Electromagnetic Plant x30.00
       │   │      │   │   Target:  360.00 items/s
       │   │      │   │   
       │   │      │   │   Ingredients:
       │   │      │   │      └── [Raw] Copper Plate (180.00/s)
       │   │      └── [Raw] Iron Plate (120.00/s)
       └── [Raw] Plastic Bar (120.00/s)

════════════════════════════════════════════════════════════════════════════════
  End of calculation
════════════════════════════════════════════════════════════════════════════════
```

## Future Improvements
- Sort recipes alphabetically in the wizard tree
- Add custom belt speeds support
- Add belt balancer and ammount calculations
- auto deleting of old calculation trees based on age or count

## Development

This project was developed as part of Module M122 Python Project at GIBZ.
