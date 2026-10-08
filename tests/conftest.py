"""Pytest configuration for NetCore.

Isolates the database to a temporary SQLite file *before* `main` is imported, so a
test run never touches the real `switches.db`.
"""
import os
import sys
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"


def pytest_configure():
    """Before collection: make `import main` work and redirect the database."""
    if str(BACKEND_DIR) not in sys.path:
        sys.path.insert(0, str(BACKEND_DIR))
    # settings/database read this at import time, so it must be set first.
    # Use a temp directory outside the repo so no stray .db is created in-tree.
    db_dir = tempfile.mkdtemp(prefix="netcore-tests-")
    os.environ["DATABASE_URL"] = f"sqlite:///{db_dir}/test_switches.db"


@pytest.fixture()
def client():
    """A TestClient bound to the app, created per test."""
    from main import app

    with TestClient(app) as c:
        yield c
