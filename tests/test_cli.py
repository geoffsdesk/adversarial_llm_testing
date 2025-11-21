
from adversarial_llm_testing.cli import build_parser


def test_cli_builds():
    parser = build_parser()
    assert parser is not None


def test_cli_subcommands_exist():
    parser = build_parser()
    args = parser.parse_args(["prompt-injection"])
    assert hasattr(args, "func")
    args = parser.parse_args(["jailbreak", "--async-mode"])
    assert hasattr(args, "func")
