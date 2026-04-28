"""OpenAI Agents SDK tool tests. function_tool wraps; underlying fn at .__wrapped__."""

from {{ project_slug_underscore }}.tools.example_tools import calculator, web_search


def test_web_search_returns_three_mock_results() -> None:
    assert len(web_search.__wrapped__("Tokyo")) == 3


def test_calculator_basic_arithmetic() -> None:
    assert calculator.__wrapped__("13960000 / 1000") == "13960.0"


def test_calculator_rejects_unsafe_expression() -> None:
    import pytest
    with pytest.raises(Exception):
        calculator.__wrapped__("__import__('os').system('echo pwned')")
