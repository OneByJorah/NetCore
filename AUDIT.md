# NetCore — Audit (2026-10-08, Stage 1)

Baseline recorded before any change. Every claim below came from a command run locally
against a clean clone.

## Baseline

| Check | Result |
|---|---|
| Clone | clean, branch `master` |
| Stack | FastAPI 0.115.6 + SQLAlchemy 2.0.36 + Alembic + Netmiko 4.4.0 + OpenAI SDK, Python **3.12** target (`pyproject.toml` `target-version = "py312"`) |
| Size | 31 Python files, ~7,254 lines |
| `import main` | **FAILED — `AttributeError: 'Settings' object has no attribute 'OPENAI_API_KEY'`** |
| Routes | 0 (app could not be constructed) |
| Tests | **none** — `tests/` contains only `mock_switch.py`; `pyproject.toml` declares `testpaths = ["tests"]`, `python_files = ["test_*.py"]` |
| `ruff check .` | **285 errors, 189 auto-fixable** |
| `gitleaks detect` | clean |

## Toolchain obstacle (real, not a defect)

The host's default interpreter is **Python 3.14.7**. Several pinned deps (`psycopg2-binary`,
`pydantic-core 2.27.2`) have no 3.14 wheels and fail to build, and Python 3.14 is far ahead
of the repo's declared 3.12 target.

Resolution: system `python3.12` exists, but `python3.12 -m venv` is unavailable on this
image (Debian splits `python3.12-venv` out) and system pip is PEP 668–blocked. Used **`uv`**
(0.11.30, already installed) to create the venv: `uv venv --python 3.12 .venv` +
`VIRTUAL_ENV=... uv pip install -r backend/requirements.txt`. All pins installed, including
`psycopg2-binary`. **This is a documented environment gap, not a repo bug** — the repo's own
target is correct.

## Findings

### N1 — CRITICAL: the backend cannot start (fixed)
`backend/config.py` read `settings.OPENAI_API_KEY` in its validation block (line 61), but
the `Settings` model **never defined that field** — nor `OPENAI_MODEL`.

Git history pins the regression precisely: commit **`5e43b24`**
("chore(maintenance): audit fixes, screenshots", authored 2026-10-07 by `openhands`)
**deleted** these two lines from `Settings`:

```python
# OpenAI / AI
OPENAI_API_KEY: Optional[str] = None
OPENAI_MODEL: str = "gpt-4o"
```

…while in the *same commit* adding the validation `if not settings.OPENAI_API_KEY:` that
reads them. Every commit before `5e43b24` defined the fields, so **the app was importable
until that commit and broken after it**.

Impact: `uvicorn main:app` dies at import. Nothing works — API, CLI, Docker, docs.

**Fix:** restored both fields. Verified: `import main` → OK, **67 routes** registered.

### N2 — CRITICAL: syntax error in `backend/routers/chat.py` (fixed)
Line 18's docstring was indented 8 spaces inside a 4-space function body →
`IndentationError: unindent does not match any outer indentation level`. This blocked
`main.py` on the line *after* N1 was cleared.

**Fix:** indentation corrected.

### N3 — syntax error in `scripts/cli.py` (fixed)
Line 151 contained a string literal broken by real newlines:
`config_text = "⏎".join(...)` → `SyntaxError: unterminated string literal`.

**Fix:** restored the `\n` escapes.

### N4 — syntax error in `scripts/nethermind.py` (fixed)
`main()` read module-global `API_BASE` at line 251 (inside an f-string for `--help`) but
declared `global API_BASE` at line 329 → `SyntaxError: name 'API_BASE' is used prior to
global declaration`.

**Fix:** moved the `global` declaration to the top of `main()`. Verified `--help` runs.

### N5 — 285 ruff errors (not fixed, reported)
Against the repo's own configured rule set (`E,F,W,I,UP,B,SIM`, line-length 120). 189 are
auto-fixable. Not auto-fixed in this pass: a 285-error sweep is a broad, low-risk-but-large
diff that should be its own reviewed PR rather than mixed into a critical-fix branch.
Recorded as the next roadmap item.

## Not verified (honest gaps)
- **No frontend build.** The UI is a separate Next.js app; it was not built or screenshotted in this pass.
- **No real switch was contacted.** All testing is against the API with an empty database; the Netmiko/proxy paths were not exercised against hardware.
- **No Docker** on this host → `docker-compose.yml` not exercised.
- N1–N4 were fixed and verified by import + live HTTP, but the app's *behaviour* on real
  config pushes remains unverified.
