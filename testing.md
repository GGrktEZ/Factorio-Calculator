# Factorio Calculator - Test Protocol

---

## Test Cases

### 1 CLI - Happy Path (Green Belt, Verbose)
**Config.json (set exactly):**
```json
{
   "belt_color": "green",
   "product": "electronic_circuit",
   "verbose": "true",
   "consoleLogging": "false"
}
```
**Steps:**
1. `python .\Main.py --cli`
2. Observe console tree; note belt speed 60/s.
3. Confirm output file created in `calculation trees/`.
4. Note log message showing log path.
**Pass if:**
- No errors; console shows verbose machine details; output file exists with current timestamp; log file at project root.
**Fail if:**
- Exceptions, missing output file, or log written elsewhere.

---

### 2) CLI - Different Belt (Yellow, Compact)
**Config.json:**
```json
{
   "belt_color": "yellow",
   "product": "electronic_circuit",
   "verbose": "false",
   "consoleLogging": "false"
}
```
**Steps:**
1. `python .\Main.py --cli`
2. Check belt speed prints 15/s; output file name includes `yellow_belt`.
3. Compare machine count is higher than green-belt runs.
**Pass if:**
- Belt speed 15/s; compact output (no machine speed/productivity lines); Machine ammount changed to fit new belt speed; file saved with yellow_belt in name.
**Fail if:**
- Verbose info appears, speed not 15/s, or file not created.

---

### 3) CLI - Invalid Recipe Error Path
**Config.json:**
```json
{
   "belt_color": "green",
   "product": "nonexistent_recipe_xyz",
   "verbose": "true",
   "consoleLogging": "false"
}
```
**Steps:**
1. `python .\Main.py --cli`
2. Observe console error message.
3. Check log for the same error text.
**Pass if:**
- Message "Recipe 'nonexistent_recipe_xyz' not found!" shown; no calculation tree file created; program exits gracefully; log entry recorded.
**Fail if:**
- Unhandled exception, crash, or no error message.

---

### 3.5) CLI - Invalid Belt Error Path
**Config.json:**
```json
{
   "belt_color": "pink",
   "product": "electric_engine_unit",
   "verbose": "true",
   "consoleLogging": "false"
}
```
**Steps:**
1. `python .\Main.py --cli`
2. Observe console error message.
3. Check log for the same error text.
**Pass if:**
- Message "Belt color 'pink' not found!" shown; no calculation tree file created; program exits gracefully; log entry recorded.
**Fail if:**
- Unhandled exception, crash, or no error message.

---

### 4) CLI - Corrupted Config Handling
**Config.json:** make it invalid JSON (e.g., remove final `}`).
**Steps:**
1. `python .\Main.py --cli`
2. Observe error about invalid JSON.
3. Restore Config.json after test.
**Pass if:**
- Clear JSON error shown in log file; no crash loop.
**Fail if:**
- Silent failure or misleading message.

---

### 5) Wizard - Launch and Calculate
**Steps:**
1. `python .\Main.py`
2. In UI, expand a category and select a recipe (e.g., Iron Gear Wheel).
3. Select a belt color (default green).
4. Leave Verbose unchecked; click Calculate.
5. Click Calculate.
6. Verify output file appears in `calculation trees/` with selected belt (default green).
**Pass if:**
- UI loads; selection works; calculation completes; file saved; no errors or logical mistakes.
**Fail if:**
- UI fails to load, calculate button does nothing, or no file is created.

---

### 6) Wizard - Verbose Toggle
**Steps:**
1. Run wizard.
2. Select a recipe; ensure "Verbose Output" is checked; Calculate.
3. Re-run wizard, uncheck "Verbose Output"; same recipe; Calculate.
4. Compare the two files (verbose has machine speed/productivity; compact does not).
**Pass if:**
- Toggle changes detail level; both files valid, correctly named and saved.
**Fail if:**
- Toggle has no effect or files missing.

---

### 7) Wizard - No Recipe Selected Error
**Steps:**
1. Run wizard.
2. Do not select a recipe; click Calculate.
**Pass if:**
- Error message shown: "ERROR: Please select a recipe first!"; Logger shows correct WARNING; app stays running.
**Fail if:**
- Crash or no error feedback. 
---

### 8) Output & Logging Verification
**Prereq:** Run any successful CLI or wizard test first.
**Steps:**
1. Check latest file in `calculation trees/` for header, recipe, belt, timestamp, ASCII tree, footer "End of calculation".
2. Verify `factorio_calculator.log` exists at project root; tail last 10 lines.
**Pass if:**
- File is well-formatted and UTF-8; log shows recent entries for the run.
**Fail if:**
- Formatting broken, missing sections, or log absent/wrong path.

---

## Quick Commands
```powershell
# CLI runs (edit Config.json per test before running)
python .\Main.py --cli

# Wizard
python .\Main.py

# Inspect outputs
Get-ChildItem "./calculation trees" -File | Sort-Object LastWriteTime -Descending | Select-Object -First 3
Get-Content .\factorio_calculator.log -Tail 20
```

---