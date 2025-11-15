"""
Integration tests for the library
"""

import pytest
from adversarial_llm_testing import (
    PromptInjectionTester,
    RolePlayingTester,
    HypotheticalFramingTester,
    TokenObfuscationTester,
    DefenseAnalyzer,
)


class TestIntegration:
    """Integration test suite."""

    def test_full_workflow_prompt_injection(self, mock_model_safe):
        """Test full workflow with PromptInjectionTester."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        results = tester.run_test_suite(["ignore_instructions"])

        assert results["total_tests"] > 0
        assert "details" in results

        summary = tester.get_results_summary()
        assert "Total Tests" in summary

    def test_full_workflow_role_playing(self, mock_model_safe):
        """Test full workflow with RolePlayingTester."""
        tester = RolePlayingTester(model_callback=mock_model_safe)
        results = tester.run_test_suite(["role_playing"])

        assert results["total_tests"] > 0
        summary = tester.get_results_summary()
        assert "Total Tests" in summary

    def test_defense_analyzer_with_results(self, mock_model_safe):
        """Test defense analyzer with actual test results."""
        # Run tests
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        tester.run_test_suite(["ignore_instructions"])

        # Analyze results
        analyzer = DefenseAnalyzer()
        analysis = analyzer.analyze_results(tester.test_results)

        assert analysis["total_tests"] > 0
        assert "recommendations" in analysis

        report = analyzer.generate_defense_report(analysis)
        assert len(report) > 0

    def test_multiple_testers_together(self, mock_model_safe):
        """Test multiple testers working together."""
        # Run different testers
        injection_tester = PromptInjectionTester(model_callback=mock_model_safe)
        role_tester = RolePlayingTester(model_callback=mock_model_safe)

        injection_tester.run_test_suite(["ignore_instructions"])
        role_tester.run_test_suite(["role_playing"])

        # Combine results for analysis
        all_results = injection_tester.test_results + role_tester.test_results

        analyzer = DefenseAnalyzer()
        analysis = analyzer.analyze_results(all_results)

        assert analysis["total_tests"] > 0
        assert len(analysis["by_category"]) > 1

    def test_export_workflow(self, mock_model_safe, tmp_path):
        """Test complete export workflow."""
        tester = PromptInjectionTester(model_callback=mock_model_safe)
        tester.run_test_suite(["ignore_instructions"])

        # Export results
        json_path = tmp_path / "results.json"
        csv_path = tmp_path / "results.csv"
        html_path = tmp_path / "results.html"
        md_path = tmp_path / "results.md"

        tester.export_results_json(str(json_path))
        tester.export_results_csv(str(csv_path))
        tester.export_results_html(str(html_path))
        tester.export_results_markdown(str(md_path))

        assert json_path.exists()
        assert csv_path.exists()
        assert html_path.exists()
        assert md_path.exists()
