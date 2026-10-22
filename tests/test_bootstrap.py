import os
import subprocess
import sys


def test_application_imports():
    result = subprocess.run(
        [sys.executable, "-c", "from app.main import app; assert app.openapi()"],
        env={
            **os.environ,
            "SECRET_KEY": "test-secret-" * 4,
            "BASE_URL": "http://localhost:8000",
            "BASE_URL_NEXT": "http://localhost:3000",
        },
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
