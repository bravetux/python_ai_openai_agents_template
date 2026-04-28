"""CLI entry point. Delegates to main.py at the project root for convenience."""

import argparse
import asyncio


def cli() -> None:
    parser = argparse.ArgumentParser(description="Run the agent.")
    parser.add_argument("query", nargs="?", default=None, help="A single query to run.")
    parser.add_argument("--repl", action="store_true", help="Start an interactive REPL.")
    args = parser.parse_args()

    # Late import so framework deps load only when invoked.
    from {{ project_slug_underscore }}.agents.orchestrator import build_orchestrator

    orchestrator = build_orchestrator()

    if args.repl:
        _run_repl(orchestrator)
        return

    query = args.query or "Search for the latest population of Tokyo and divide it by 1000."
    answer = _run_once(orchestrator, query)
    print(answer)


def _run_once(orchestrator, query: str) -> str:
    result = orchestrator(query)
    if asyncio.iscoroutine(result):
        result = asyncio.run(result)
    return str(result)


def _run_repl(orchestrator) -> None:
    print("Agent REPL. Ctrl-D or 'exit' to quit.")
    while True:
        try:
            q = input("> ").strip()
        except EOFError:
            return
        if q in {"exit", "quit"}:
            return
        if not q:
            continue
        print(_run_once(orchestrator, q))


if __name__ == "__main__":
    cli()
