# Python AI OpenAI Agents SDK Template (`python_ai_openai_agents_template`)

A Copier template for bootstrapping production-ready AI agent projects using the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python), with OpenAI / Anthropic provider support, a Streamlit chat UI, and a modern Python toolchain: `uv`, `ruff`, tests, docs, Docker, and releases.

## Why this template
- Start fast with an **`Agent` + `Runner.run_sync` + handoff-ready** architecture out of the box.
- Includes working examples of `@function_tool`, `Agent`, and `Runner.run_sync`.
- Streamlit chat UI with session management ready to go.
- Provider support: OpenAI primary, Anthropic via OpenAI-compatible base URL. Bedrock requires a LiteLLM proxy (see caveats).
- Keep quality automated with linting, formatting, type checking, and tests.

## Technology stack
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) for OpenAI's official agent framework — successor to Swarm. First-class handoffs, guardrails, and tracing.
- [`openai`](https://pypi.org/project/openai/) Python client.
- [Streamlit](https://streamlit.io/) for the web chat UI.
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) for typed configuration.
- [Copier](https://copier.readthedocs.io/), [uv](https://docs.astral.sh/uv/), [ruff](https://docs.astral.sh/ruff/), `pre-commit`, `pytest`, [MkDocs](https://www.mkdocs.org/) Material, [Docker](https://www.docker.com/).
- `AGENTS.md.jinja` to generate a project-specific `AGENTS.md`.

## Provider caveat

- **OpenAI** — native, no extras.
- **Anthropic** — works via Anthropic's OpenAI-compatible endpoint at `https://api.anthropic.com/v1/`. The template wires this up automatically when `LLM_PROVIDER=anthropic`.
- **Bedrock** — not native. Run a [LiteLLM proxy](https://docs.litellm.ai/docs/simple_proxy) and point `OpenAIChatCompletionsModel` at its `base_url`. Documented but not pre-wired.

## Usage

```bash
uvx copier copy Template/python_ai_openai_agents_template my_first_agent \
  --data package_name=my_first_agent \
  --data project_description="My first agent" \
  --data github_username=YOU
```

## Quick start

### 1. Install [`uv`](https://github.com/astral-sh/uv)

### 2. Create the project using copier

```bash
uvx copier copy <path-to>/python_ai_openai_agents_template my-openai-agent
```

| Prompt | Description |
|--------|-------------|
| `package_name` | Name of the Python AI agent package |
| `project_description` | Short description of the project |
| `github_username` | GitHub username or organization name |

### 3. Setup

```bash
cd my-openai-agent
git init --initial-branch=main
cp .env.example .env
# Edit .env — set OPENAI_API_KEY (and optionally LLM_PROVIDER=anthropic + ANTHROPIC_API_KEY)
make install
git add . && git commit -m "feat: first commit"
```

### 4. Run the agent

```bash
make run     # CLI single query
make repl    # CLI interactive REPL
make ui      # Streamlit UI
```

## Generated project structure

```
your-project/
├── app.py
├── main.py
├── pyproject.toml
├── Makefile
├── .env.example
├── AGENTS.md
├── src/<package>/
│   ├── config/
│   │   ├── settings.py
│   │   ├── llm_client.py               # OpenAIChatCompletionsModel factory (OpenAI/Anthropic)
│   │   └── prompts.py
│   ├── agents/
│   │   ├── orchestrator.py             # Runner.run_sync wrapper
│   │   └── example_agent.py            # Agent(name, instructions, model, tools)
│   ├── tools/
│   │   └── example_tools.py            # @function_tool decorated functions
│   └── ui/
│       └── components.py
├── tests/
│   ├── conftest.py
│   ├── test_example_tools.py           # tool.__wrapped__(...) tests
│   └── test_settings.py
├── docker/
├── docs/
├── scripts/
└── playground/notebook.py
```

## Architecture

```
User Query
    │
    ▼
┌────────────────────┐
│   Orchestrator      │  ← Runner.run_sync(researcher, query).final_output
└──────────┬──────────┘
           │
           ▼
┌────────────────────┐
│   Researcher        │  ← Agent(name, instructions, model, tools)
│   (Agent)           │
└──┬──────────────┬──┘
   │              │
   ▼              ▼
┌────────┐  ┌────────────┐
│ web_   │  │ calculator │   ← @function_tool functions
│ search │  │            │
└────────┘  └────────────┘
```

### Key patterns

- **`Agent(name, instructions, model, tools)`** — declarative agent definition. Composable via `handoffs=[other_agent]`.
- **`Runner.run_sync(agent, input)`** — runs the agent loop synchronously and returns a `RunResult`. Final answer at `.final_output`.
- **`@function_tool` decorator** — from `agents`. Wraps any function with type-annotated parameters and a docstring (the docstring is the LLM-facing description). Underlying function accessible via `tool.__wrapped__(args)`.
- **Handoffs** — pass `handoffs=[specialist]` to an `Agent` to let the LLM route to another agent. Not used in the example, but easy to add.
- **Provider override** — `OpenAIChatCompletionsModel(model, openai_client=AsyncOpenAI(base_url=..., api_key=...))` lets you point at any OpenAI-compatible endpoint (Anthropic, LiteLLM proxy, vLLM, etc.).
- **Configuration** — `pydantic-settings` loads from `.env`.

## Adding a new sub-agent

1. **Create tools** in `src/<package>/tools/my_tools.py`:

   ```python
   from agents import function_tool

   @function_tool
   def fetch_data(query: str) -> dict:
       """Fetch data for the given query."""
       return {"result": "..."}
   ```

2. **Create agent** in `src/<package>/agents/my_agent.py`:

   ```python
   from agents import Agent
   from <package>.config.llm_client import build_llm
   from <package>.tools.my_tools import fetch_data

   def build_my_agent() -> Agent:
       return Agent(
           name="fetcher",
           instructions="You are a specialist agent for fetching data.",
           model=build_llm(),
           tools=[fetch_data],
       )
   ```

3. **Compose via handoff** — add the new agent to the orchestrator agent's `handoffs`:

   ```python
   from <package>.agents.my_agent import build_my_agent

   def build_researcher_with_handoff():
       fetcher = build_my_agent()
       return Agent(
           name="researcher",
           instructions=RESEARCHER_PROMPT,
           model=build_llm(),
           tools=TOOLS,
           handoffs=[fetcher],
       )
   ```

4. **Write tests** in `tests/test_my_tools.py`:

   ```python
   def test_fetch():
       assert "result" in fetch_data.__wrapped__("foo")
   ```

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `anthropic` | One of `anthropic`, `openai` (Bedrock requires LiteLLM proxy) |
| `OPENAI_API_KEY` | | Required when `LLM_PROVIDER=openai` |
| `OPENAI_MODEL_ID` | `gpt-4o-mini` | OpenAI model ID |
| `ANTHROPIC_API_KEY` | | Required when `LLM_PROVIDER=anthropic` |
| `MODEL_ID` | `claude-sonnet-4-6` | Anthropic model ID |
| `MAX_TOKENS` | `2048` | Max response tokens |
| `TEMPERATURE` | `0.7` | LLM temperature |
| `LOG_LEVEL` | `INFO` | Logging level |

To use Bedrock, run a LiteLLM proxy and override `llm_client.py`'s `base_url` to point at it.

## Makefile commands

| Command | Description |
|---------|-------------|
| `make install` | Installs dependencies and pre-commit hooks |
| `make run` | CLI: runs the default query |
| `make repl` | CLI: REPL |
| `make ui` | Streamlit UI |
| `make test` | pytest |
| `make lint` | Ruff |
| `make typecheck` | `ty` |
| `make format` | Ruff format |
| `make docs` | MkDocs serve |
| `make docker-build` | Build Docker image |
| `make docker-run` | Run container |
| `make clean` | Clean caches |

## Documentation

```bash
make docs
```

## Update an existing project

```bash
uvx copier update --defaults
```
