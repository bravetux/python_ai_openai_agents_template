"""OpenAI Agents SDK researcher."""

from agents import Agent

from {{ project_slug_underscore }}.config.llm_client import build_llm
from {{ project_slug_underscore }}.config.prompts import RESEARCHER_PROMPT
from {{ project_slug_underscore }}.tools.example_tools import TOOLS


def build_researcher() -> Agent:
    return Agent(
        name="researcher",
        instructions=RESEARCHER_PROMPT,
        model=build_llm(),
        tools=TOOLS,
    )
