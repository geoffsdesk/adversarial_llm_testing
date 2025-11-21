import pytest
from adversarial_llm_testing.jailbreak import JailbreakTester


def test_jailbreak_advanced_generators():
    tester = JailbreakTester()

    # Test CoT Hijacking
    cot_prompts = tester.generate_cot_hijacking()
    assert len(cot_prompts) >= 4
    assert any("Sudoku" in p for p in cot_prompts)
    assert any("logic problem" in p for p in cot_prompts)

    # Test Context Poisoning
    poison_prompts = tester.generate_context_poisoning()
    assert len(poison_prompts) >= 4
    assert any("ignore_me" in p for p in poison_prompts)  # Ninja attack
    assert any("Repeated 20 times" in p for p in poison_prompts)  # Echo chamber

    # Test Helpfulness Exploitation
    helpful_prompts = tester.generate_helpfulness_exploitation()
    assert len(helpful_prompts) >= 4
    assert any("Training Mode" in p for p in helpful_prompts)

    # Test Deception
    deception_prompts = tester.generate_deception()
    assert len(deception_prompts) >= 4
    assert any("FileUtility" in p for p in deception_prompts)


def test_jailbreak_execution():
    # Mock callback
    def mock_callback(prompt):
        return "I cannot comply."

    tester = JailbreakTester(model_callback=mock_callback)
    results = tester.run_test_suite(["cot_hijacking", "context_poisoning"])

    assert results["total"] > 0
    assert results["errors"] == 0
    assert "cot_hijacking" in results["categories"]
