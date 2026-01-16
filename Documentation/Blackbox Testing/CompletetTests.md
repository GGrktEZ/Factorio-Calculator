# Factorio Calculator - Completed Tests (Evidence)

---

## Test Case 1: CLI - Happy Path (Green Belt, Verbose)

**Status:** ✅ PASS 

**Description:**
Test the CLI with default green belt and verbose output enabled.

**Configuration Used:**
```json
{
   "belt_color": "green",
   "product": "electronic_circuit",
   "verbose": "true",
   "consoleLogging": "false"
}
```

**Screenshots:**
- Console Output:
  ![alt text](Screenshots/Test1_1.png)
- Output File in calculation trees/:
  ![alt text](Screenshots/Test1_2.png)
- Log File Verification:
  ![alt text](Screenshots/Test1_3.png)

**Observations:**
- Belt speed displayed: 60/s 
- Console shows verbose machine details: 
- Output file created with current timestamp: 
- Log file created at project root: 
- No exceptions or errors: 

---

## Test Case 2: CLI - Different Belt (Yellow, Compact)

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Test the CLI with yellow belt and compact (non-verbose) output.

**Configuration Used:**
```json
{
   "belt_color": "yellow",
   "product": "electronic_circuit",
   "verbose": "false",
   "consoleLogging": "false"
}
```

**Screenshots:**
- Console Output (should be compact):
  ![Add screenshot of console output here]
- Output File with yellow_belt in filename:
  ![Add screenshot of file explorer here]
- File Content Comparison (vs Test Case 1):
  ![Add screenshot comparing verbose vs compact output here]

**Observations:**
- Belt speed displayed: 15/s ✅ / ❌
- Compact output (no machine speed/productivity lines): ✅ / ❌
- Machine count adjusted for slower belt speed: ✅ / ❌
- Filename includes `yellow_belt`: ✅ / ❌
- No verbose info appears: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Test Case 3: CLI - Invalid Recipe Error Path

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Test error handling when an invalid/non-existent recipe is specified.

**Configuration Used:**
```json
{
   "belt_color": "green",
   "product": "nonexistent_recipe_xyz",
   "verbose": "true",
   "consoleLogging": "false"
}
```

**Screenshots:**
- Console Error Message:
  ![Add screenshot of error message here]
- Log File showing error entry:
  ![Add screenshot of log file here]

**Observations:**
- Error message displayed: "Recipe 'nonexistent_recipe_xyz' not found!" ✅ / ❌
- No calculation tree file created: ✅ / ❌
- Program exits gracefully (no crash): ✅ / ❌
- Error logged in log file: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Test Case 3.5: CLI - Invalid Belt Error Path

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Test error handling when an invalid belt color is specified.

**Configuration Used:**
```json
{
   "belt_color": "pink",
   "product": "electric_engine_unit",
   "verbose": "true",
   "consoleLogging": "false"
}
```

**Screenshots:**
- Console Error Message:
  ![Add screenshot of error message here]
- Log File showing error entry:
  ![Add screenshot of log file here]

**Observations:**
- Error message displayed: "Belt color 'pink' not found!" ✅ / ❌
- No calculation tree file created: ✅ / ❌
- Program exits gracefully (no crash): ✅ / ❌
- Error logged in log file: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Test Case 4: CLI - Corrupted Config Handling

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Test error handling when Config.json contains invalid JSON syntax.

**Configuration Used:**
Invalid JSON (removed final `}`)

**Screenshots:**
- Console Error Message:
  ![Add screenshot of error message here]
- Log File showing JSON error:
  ![Add screenshot of log file here]

**Observations:**
- Clear JSON error shown in log file: ✅ / ❌
- No crash loop or silent failure: ✅ / ❌
- Config.json restored successfully after test: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Test Case 5: Wizard - Launch and Calculate

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Test the Textual wizard UI to launch, select a recipe, and perform a calculation.

**Steps Performed:**
1. Launched wizard with `python .\Main.py`
2. Expanded a category and selected "Iron Gear Wheel" (or other recipe)
3. Selected green belt (default)
4. Left Verbose unchecked
5. Clicked Calculate

**Screenshots:**
- Wizard UI Initial State:
  ![Add screenshot of wizard UI here]
- Category/Recipe Selection:
  ![Add screenshot of selection here]
- Belt Color Selection:
  ![Add screenshot of belt selection here]
- Calculation in Progress:
  ![Add screenshot of calculation process here]
- Output File Generated:
  ![Add screenshot of file in calculation trees/ here]

**Observations:**
- UI loads without errors: ✅ / ❌
- Category expansion works: ✅ / ❌
- Recipe selection works: ✅ / ❌
- Belt color selection works: ✅ / ❌
- Calculate button executes successfully: ✅ / ❌
- Output file created in `calculation trees/`: ✅ / ❌
- No errors or logical mistakes: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Test Case 6: Wizard - Verbose Toggle

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Test that the Verbose Output toggle changes the detail level of output files.

**Steps Performed:**
1. Run 1: Selected recipe with Verbose Output checked → Calculate
2. Run 2: Selected same recipe with Verbose Output unchecked → Calculate
3. Compared the two output files

**Screenshots:**
- Wizard with Verbose Checked:
  ![Add screenshot here]
- Wizard with Verbose Unchecked:
  ![Add screenshot here]
- Verbose Output File Content:
  ![Add screenshot showing detailed output here]
- Compact Output File Content:
  ![Add screenshot showing compact output here]
- File Comparison (side-by-side):
  ![Add comparison screenshot here]

**Observations:**
- Verbose checkbox toggles successfully: ✅ / ❌
- Verbose file includes machine speed/productivity details: ✅ / ❌
- Compact file excludes machine speed/productivity details: ✅ / ❌
- Both files valid and correctly named: ✅ / ❌
- Both files saved in correct location: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Test Case 7: Wizard - No Recipe Selected Error

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Test error handling when attempting to calculate without selecting a recipe.

**Steps Performed:**
1. Launched wizard
2. Did not select any recipe
3. Clicked Calculate

**Screenshots:**
- Error Message Displayed:
  ![Add screenshot of error dialog here]
- Logger Output (if visible):
  ![Add screenshot of warning in logger here]
- Application State After Error:
  ![Add screenshot showing app still running here]

**Observations:**
- Error message displayed: "ERROR: Please select a recipe first!" ✅ / ❌
- Logger shows WARNING level entry: ✅ / ❌
- Application remains running (no crash): ✅ / ❌
- User can retry the calculation: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Test Case 8: Output & Logging Verification

**Status:** ✅ PASS / ❌ FAIL

**Description:**
Verify output file formatting and logging functionality (run after any successful test).

**Steps Performed:**
1. Ran a successful CLI or wizard test (prerequisite)
2. Inspected latest output file in `calculation trees/`
3. Verified `factorio_calculator.log` at project root
4. Checked last 10 lines of log file

**Screenshots:**
- Output File Structure:
  ![Add screenshot of file content here]
- File Header Section:
  ![Add screenshot of header here]
- Recipe and Configuration Section:
  ![Add screenshot of config section here]
- ASCII Tree Content:
  ![Add screenshot of tree here]
- File Footer:
  ![Add screenshot showing "End of calculation" here]
- Log File Location:
  ![Add screenshot of project root with log file here]
- Log File Recent Entries:
  ![Add screenshot of last 20 log lines here]

**Observations:**
- Output file is well-formatted: ✅ / ❌
- File is UTF-8 encoded: ✅ / ❌
- Header section present: ✅ / ❌
- Recipe information complete: ✅ / ❌
- Belt information present: ✅ / ❌
- Timestamp included: ✅ / ❌
- ASCII tree displays correctly: ✅ / ❌
- Footer "End of calculation" present: ✅ / ❌
- Log file exists at project root: ✅ / ❌
- Log file contains recent entries: ✅ / ❌

**Notes:**
[Add any additional observations or issues encountered]

---

## Summary

| Test Case | Status | Date | Notes |
|-----------|--------|------|-------|
| 1 - CLI Happy Path (Green, Verbose) | ❌ UNTESTED | | |
| 2 - CLI Yellow Belt Compact | ❌ UNTESTED | | |
| 3 - Invalid Recipe Error | ❌ UNTESTED | | |
| 3.5 - Invalid Belt Error | ❌ UNTESTED | | |
| 4 - Corrupted Config | ❌ UNTESTED | | |
| 5 - Wizard Launch & Calculate | ❌ UNTESTED | | |
| 6 - Wizard Verbose Toggle | ❌ UNTESTED | | |
| 7 - Wizard No Recipe Error | ❌ UNTESTED | | |
| 8 - Output & Logging | ❌ UNTESTED | | |

**Overall Result:** ❓ PENDING

**Tester Name:** [Your name]

**Test Date(s):** [Date range]

**Notes:**
[Add any overall notes, environment details, or issues here]

---
