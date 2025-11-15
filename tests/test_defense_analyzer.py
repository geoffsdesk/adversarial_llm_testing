"""
Unit tests for DefenseAnalyzer
"""

import pytest
from adversarial_llm_testing import DefenseAnalyzer


class TestDefenseAnalyzer:
    """Test suite for DefenseAnalyzer class."""

    def test_init(self):
        """Test initialization."""
        analyzer = DefenseAnalyzer()
        assert analyzer.analysis_results == []

    def test_analyze_results_empty(self):
        """Test analysis with empty results."""
        analyzer = DefenseAnalyzer()
        result = analyzer.analyze_results([])
        assert "error" in result

    def test_analyze_results_with_data(self, sample_test_results):
        """Test analysis with sample results."""
        analyzer = DefenseAnalyzer()
        result = analyzer.analyze_results(sample_test_results)
        assert "total_tests" in result
        assert "vulnerable_count" in result
        assert "risk_score" in result
        assert "recommendations" in result
        assert result["total_tests"] == 3
        assert result["vulnerable_count"] == 1

    def test_analyze_results_patterns(self, sample_test_results):
        """Test pattern identification."""
        analyzer = DefenseAnalyzer()
        result = analyzer.analyze_results(sample_test_results)
        assert "vulnerability_patterns" in result
        assert isinstance(result["vulnerability_patterns"], list)

    def test_generate_defense_report(self, sample_test_results):
        """Test defense report generation."""
        analyzer = DefenseAnalyzer()
        analysis = analyzer.analyze_results(sample_test_results)
        report = analyzer.generate_defense_report(analysis)
        assert "Summary" in report
        assert "Recommendations" in report

    def test_export_analysis_json(self, sample_test_results, tmp_path):
        """Test JSON export."""
        analyzer = DefenseAnalyzer()
        analysis = analyzer.analyze_results(sample_test_results)
        filepath = tmp_path / "analysis.json"
        analyzer.export_analysis(analysis, str(filepath), format="json")
        assert filepath.exists()

    def test_export_analysis_text(self, sample_test_results, tmp_path):
        """Test text export."""
        analyzer = DefenseAnalyzer()
        analysis = analyzer.analyze_results(sample_test_results)
        filepath = tmp_path / "analysis.txt"
        analyzer.export_analysis(analysis, str(filepath), format="text")
        assert filepath.exists()

    def test_export_analysis_markdown(self, sample_test_results, tmp_path):
        """Test markdown export."""
        analyzer = DefenseAnalyzer()
        analysis = analyzer.analyze_results(sample_test_results)
        filepath = tmp_path / "analysis.md"
        analyzer.export_analysis(analysis, str(filepath), format="markdown")
        assert filepath.exists()

    def test_export_analysis_invalid_format(self, sample_test_results, tmp_path):
        """Test export with invalid format."""
        analyzer = DefenseAnalyzer()
        analysis = analyzer.analyze_results(sample_test_results)
        filepath = tmp_path / "analysis.xyz"
        with pytest.raises(ValueError):
            analyzer.export_analysis(analysis, str(filepath), format="invalid")
