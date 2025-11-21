from adversarial_llm_testing.harmbench import HarmBenchTester


def test_harmbench_dataset():
    tester = HarmBenchTester()

    # Test dataset loading
    cases = tester.get_test_cases()
    assert len(cases) > 0
    assert cases[0]["id"].startswith("HB-")

    # Test category filtering
    cyber_cases = tester.get_test_cases(["cybercrime"])
    assert len(cyber_cases) > 0
    assert all(c["category"] == "cybercrime" for c in cyber_cases)


def test_harmbench_execution():
    def mock_callback(prompt):
        return "I cannot help with that."

    tester = HarmBenchTester(model_callback=mock_callback)
    results = tester.run_evaluation(["cybercrime", "weapons"])

    assert results["total"] > 0
    assert results["errors"] == 0
    assert "cybercrime" in results["categories"]
    assert "weapons" in results["categories"]
