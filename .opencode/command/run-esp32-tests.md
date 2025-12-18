# run-unit-tests

Purpose
- A reusable assistant prompt for running ESP32 component unit tests in this repository.

When to use
- Use this prompt when you want the assistant to run one or more component unit tests using the repository's test runner at `tests/apps/test.py`.

Requirements (environment)
- ESP-IDF installed and available under `~/esp/esp-idf` with `export.sh` present.
- A Python 3 interpreter available as `python3`.
- Device connected for flashing and serial capture (default serial port: `/dev/ttyACM0`) when tests require hardware.
- Necessary toolchain and IDF Python virtualenv (the project already expects `~/.espressif/python_env/*`).

Inputs / Parameters (use natural language or explicit flags)
- `tests`: optional list of test names to run (examples: `crypto_utils_test`, `wifi_manager_test`). If omitted, run all available app tests.
- `port` (optional): serial port path (default: `/dev/ttyACM0`).
- `target` (optional): IDF target (default: `esp32c3`).
- `output` (optional): report filename to write into `tests/apps/` (default: `report.txt`).

Behavior & steps the assistant should perform

1. Ensure prerequisites exist:
   - Check that `~/esp/esp-idf/export.sh` exists and is readable. If missing, inform the user and stop.
   - Optionally check that the specified serial port exists. If not found, warn but continue (the test runner may create/skip tests).
2. Run the repository test runner script located at `tests/apps/test.py` with defaults to run all tests.
   - Command: `python3 tests/apps/test.py`
3. Capture console output and ensure that the following artifacts are produced/updated:
   - `tests/apps/report.txt` (or the provided `--output` file)
   - `tests/apps/build.log`
   - `tests/apps/serial.log`
4. On failures, attempt fix-and-rerun per component:
   - For each failing component, detect the primary reason: build failed, flash failed, monitor/serial failed, or crash detected.
   - Apply safe, non-destructive remediation based on the reason:
     - Build failed: trigger a clean rebuild for that app by re-running the component with the runner. If configuration/cache issues persist, remove the test app's `build/` directory and retry (one time) before proceeding.
     - Port unavailable: re-run the component with `--force-free-port`. If multiple ports are present, prefer the original `-p`; otherwise, try a likely `/dev/ttyACM*`/`/dev/ttyUSB*` candidate.
     - Flash failed: retry once; if persistent, extend flash timeout and retry again.
     - Monitor/serial failed: wait briefly (2s), reopen serial, increase monitor timeout to 60s, then retry.
     - Crash detected: surface crash context for diagnosis; re-run once to confirm reproducibility. Do not auto-modify source code.
   - Re-run the isolated test until it passes or a maximum of 2 retries are exhausted, using: `python3 tests/apps/test.py <component> [flags]`.
   - After a test passes, immediately continue with remaining tests. Record which remediation steps were applied.
5. If requested, continue debugging a specific component interactively (additional manual re-runs or deeper analysis).
6. Commit confirmed fixes:
   - After a failing component has been fixed and reruns are passing, stage and commit only the relevant changes (avoid committing logs or unrelated files).
   - Use a concise, purpose-driven message focusing on the why. Example:
     - `git add <changed-files>`
     - `git commit -m "fix(<component>): stabilize unit test by <reason>"`

Expected outputs from the assistant
- Console summary of which tests were run and pass/fail status.
- Paths to generated artifacts: `tests/apps/report.txt`, `tests/apps/build.log`, `tests/apps/serial.log`.
- If failures: a short actionable diagnostic (build errors snippet or serial crash excerpt) and suggested next steps.

Failure handling
- If `~/esp/esp-idf/export.sh` is missing: stop and ask the user to install/point to ESP-IDF.
- If serial port is missing or busy: warn and offer to continue (build-only) or ask for correct port.
- If `idf.py` fails on `set-target` or `build`: capture errors and include snippets in the reply.

Examples (invocations)
- Run everything with defaults:
  - `Run the repo unit tests using the default port and target.`
- Run a single test:
  - `Run the crypto_utils_test on /dev/ttyACM0 for target esp32c3 and save report as run_crypto.txt.`
- Re-run a failed test:
  - `Re-run wifi_manager_test on /dev/ttyACM0`.

Notes for the assistant
- Do not assume `pytest` — this repository uses the custom test runner script `tests/apps/test.py`.
- Prefer showing short excerpts (first few build errors, last ~40 serial lines) unless the user asks for full logs.
- Ask the user before taking destructive actions (killing processes using the serial port). If a port appears busy, inform the user and request permission to kill processes.

---

Version: 1.0
Created-by: repo assistant
Created-at: automatically when invoked
