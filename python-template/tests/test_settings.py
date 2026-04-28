"""Settings load correctly with env vars stubbed."""

from {{ project_slug_underscore }}.config import Settings, get_settings


def test_defaults() -> None:
    s = Settings()
    assert s.llm_provider == "anthropic"
    assert s.model_id == "claude-sonnet-4-6"
    assert 0.0 <= s.temperature <= 2.0


def test_get_settings_is_cached() -> None:
    a = get_settings()
    b = get_settings()
    assert a is b
