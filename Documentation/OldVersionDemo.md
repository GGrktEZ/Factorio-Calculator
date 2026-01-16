# Development History

## Quality & Structure Updates (2026-01-07)
- Introduced `factorio_calc/` package to group related modules
- Added `.env` (with `.env.example`) and `settings.py` to remove hard-coded config (BASE_JSON, CONFIG_JSON, logging, defaults)
- Renamed entry point to `main.py` for a clear, conventional start script
- Created `requirements.txt` (textual, python-dotenv)
- Removed unused imports and tightened wizard imports; converted legacy top-level modules into thin compatibility wrappers
- Standardized naming and formatting; improved docstrings where applicable
- Logging now respects `.env` (`LOG_DIR`, `LOG_CONSOLE`) with safe defaults

## Recipe Category Refactoring

The recipe data structure underwent a significant refactoring to separate machine selection from UI categorization.

### Old Structure (Single-purpose `category`)
```json
"electronic_circuit": {
  "category": "electromagnetics",
  "time": 0.5,
  "ingredients": [
    { "name": "iron_plate", "amount": 1 },
    { "name": "copper_cable", "amount": 3 }
  ],
  "products": [{ "name": "electronic_circuit", "amount": 1 }],
  "allow_productivity": true
}
```

The `category` field served a dual purpose:
- Determining which machine could craft the recipe
- (Implicitly) organizing recipes in UI

### New Structure (Separation of Concerns)
```json
"electronic_circuit": {
  "preferred_machine": "electromagnetics",
  "category": ["Intermediates", "Fulgora", "Circuits"],
  "time": 0.5,
  "ingredients": [
    { "name": "iron_plate", "amount": 1 },
    { "name": "copper_cable", "amount": 3 }
  ],
  "products": [{ "name": "electronic_circuit", "amount": 1 }],
  "allow_productivity": true
}
```

### Benefits
- **`preferred_machine`**: Explicitly defines which machine category to use for crafting
- **`category`**: Now an array defining the UI hierarchy path for the wizard tree view
- **Better separation of concerns**: Machine logic vs. UI organization
- **Backward compatibility**: Maintained in `Recipe.from_dict()` for legacy data

### Notes
- Category paths can be adjusted in `base.json` to refine recipe grouping in the wizard UI
- The calculator uses `preferred_machine` to select the best machine for each recipe

