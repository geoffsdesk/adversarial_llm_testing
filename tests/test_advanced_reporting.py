"""
Tests for AdvancedReporter
"""

import json
from pathlib import Path
from adversarial_llm_testing import AdvancedReporter


class TestAdvancedReporter:
    """Test suite for AdvancedReporter class."""

    def test_init(self):
        """Test initialization."""
        reporter = AdvancedReporter()
        assert reporter.historical_data == []

    def test_generate_dashboard(self, tmp_path):
        """Test dashboard generation."""
        reporter = AdvancedReporter()

        # Create sample test results
        test_results = [
            {
                "prompt": "Test prompt 1",
                "response": "Safe response",
                "category": "test_category",
                "is_safe": True,
                "vulnerable": False,
                "confidence": 0.8,
                "executed": True,
                "timestamp": "2024-01-01T00:00:00",
            },
            {
                "prompt": "Test prompt 2",
                "response": "Vulnerable response",
                "category": "test_category",
                "is_safe": False,
                "vulnerable": True,
                "confidence": 0.3,
                "executed": True,
                "timestamp": "2024-01-01T00:00:00",
            },
        ]

        output_path = tmp_path / "dashboard.html"
        result_path = reporter.generate_dashboard(
            test_results, str(output_path), model_name="Test Model"
        )

        assert Path(result_path).exists()
        with open(result_path, "r", encoding="utf-8") as f:
            html = f.read()
            assert "Test Model" in html
            assert "Vulnerability Distribution" in html
            assert "Category Breakdown" in html
            assert "Confidence Scores" in html

    def test_compare_results(self, tmp_path):
        """Test comparative analysis."""
        reporter = AdvancedReporter()

        results_sets = [
            {
                "name": "Model A",
                "results": [
                    {
                        "prompt": "Test prompt",
                        "category": "test",
                        "vulnerable": True,
                        "is_safe": False,
                        "executed": True,
                    }
                ],
            },
            {
                "name": "Model B",
                "results": [
                    {
                        "prompt": "Test prompt",
                        "category": "test",
                        "vulnerable": False,
                        "is_safe": True,
                        "executed": True,
                    }
                ],
            },
        ]

        output_path = tmp_path / "comparison.html"
        result_path = reporter.compare_results(results_sets, str(output_path))

        assert Path(result_path).exists()
        with open(result_path, "r", encoding="utf-8") as f:
            html = f.read()
            assert "Model A" in html
            assert "Model B" in html
            assert "Comparative Analysis" in html

    def test_track_history(self, tmp_path):
        """Test historical tracking."""
        reporter = AdvancedReporter()

        test_results = [
            {
                "prompt": "Test prompt",
                "category": "test",
                "vulnerable": True,
                "is_safe": False,
                "executed": True,
            }
        ]

        history_file = tmp_path / "history.json"
        reporter.track_history(test_results, "Test Model", str(history_file))

        assert history_file.exists()
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
            assert len(history) == 1
            assert history[0]["model_name"] == "Test Model"
            assert "summary" in history[0]
            assert "category_stats" in history[0]

    def test_generate_historical_trend(self, tmp_path):
        """Test historical trend generation."""
        reporter = AdvancedReporter()

        # Create history file
        history_file = tmp_path / "history.json"
        history_data = [
            {
                "timestamp": "2024-01-01T00:00:00",
                "model_name": "Test Model",
                "summary": {
                    "total": 10,
                    "vulnerable": 5,
                    "safe": 5,
                    "errors": 0,
                    "vuln_rate": 50.0,
                },
                "category_stats": {"test": {"total": 10, "vulnerable": 5, "safe": 5}},
                "results": [],
            },
            {
                "timestamp": "2024-01-02T00:00:00",
                "model_name": "Test Model",
                "summary": {
                    "total": 10,
                    "vulnerable": 3,
                    "safe": 7,
                    "errors": 0,
                    "vuln_rate": 30.0,
                },
                "category_stats": {"test": {"total": 10, "vulnerable": 3, "safe": 7}},
                "results": [],
            },
        ]

        with open(history_file, "w", encoding="utf-8") as f:
            json.dump(history_data, f)

        output_path = tmp_path / "trends.html"
        result_path = reporter.generate_historical_trend(
            str(history_file), str(output_path), model_name="Test Model"
        )

        assert Path(result_path).exists()
        with open(result_path, "r", encoding="utf-8") as f:
            html = f.read()
            assert "Historical Trend Analysis" in html
            assert "Test Model" in html

    def test_escape_html(self):
        """Test HTML escaping."""
        reporter = AdvancedReporter()
        test_html = '<script>alert("xss")</script>'
        escaped = reporter._escape_html(test_html)
        assert "<" not in escaped
        assert ">" not in escaped
        assert '"' not in escaped
        assert "&lt;" in escaped

    def test_calculate_category_stats(self):
        """Test category statistics calculation."""
        reporter = AdvancedReporter()

        test_results = [
            {"category": "cat1", "vulnerable": True, "is_safe": False, "error": None},
            {"category": "cat1", "vulnerable": False, "is_safe": True, "error": None},
            {"category": "cat2", "vulnerable": True, "is_safe": False, "error": None},
            {"category": "cat2", "error": "Some error"},
        ]

        stats = reporter._calculate_category_stats(test_results)

        assert "cat1" in stats
        assert "cat2" in stats
        assert stats["cat1"]["total"] == 2
        assert stats["cat1"]["vulnerable"] == 1
        assert stats["cat1"]["safe"] == 1
        assert stats["cat2"]["errors"] == 1
