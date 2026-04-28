#!/usr/bin/env bash
set -euo pipefail
uv run pytest
uv run ruff check .
uv build
echo "Build complete. Artifacts in dist/."
