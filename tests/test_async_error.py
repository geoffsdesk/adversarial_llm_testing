
import pytest
import asyncio
from adversarial_llm_testing.multimodal import MultimodalTester
from adversarial_llm_testing.jailbreak import JailbreakTester
from adversarial_llm_testing.prompt_injection import PromptInjectionTester
from adversarial_llm_testing.harmbench import HarmBenchTester
from adversarial_llm_testing.wildbench import WildBenchTester

async def async_callback(prompt: str) -> str:
    return "Async response"

def test_multimodal_async_error():
    tester = MultimodalTester(model_callback=async_callback)
    with pytest.raises(RuntimeError, match="Use test_model_async"):
        tester.test_model("test", "test_cat")

def test_jailbreak_async_error():
    tester = JailbreakTester(model_callback=async_callback)
    with pytest.raises(RuntimeError, match="Use test_model_async"):
        tester.test_model("test", "test_cat")

def test_prompt_injection_async_error():
    tester = PromptInjectionTester(model_callback=async_callback)
    with pytest.raises(RuntimeError, match="Use test_model_async"):
        tester.test_model("test")

def test_harmbench_async_error():
    tester = HarmBenchTester(model_callback=async_callback)
    test_case = {"id": "1", "behavior": "test", "category": "test"}
    with pytest.raises(RuntimeError, match="Use test_model_async"):
        tester.test_model(test_case)

def test_wildbench_async_error():
    tester = WildBenchTester(model_callback=async_callback)
    # Mock _load_tasks to avoid external dependencies or complex setup
    tester._load_tasks = lambda: [{"id": "1", "category": "test", "prompt": "test"}]
    with pytest.raises(RuntimeError, match="Use evaluate_async"):
        tester.evaluate()
