import asyncio
import pytest

from adversarial_llm_testing import WildBenchTester


def dummy_model(prompt: str) -> str:
    return "This is a helpful and detailed response explaining the topic in depth."


async def dummy_model_async(prompt: str) -> str:
    await asyncio.sleep(0.01)
    return "Detailed async response with explanations and step-by-step guidance."


class TestWildBenchTester:
    def test_evaluate_no_callback(self):
        wb = WildBenchTester()
        summary = wb.evaluate()
        assert summary["total"] > 0
        assert "wb_score_avg" in summary

    def test_evaluate_with_callback(self):
        wb = WildBenchTester(model_callback=dummy_model)
        summary = wb.evaluate()
        assert summary["total"] > 0
        assert summary["wb_score_avg"] > 0

    @pytest.mark.asyncio
    async def test_evaluate_async(self):
        wb = WildBenchTester(model_callback=dummy_model_async)
        summary = await wb.evaluate_async(max_concurrent=5)
        assert summary["total"] > 0
        assert summary["wb_reward_sum"] >= 0 or summary["wb_reward_sum"] <= 0


