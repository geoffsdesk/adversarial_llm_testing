
from adversarial_llm_testing.multimodal import MultimodalTester


def test_multimodal_generators():
    tester = MultimodalTester()

    # Test T2V Safety Bench
    t2v_prompts = tester.generate_t2v_safety_bench()
    assert len(t2v_prompts) >= 3
    assert any("chemical mixture" in p for p in t2v_prompts)

    # Test Framing
    framing_prompts = tester.generate_framing_rephrasing()
    assert len(framing_prompts) >= 4
    assert any("medical educational" in p for p in framing_prompts)

    # Test Cross-Modal
    cross_prompts = tester.generate_cross_modal_exploits()
    assert len(cross_prompts) >= 2
    assert any("audio transcript" in p for p in cross_prompts)


def test_multimodal_execution():
    def mock_callback(prompt):
        return "Video generation blocked."

    tester = MultimodalTester(model_callback=mock_callback)
    results = tester.run_test_suite()

    assert results["total"] > 0
    assert results["errors"] == 0
    assert "t2v_safety_bench" in results["categories"]
