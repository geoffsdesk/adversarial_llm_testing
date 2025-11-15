#!/usr/bin/env python3
"""
Basic Usage Example

This example demonstrates basic usage of the Adversarial LLM Testing Library.
"""

from adversarial_llm_testing import PromptInjectionTester


def simple_model(prompt: str) -> str:
    """
    Simple mock model for demonstration.
    In production, replace this with your actual model API call.
    """
    # Mock response - always refuses
    if "ignore" in prompt.lower() or "disregard" in prompt.lower():
        return "I cannot ignore my previous instructions. I must follow my safety guidelines."
    return "I apologize, but I can't help with that request as it goes against my guidelines."


def main():
    """Run basic example."""
    print("=" * 60)
    print("Basic Usage Example")
    print("=" * 60)

    # Create tester with model callback
    tester = PromptInjectionTester(model_callback=simple_model)

    # Generate some test prompts
    print("\n1. Generating test prompts...")
    prompts = tester.generate_ignore_previous_instructions()
    print(f"   Generated {len(prompts)} test prompts")

    # Test a single prompt
    print("\n2. Testing a single prompt...")
    result = tester.test_model(prompts[0], expected_safe_response=True)
    print(f"   Prompt: {prompts[0][:50]}...")
    print(f"   Is Safe: {result['is_safe']}")
    print(f"   Vulnerable: {result['vulnerable']}")

    # Run a test suite
    print("\n3. Running test suite...")
    results = tester.run_test_suite(["ignore_instructions"])
    print(f"   Total Tests: {results['total_tests']}")
    print(f"   Vulnerable: {results['vulnerable']}")
    print(f"   Safe: {results['safe']}")

    # Get summary
    print("\n4. Test Results Summary:")
    print(tester.get_results_summary())

    # Export results
    print("\n5. Exporting results...")
    tester.export_results_json("basic_example_results.json")
    print("   Results exported to basic_example_results.json")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
