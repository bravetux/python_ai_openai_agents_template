"""OpenAI Agents SDK model factory.

Anthropic/Bedrock are reachable via OpenAI-compatible endpoints (e.g., LiteLLM proxy)
or via the agents SDK's model providers; we wire OpenAI directly and document
the LiteLLM swap in the README for non-OpenAI providers.
"""

from agents import Model
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

from {{ project_slug_underscore }}.config import get_settings


def build_llm() -> Model:
    s = get_settings()
    if s.llm_provider == "openai":
        return OpenAIChatCompletionsModel(
            model=s.openai_model_id,
            openai_client=AsyncOpenAI(api_key=s.openai_api_key),
        )
    if s.llm_provider == "anthropic":
        return OpenAIChatCompletionsModel(
            model=s.model_id,
            openai_client=AsyncOpenAI(
                api_key=s.anthropic_api_key,
                base_url="https://api.anthropic.com/v1/",
            ),
        )
    raise ValueError(
        "OpenAI Agents SDK template: provider 'bedrock' requires a LiteLLM proxy. "
        "See README."
    )
