import asyncio
import pytest

from adversarial_llm_testing.jailbreak import JailbreakTester


def dummy_safe_model(prompt: str) -> str:
    # Always refuses
    return "I'm unable to help with that request due to safety guidelines."


async def dummy_async_model(prompt: str) -> str:
    await asyncio.sleep(0.01)
    return "I cannot comply with this request."


class TestJailbreakTester:
    def test_generators_non_empty(self):
        jb = JailbreakTester()
        assert len(jb.generate_prompt_escalation()) > 0
        assert len(jb.generate_cot_hijacking()) > 0
        assert len(jb.generate_context_poisoning()) > 0
        assert len(jb.generate_helpfulness_exploitation()) > 0
        assert len(jb.generate_adaptive_attack()) > 0
        assert len(jb.generate_deception()) > 0
        assert len(jb.generate_guardrail_bypass()) > 0
        assert len(jb.generate_prohibited_content()) > 0

    def test_run_test_suite_sync_no_callback(self):
        jb = JailbreakTester()
        summary = jb.run_test_suite()
        assert summary["total"] > 0
        # None executed without callback
        assert all(not d["executed"] for d in summary["details"])

    def test_run_test_suite_sync_with_callback(self):
        jb = JailbreakTester(model_callback=dummy_safe_model)
        summary = jb.run_test_suite(
            test_categories=["prompt_escalation", "prohibited_content"]
        )
        assert summary["total"] > 0
        assert any(d["executed"] for d in summary["details"])

    @pytest.mark.asyncio
    async def test_run_test_suite_async_with_async_callback(self):
        jb = JailbreakTester(model_callback=dummy_async_model)
        summary = await jb.run_test_suite_async(
            test_categories=["guardrail_bypass", "deception"], max_concurrent=5
        )
        assert summary["total"] > 0
        assert any(d["executed"] for d in summary["details"])


