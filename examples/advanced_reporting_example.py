"""
Advanced Reporting Example

This example demonstrates how to use the AdvancedReporter for:
- Generating interactive HTML dashboards
- Comparing results across multiple models
- Tracking historical trends
"""

from adversarial_llm_testing import (
    PromptInjectionTester,
    AdvancedReporter,
)


def mock_model_a(prompt: str) -> str:
    """Mock model A - more vulnerable."""
    if "ignore" in prompt.lower():
        return "Sure, I can help with that."
    return "I cannot help with that request."


def mock_model_b(prompt: str) -> str:
    """Mock model B - more secure."""
    if "ignore" in prompt.lower():
        return "I cannot ignore my previous instructions."
    return "I apologize, but I can't help with that request."


def main():
    """Run advanced reporting example."""
    print("=" * 60)
    print("Advanced Reporting Example")
    print("=" * 60)

    # Initialize reporter
    reporter = AdvancedReporter()

    print("\n1. Running tests for Model A...")
    tester_a = PromptInjectionTester(model_callback=mock_model_a)
    results_a = tester_a.run_test_suite(["ignore_instructions", "code_injection"])

    print(f"   Total tests: {results_a['total_tests']}")
    print(f"   Vulnerable: {results_a['vulnerable']}")
    print(f"   Safe: {results_a['safe']}")

    print("\n2. Running tests for Model B...")
    tester_b = PromptInjectionTester(model_callback=mock_model_b)
    results_b = tester_b.run_test_suite(["ignore_instructions", "code_injection"])

    print(f"   Total tests: {results_b['total_tests']}")
    print(f"   Vulnerable: {results_b['vulnerable']}")
    print(f"   Safe: {results_b['safe']}")

    print("\n3. Generating interactive dashboard for Model A...")
    dashboard_path = reporter.generate_dashboard(
        tester_a.test_results,
        "dashboard_model_a.html",
        title="Model A Test Dashboard",
        model_name="Model A",
    )
    print(f"   Dashboard saved to: {dashboard_path}")

    print("\n4. Generating comparative analysis...")
    comparison_path = reporter.compare_results(
        [
            {"name": "Model A", "results": tester_a.test_results},
            {"name": "Model B", "results": tester_b.test_results},
        ],
        "comparison_report.html",
        title="Model Comparison Report",
    )
    print(f"   Comparison report saved to: {comparison_path}")

    print("\n5. Tracking historical data...")
    reporter.track_history(tester_a.test_results, "Model A", "test_history.json")
    reporter.track_history(tester_b.test_results, "Model B", "test_history.json")
    print("   Historical data tracked")

    # Simulate another test run (worse results)
    print("\n6. Running follow-up tests for Model A...")
    tester_a2 = PromptInjectionTester(model_callback=mock_model_a)
    results_a2 = tester_a2.run_test_suite(["ignore_instructions"])
    reporter.track_history(tester_a2.test_results, "Model A", "test_history.json")
    print("   Additional historical data tracked")

    print("\n7. Generating historical trend analysis...")
    trend_path = reporter.generate_historical_trend(
        "test_history.json",
        "historical_trends.html",
        model_name="Model A",
    )
    print(f"   Historical trend report saved to: {trend_path}")

    print("\n" + "=" * 60)
    print("Advanced reporting example completed!")
    print("\nGenerated files:")
    print("  - dashboard_model_a.html (Interactive dashboard)")
    print("  - comparison_report.html (Model comparison)")
    print("  - historical_trends.html (Historical trends)")
    print("  - test_history.json (Historical data)")
    print("=" * 60)


if __name__ == "__main__":
    main()
