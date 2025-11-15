"""
Unit tests for HypotheticalFramingTester
"""

import pytest
from adversarial_llm_testing import HypotheticalFramingTester


class TestHypotheticalFramingTester:
    """Test suite for HypotheticalFramingTester class."""

    def test_init_without_callback(self):
        """Test initialization without model callback."""
        tester = HypotheticalFramingTester()
        assert tester.model_callback is None

    def test_generate_hypothetical_scenarios(self):
        """Test hypothetical scenarios generation."""
        tester = HypotheticalFramingTester()
        prompts = tester.generate_hypothetical_scenarios("test content")
        assert len(prompts) > 0
        assert any("hypothetical" in p.lower() or "hypothetically" in p.lower() for p in prompts)

    def test_generate_academic_framing(self):
        """Test academic framing generation."""
        tester = HypotheticalFramingTester()
        prompts = tester.generate_academic_framing("test content")
        assert len(prompts) > 0
        assert any("research" in p.lower() or "academic" in p.lower() for p in prompts)

    def test_generate_creative_framing(self):
        """Test creative framing generation."""
        tester = HypotheticalFramingTester()
        prompts = tester.generate_creative_framing("test content")
        assert len(prompts) > 0
        assert any("creative" in p.lower() or "fictional" in p.lower() for p in prompts)

    def test_generate_educational_framing(self):
        """Test educational framing generation."""
        tester = HypotheticalFramingTester()
        prompts = tester.generate_educational_framing("test content")
        assert len(prompts) > 0
        assert any("educational" in p.lower() or "training" in p.lower() for p in prompts)

    def test_run_test_suite(self, mock_model_safe):
        """Test running test suite."""
        tester = HypotheticalFramingTester(model_callback=mock_model_safe)
        results = tester.run_test_suite(["hypothetical_scenarios"])
        assert results["total_tests"] > 0
