"""Shared pytest fixtures."""

import os

import pytest


@pytest.fixture(autouse=True)
def _stub_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    """Provide deterministic credentials so Settings loads cleanly in tests."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setattr(os, "environ", os.environ.copy())
