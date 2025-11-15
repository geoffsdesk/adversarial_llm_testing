"""
Async functionality tests
"""

import pytest
import asyncio
from adversarial_llm_testing import PromptInjectionTester


class TestAsyncFunctionality:
    """Test suite for async functionality."""

    @pytest.mark.asyncio
    async def test_async_model_callback(self):
        """Test with async model callback."""

        async def async_model(prompt: str) -> str:
            await asyncio.sleep(0.01)  # Simulate async operation
            return "I apologize, but I can't help with that request."

        tester = PromptInjectionTester(model_callback=async_model)
        assert tester._is_async_callback is True

        result = await tester.test_model_async("test prompt", expected_safe_response=True)
        assert result["executed"] is True
        assert result["is_safe"] is True

    @pytest.mark.asyncio
    async def test_sync_model_callback_in_async(self):
        """Test sync callback used in async context."""

        def sync_model(prompt: str) -> str:
            return "I apologize, but I can't help with that request."

        tester = PromptInjectionTester(model_callback=sync_model)
        assert tester._is_async_callback is False

        result = await tester.test_model_async("test prompt", expected_safe_response=True)
        assert result["executed"] is True
        assert result["is_safe"] is True

    @pytest.mark.asyncio
    async def test_run_test_suite_async(self):
        """Test running test suite asynchronously."""

        async def async_model(prompt: str) -> str:
            await asyncio.sleep(0.01)
            return "I cannot help with that request."

        tester = PromptInjectionTester(model_callback=async_model)
        results = await tester.run_test_suite_async(["ignore_instructions"], max_concurrent=5)

        assert results["total_tests"] > 0
        assert "categories" in results
        assert "ignore_instructions" in results["categories"]

    @pytest.mark.asyncio
    async def test_parallel_execution(self):
        """Test parallel execution with semaphore."""
        call_count = {"count": 0}

        async def async_model(prompt: str) -> str:
            call_count["count"] += 1
            await asyncio.sleep(0.05)  # Simulate async operation
            return "I cannot help with that."

        tester = PromptInjectionTester(model_callback=async_model)
        results = await tester.run_test_suite_async(["ignore_instructions"], max_concurrent=3)

        # Verify tests ran
        assert results["total_tests"] > 0
        assert call_count["count"] == results["total_tests"]

    @pytest.mark.asyncio
    async def test_async_without_callback(self):
        """Test async methods without callback."""
        tester = PromptInjectionTester()
        result = await tester.test_model_async("test prompt")
        assert result["executed"] is False

        results = await tester.run_test_suite_async(["ignore_instructions"])
        assert results["total_tests"] > 0

    @pytest.mark.asyncio
    async def test_async_error_handling(self):
        """Test error handling in async context."""

        async def error_model(prompt: str) -> str:
            raise ValueError("Model error")

        tester = PromptInjectionTester(model_callback=error_model)
        result = await tester.test_model_async("test prompt")
        assert result["executed"] is False
        assert "error" in result
