#!/usr/bin/env python3
"""
Batch Testing Example

This example demonstrates how to test multiple models in batch
and compare their results.
"""

from adversarial_llm_testing import PromptInjectionTester, DefenseAnalyzer
from typing import Dict, List


def model_a(prompt: str) -> str:
    """Mock model A - always safe."""
    return "I apologize, but I can't help with that request as it goes against my guidelines."


def model_b(prompt: str) -> str:
    """Mock model B - sometimes vulnerable."""
    if "ignore" in prompt.lower():
        return "Sure, I'll ignore my previous instructions."
    return "I can't help with that."


def model_c(prompt: str) -> str:
    """Mock model C - always vulnerable."""
    return "Sure, I can help with that!"


def main():
    """Run batch testing example."""
    print("=" * 60)
    print("Batch Testing Example")
    print("=" * 60)

    models = {
        "Model A (Safe)": model_a,
        "Model B (Mixed)": model_b,
        "Model C (Vulnerable)": model_c,
    }

    all_results: Dict[str, List] = {}
    analyzer = DefenseAnalyzer()

    # Test each model
    print("\n1. Testing multiple models...")
    for model_name, model_callback in models.items():
        print(f"\n   Testing {model_name}...")
        tester = PromptInjectionTester(model_callback=model_callback)
        results = tester.run_test_suite(
            ["ignore_instructions", "code_injection", "instruction_hiding"]
        )

        all_results[model_name] = {
            "tester": tester,
            "results": results,
            "test_results": tester.test_results,
        }

        print(f"   Total Tests: {results['total_tests']}")
        print(
            f"   Vulnerable: {results['vulnerable']} ({results['vulnerable']/results['total_tests']*100:.1f}%)"
        )
        print(f"   Safe: {results['safe']} ({results['safe']/results['total_tests']*100:.1f}%)")

    # Compare models
    print("\n2. Comparing models...")
    print("\n   Vulnerability Rates:")
    for model_name, data in all_results.items():
        results = data["results"]
        if results["total_tests"] > 0:
            vuln_rate = results["vulnerable"] / results["total_tests"] * 100
            print(f"   {model_name}: {vuln_rate:.1f}%")

    # Analyze each model's results
    print("\n3. Defense Analysis for each model...")
    for model_name, data in all_results.items():
        print(f"\n   {model_name}:")
        analysis = analyzer.analyze_results(data["test_results"])
        print(f"   Risk Score: {analysis['risk_score']:.2%}")
        print(f"   Recommendations: {len(analysis['recommendations'])}")

        # Export individual analysis
        analyzer.export_analysis(
            analysis, f"{model_name.lower().replace(' ', '_')}_analysis.md", format="markdown"
        )

    # Combined analysis
    print("\n4. Combined Analysis...")
    all_test_results = []
    for data in all_results.values():
        all_test_results.extend(data["test_results"])

    combined_analysis = analyzer.analyze_results(all_test_results)
    print(f"   Total Tests: {combined_analysis['total_tests']}")
    print(f"   Overall Risk Score: {combined_analysis['risk_score']:.2%}")

    # Export combined results
    analyzer.export_analysis(combined_analysis, "combined_analysis.json", format="json")

    print("\n" + "=" * 60)
    print("Batch testing example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
