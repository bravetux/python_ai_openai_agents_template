"""Convenience launcher. Equivalent to `python -m {{ project_slug_underscore }}`."""

from {{ project_slug_underscore }}.__main__ import cli

if __name__ == "__main__":
    cli()
