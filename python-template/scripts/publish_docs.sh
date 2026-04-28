#!/usr/bin/env bash
set -euo pipefail
uv run mkdocs gh-deploy --force
