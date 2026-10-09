# Changelog

All notable changes to NetCore. Format follows [Keep a Changelog](https://keepachangelog.com/);
this project uses [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-10-09

### Fixed
- **The backend could not start at all.** `Settings` no longer defined
  `OPENAI_API_KEY` / `OPENAI_MODEL`, but the config validation block read
  `settings.OPENAI_API_KEY`, so `import main` raised
  `AttributeError: 'Settings' object has no attribute 'OPENAI_API_KEY'` and every entry
  point (API, CLI, Docker, docs) was dead. A regression introduced in `5e43b24`, which
  removed the two field definitions *and* added the validation that reads them.
- **A real `UnboundLocalError` on the config-pull path.** A redundant local
  `import re` inside `netmiko_client.pull_running_config()` made `re` function-local, so
  the `re.search()` call above it raised
  `UnboundLocalError: cannot access local variable 're'`. Caught by ruff's `F823`.
- **Syntax errors in both CLI entry points** — `routers/chat.py` had a docstring indented
  eight spaces inside a four-space function; `scripts/cli.py` had a string literal split
  by real newlines; `scripts/nethermind.py` read a module global before its `global`
  declaration. Each one made the tree uncompilable.
- **The containerised stack never worked.** The "production" frontend image ran
  `npm run dev` — a *development* server shipped as the artifact, as root — and
  `docker-compose.yml` masked the built image three ways (`command: npm run dev`, a
  `./frontend:/app` bind mount, and an anonymous `/app/node_modules` volume), so the
  container crash-looped with `sh: next: not found`.
- **The backend image could not build.** Installing `libssl-dev` failed outright
  (`libssl3t64` pinned to one version while a different one was offered); `apt` is now
  gone entirely, since every dependency ships a manylinux wheel.
- Frontend healthcheck could never pass — it probed a host-side port that does not exist
  inside the container.
- `CORS_ORIGINS` did not include `http://127.0.0.1:3000`, so opening the UI via the IP
  form failed CORS. Both spellings are now allowed by default.

### Added
- **Test suite (11 tests)** — app metadata, OpenAPI route presence, dashboard stats shape,
  switch create/read-back, and five pure-logic tests of the ArubaOS/ProCurve
  running-config parser. The database is redirected to a temp file before import, so a
  test run never touches your real `switches.db`.
- `.dockerignore` for both build contexts — without them the 539 MB `node_modules`, the
  `.git` directory and any local `.env` would have been baked into the images.
- `HEALTHCHECK` instructions for both images.
- Real screenshots in `docs/media/`.

### Changed
- 288 `ruff` errors resolved (the repo configured ruff but failed it everywhere). `B008`
  is ignored deliberately: FastAPI *requires* `Depends()` in argument defaults.
- Both containers now run as **non-root** (`uid=1000`).
- Compose publishes only to `127.0.0.1`.
- Removed the obsolete `version:` attribute from `docker-compose.yml`.

### Security
- `gitleaks`: clean. `trivy`: 0 CRITICAL/HIGH; both Dockerfiles 0 findings
  (previously 1 HIGH for a root-running image).
