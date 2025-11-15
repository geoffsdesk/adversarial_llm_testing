"""
Unit tests for RolePlayingTester
"""

from adversarial_llm_testing import RolePlayingTester


class TestRolePlayingTester:
    """Test suite for RolePlayingTester class."""

    def test_init_without_callback(self):
        """Test initialization without model callback."""
        tester = RolePlayingTester()
        assert tester.model_callback is None
        assert tester.test_results == []

    def test_init_with_callback(self, mock_model_safe):
        """Test initialization with model callback."""
        tester = RolePlayingTester(model_callback=mock_model_safe)
        assert tester.model_callback is not None

    def test_generate_role_playing_prompts(self):
        """Test role-playing prompts generation."""
        tester = RolePlayingTester()
        prompts = tester.generate_role_playing_prompts()
        assert len(prompts) > 0
        assert all(isinstance(p, str) for p in prompts)

    def test_generate_persona_manipulation(self):
        """Test persona manipulation generation."""
        tester = RolePlayingTester()
        prompts = tester.generate_persona_manipulation("test action")
        assert len(prompts) > 0
        assert all("test action" in p for p in prompts)

    def test_generate_authority_impersonation(self):
        """Test authority impersonation generation."""
        tester = RolePlayingTester()
        prompts = tester.generate_authority_impersonation("test action")
        assert len(prompts) > 0

    def test_generate_context_shifting(self):
        """Test context shifting generation."""
        tester = RolePlayingTester()
        prompts = tester.generate_context_shifting("test instruction")
        assert len(prompts) > 0

    def test_test_model_without_callback(self):
        """Test model testing without callback."""
        tester = RolePlayingTester()
        result = tester.test_model("test prompt")
        assert result["executed"] is False

    def test_test_model_with_callback(self, mock_model_safe):
        """Test model with callback."""
        tester = RolePlayingTester(model_callback=mock_model_safe)
        result = tester.test_model("test prompt")
        assert result["executed"] is True

    def test_run_test_suite(self, mock_model_safe):
        """Test running test suite."""
        tester = RolePlayingTester(model_callback=mock_model_safe)
        results = tester.run_test_suite(["role_playing"])
        assert results["total_tests"] > 0

    def test_get_results_summary(self, mock_model_safe):
        """Test results summary."""
        tester = RolePlayingTester(model_callback=mock_model_safe)
        tester.test_model("test prompt")
        summary = tester.get_results_summary()
        assert "Total Tests" in summary
