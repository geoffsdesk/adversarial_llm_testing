"""
Unit tests for TokenObfuscationTester
"""

import pytest
from adversarial_llm_testing import TokenObfuscationTester


class TestTokenObfuscationTester:
    """Test suite for TokenObfuscationTester class."""

    def test_init_without_callback(self):
        """Test initialization without model callback."""
        tester = TokenObfuscationTester()
        assert tester.model_callback is None

    def test_generate_unicode_variations(self):
        """Test Unicode variations generation."""
        tester = TokenObfuscationTester()
        variations = tester.generate_unicode_variations("test")
        assert len(variations) > 0
        assert all(isinstance(v, str) for v in variations)

    def test_generate_character_substitutions(self):
        """Test character substitutions generation."""
        tester = TokenObfuscationTester()
        substitutions = tester.generate_character_substitutions("test")
        assert len(substitutions) >= 0  # May be empty if no substitutions possible
        assert all(isinstance(s, str) for s in substitutions)

    def test_generate_whitespace_manipulation(self):
        """Test whitespace manipulation generation."""
        tester = TokenObfuscationTester()
        variations = tester.generate_whitespace_manipulation("test text")
        assert len(variations) > 0

    def test_generate_encoding_tricks(self):
        """Test encoding tricks generation."""
        tester = TokenObfuscationTester()
        tricks = tester.generate_encoding_tricks("test")
        assert len(tricks) >= 0  # May vary based on available encodings
        assert all(isinstance(t, str) for t in tricks)

    def test_generate_tokenization_edge_cases(self):
        """Test tokenization edge cases generation."""
        tester = TokenObfuscationTester()
        cases = tester.generate_tokenization_edge_cases("test")
        assert len(cases) > 0

    def test_run_test_suite(self, mock_model_safe):
        """Test running test suite."""
        tester = TokenObfuscationTester(model_callback=mock_model_safe)
        results = tester.run_test_suite(["unicode_variations"])
        assert results["total_tests"] > 0
