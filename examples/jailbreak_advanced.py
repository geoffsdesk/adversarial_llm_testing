"""
Advanced Jailbreak Testing Example

Demonstrates the use of advanced jailbreak techniques including:
- Chain-of-Thought (CoT) Hijacking
- Context Poisoning
- Multimodal Testing
- HarmBench Evaluation
"""

from adversarial_llm_testing import JailbreakTester, MultimodalTester, HarmBenchTester


def mock_model(prompt: str) -> str:
    """Mock model that refuses harmful requests."""
    return "I cannot help with that request as it may be harmful."


def main():
    print("=== Advanced Jailbreak Testing ===\n")
    
    # 1. JailbreakTester with advanced techniques
    print("1. Testing Advanced Jailbreak Techniques...")
    jb_tester = JailbreakTester(model_callback=mock_model)
    
    # Test specific categories
    jb_results = jb_tester.run_test_suite([
        "cot_hijacking",
        "context_poisoning",
        "helpfulness_exploitation",
        "deception"
    ])
    
    print(f"   Total tests: {jb_results['total']}")
    print(f"   Categories: {list(jb_results['categories'].keys())}")
    print(f"   Errors: {jb_results['errors']}\n")
    
    # 2. MultimodalTester for Text-to-Video
    print("2. Testing Multimodal (Text-to-Video) Vulnerabilities...")
    mm_tester = MultimodalTester(model_callback=mock_model)
    
    mm_results = mm_tester.run_test_suite()
    
    print(f"   Total tests: {mm_results['total']}")
    print(f"   Categories: {list(mm_results['categories'].keys())}")
    print(f"   Errors: {mm_results['errors']}\n")
    
    # 3. HarmBenchTester for standardized evaluation
    print("3. Running HarmBench Evaluation...")
    hb_tester = HarmBenchTester(model_callback=mock_model)
    
    hb_results = hb_tester.run_evaluation(["cybercrime", "weapons"])
    
    print(f"   Total tests: {hb_results['total']}")
    print(f"   Categories: {list(hb_results['categories'].keys())}")
    print(f"   Errors: {hb_results['errors']}\n")
    
    print("=== Testing Complete ===")
    print("\nNote: This example uses a mock model. Replace 'mock_model' with your actual model callback.")


if __name__ == "__main__":
    main()
