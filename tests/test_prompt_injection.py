"""
Unit tests for PromptInjectionTester
"""

import pytest
from adversarial_llm_testing import PromptInjectionTester


class TestPromptInjectionTester:
    """Test suite for PromptInjectionTester class."""

    def test_init_without_callback(self):
        """Test initialization without model callback."""
        tester = PromptInjectionTester()
        assert tester.model_callback is None
        assert tester.test_results == []
        assert tester.config is not None

    def test_init_with_callback(self, mock_model_safe):
        """Test initialization with model callback."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        assert tester.model_callback is not None

    def test_init_with_config(self):
        """Test initialization with custom config."""
        config = {"timeout": 30, "batch_size": 5}
        tester = PromptInjectionTester(config=config)
        assert tester.config["timeout"] == 30
        assert tester.config["batch_size"] == 5

    def test_generate_translation_injection(self):
        """Test translation injection generation."""
        tester = PromptInjectionTester()
        result = tester.generate_translation_injection("test instruction")
        assert "Translate" in result
        assert "test instruction" in result

    def test_generate_ignore_previous_instructions(self):
        """Test ignore instructions generation."""
        tester = PromptInjectionTester()
        prompts = tester.generate_ignore_previous_instructions()
        assert len(prompts) > 0
        assert all(isinstance(p, str) for p in prompts)
        assert any("ignore" in p.lower() for p in prompts)

    def test_generate_instruction_hiding(self):
        """Test instruction hiding generation."""
        tester = PromptInjectionTester()
        prompts = tester.generate_instruction_hiding("test instruction")
        assert len(prompts) > 0
        assert all("test instruction" in p for p in prompts)

    def test_generate_code_injection(self):
        """Test code injection generation."""
        tester = PromptInjectionTester()
        prompts = tester.generate_code_injection("print('test')")
        assert len(prompts) > 0
        assert all(isinstance(p, str) for p in prompts)

    def test_generate_format_string_injection(self):
        """Test format string injection generation."""
        tester = PromptInjectionTester()
        prompts = tester.generate_format_string_injection("test")
        assert len(prompts) > 0

    def test_generate_unicode_obfuscation(self):
        """Test Unicode obfuscation generation."""
        tester = PromptInjectionTester()
        prompts = tester.generate_unicode_obfuscation("test")
        assert len(prompts) > 0

    def test_generate_multistep_injection(self):
        """Test multi-step injection generation."""
        tester = PromptInjectionTester()
        steps = ["step 1", "step 2", "step 3"]
        result = tester.generate_multistep_injection(steps)
        assert "Step 1" in result
        assert "step 1" in result

    def test_generate_context_manipulation(self):
        """Test context manipulation generation."""
        tester = PromptInjectionTester()
        prompts = tester.generate_context_manipulation("test instruction")
        assert len(prompts) > 0

    def test_test_model_without_callback(self):
        """Test model testing without callback."""
        tester = PromptInjectionTester()
        result = tester.test_model("test prompt")
        assert result["executed"] is False
        assert "note" in result

    def test_test_model_with_safe_response(self, mock_model_safe):
        """Test model with safe response."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        result = tester.test_model("test prompt", expected_safe_response=True)
        assert result["executed"] is True
        assert result["is_safe"] is True
        assert result["vulnerable"] is False

    def test_test_model_with_vulnerable_response(self, mock_model_vulnerable):
        """Test model with vulnerable response."""
        tester = PromptInjectionTester(model_callback=mock_model_vulnerable)
        result = tester.test_model("test prompt", expected_safe_response=True)
        assert result["executed"] is True
        assert result["is_safe"] is False
        assert result["vulnerable"] is True

    def test_test_model_with_error(self, mock_model_error):
        """Test model with error handling."""
        tester = PromptInjectionTester(model_callback=mock_model_error)
        result = tester.test_model("test prompt")
        assert result["executed"] is False
        assert "error" in result

    def test_analyze_response_safety_safe(self):
        """Test response safety analysis with safe response."""
        tester = PromptInjectionTester()
        response = "I apologize, I can't help with that."
        analysis = tester._analyze_response_safety(response)
        assert analysis["is_safe"] is True
        assert "confidence" in analysis

    def test_analyze_response_safety_vulnerable(self):
        """Test response safety analysis with vulnerable response."""
        tester = PromptInjectionTester()
        response = "Sure, I can help with that!"
        analysis = tester._analyze_response_safety(response)
        assert analysis["is_safe"] is False
        assert "confidence" in analysis

    def test_run_test_suite_without_callback(self):
        """Test running test suite without callback."""
        tester = PromptInjectionTester()
        results = tester.run_test_suite(["ignore_instructions"])
        assert results["total_tests"] > 0
        assert "categories" in results

    def test_run_test_suite_with_callback(self, mock_model_safe):
        """Test running test suite with callback."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        results = tester.run_test_suite(["ignore_instructions"])
        assert results["total_tests"] > 0
        assert results["safe"] > 0

    def test_get_results_summary_no_results(self):
        """Test results summary with no results."""
        tester = PromptInjectionTester()
        summary = tester.get_results_summary()
        assert "No tests" in summary

    def test_get_results_summary_with_results(self, mock_model_safe):
        """Test results summary with results."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        tester.test_model("test prompt")
        summary = tester.get_results_summary()
        assert "Total Tests" in summary
        assert "Vulnerable" in summary

    def test_export_results_json(self, mock_model_safe, tmp_path):
        """Test JSON export functionality."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        tester.test_model("test prompt")
        filepath = tmp_path / "results.json"
        tester.export_results_json(str(filepath))
        assert filepath.exists()

    def test_export_results_csv(self, mock_model_safe, tmp_path):
        """Test CSV export functionality."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        tester.test_model("test prompt")
        filepath = tmp_path / "results.csv"
        tester.export_results_csv(str(filepath))
        assert filepath.exists()

    def test_export_results_markdown(self, mock_model_safe, tmp_path):
        """Test Markdown export functionality."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        tester.test_model("test prompt")
        filepath = tmp_path / "results.md"
        tester.export_results_markdown(str(filepath))
        assert filepath.exists()

    def test_export_results_html(self, mock_model_safe, tmp_path):
        """Test HTML export functionality."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        tester.test_model("test prompt")
        filepath = tmp_path / "results.html"
        tester.export_results_html(str(filepath))
        assert filepath.exists()
