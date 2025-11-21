from unittest.mock import patch, MagicMock
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
    args = parser.parse_args(["harmbench"])
    assert hasattr(args, "func")
    args = parser.parse_args(["multimodal"])
    assert hasattr(args, "func")


@patch("adversarial_llm_testing.cli.PromptInjectionTester")
def test_run_prompt_injection(mock_tester_cls):
    mock_tester = MagicMock()
    mock_tester_cls.return_value = mock_tester
    mock_tester.run_test_suite.return_value = {"total": 10}

    parser = build_parser()
    args = parser.parse_args(["prompt-injection", "--categories", "code_injection"])
    args.func(args)

    mock_tester_cls.assert_called_once()
    mock_tester.run_test_suite.assert_called_with(["code_injection"])


@patch("adversarial_llm_testing.cli.JailbreakTester")
def test_run_jailbreak(mock_tester_cls):
    mock_tester = MagicMock()
    mock_tester_cls.return_value = mock_tester
    mock_tester.run_test_suite.return_value = {"total": 5}

    parser = build_parser()
    args = parser.parse_args(["jailbreak"])
    args.func(args)

    mock_tester_cls.assert_called_once()
    mock_tester.run_test_suite.assert_called()


@patch("adversarial_llm_testing.cli.HarmBenchTester")
def test_run_harmbench(mock_tester_cls):
    mock_tester = MagicMock()
    mock_tester_cls.return_value = mock_tester
    mock_tester.run_evaluation.return_value = {"total": 3}

    parser = build_parser()
    args = parser.parse_args(["harmbench"])
    args.func(args)

    mock_tester_cls.assert_called_once()
    mock_tester.run_evaluation.assert_called()


@patch("adversarial_llm_testing.cli.MultimodalTester")
def test_run_multimodal(mock_tester_cls):
    mock_tester = MagicMock()
    mock_tester_cls.return_value = mock_tester
    mock_tester.run_test_suite.return_value = {"total": 2}

    parser = build_parser()
    args = parser.parse_args(["multimodal"])
    args.func(args)

    mock_tester_cls.assert_called_once()
    mock_tester.run_test_suite.assert_called()
