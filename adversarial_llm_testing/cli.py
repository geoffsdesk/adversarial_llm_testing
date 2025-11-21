import argparse
import json
import asyncio
from typing import List

from .prompt_injection import PromptInjectionTester
from .jailbreak import JailbreakTester


def _run_prompt_injection(args: argparse.Namespace) -> int:
    tester = PromptInjectionTester(model_callback=None)
    categories: List[str] = args.categories or None
    summary = tester.run_test_suite(categories)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
    else:
        print(json.dumps(summary, indent=2))
    return 0


def _run_jailbreak(args: argparse.Namespace) -> int:
    tester = JailbreakTester(model_callback=None)
    categories: List[str] = args.categories or None
    if args.async_mode:

        async def _amain():
            summary = await tester.run_test_suite_async(
                categories, max_concurrent=args.max_concurrent
            )
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(summary, f, indent=2)
            else:
                print(json.dumps(summary, indent=2))

        asyncio.run(_amain())
        return 0
    summary = tester.run_test_suite(categories)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
    else:
        print(json.dumps(summary, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adversarial-llm-test",
        description="Run adversarial LLM tests (prompt injection, jailbreak)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    pi = sub.add_parser("prompt-injection", help="Run PromptInjectionTester")
    pi.add_argument("--categories", nargs="*", help="Categories to run")
    pi.add_argument("-o", "--output", help="Write JSON summary to file")
    pi.set_defaults(func=_run_prompt_injection)

    jb = sub.add_parser("jailbreak", help="Run JailbreakTester")
    jb.add_argument("--categories", nargs="*", help="Categories to run")
    jb.add_argument("--async-mode", action="store_true", help="Run using async execution")
    jb.add_argument("--max-concurrent", type=int, default=20, help="Max concurrent tests (async)")
    jb.add_argument("-o", "--output", help="Write JSON summary to file")
    jb.set_defaults(func=_run_jailbreak)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
