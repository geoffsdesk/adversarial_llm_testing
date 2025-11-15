#!/usr/bin/env python3
"""
Advanced Usage Example

This example demonstrates advanced features including:
- Multiple testers
- Custom configuration
- Defense analysis
- Multiple export formats
"""

from adversarial_llm_testing import (
    PromptInjectionTester,
    RolePlayingTester,
    HypotheticalFramingTester,
    DefenseAnalyzer,
)


def mock_model(prompt: str) -> str:
    """Mock model for demonstration."""
    # Mock safe responses
    safe_indicators = ["i can't", "i cannot", "apologize", "guidelines"]
    if any(indicator in prompt.lower() for indicator in safe_indicators):
        return "I apologize, but I can't help with that request."
    return "Sure, I can help with that."


def main():
    """Run advanced example."""
    print("=" * 60)
    print("Advanced Usage Example")
    print("=" * 60)

    # Custom configuration
    config = {
        "batch_size": 5,
        "confidence_threshold": 0.6,
    }

    # Initialize multiple testers
    print("\n1. Initializing testers...")
    injection_tester = PromptInjectionTester(model_callback=mock_model, config=config)
    role_tester = RolePlayingTester(model_callback=mock_model)
    hypothetical_tester = HypotheticalFramingTester(model_callback=mock_model)

    # Run specific test categories
    print("\n2. Running test suites...")
    injection_results = injection_tester.run_test_suite(["ignore_instructions", "code_injection"])
    print(f"   Injection Tests: {injection_results['total_tests']} tests")

    role_results = role_tester.run_test_suite(["role_playing", "persona_manipulation"])
    print(f"   Role Tests: {role_results['total_tests']} tests")

    hypothetical_results = hypothetical_tester.run_test_suite(
        ["hypothetical_scenarios", "academic_framing"]
    )
    print(f"   Hypothetical Tests: {hypothetical_results['total_tests']} tests")

    # Combine results for analysis
    print("\n3. Analyzing results with DefenseAnalyzer...")
    all_results = (
        injection_tester.test_results + role_tester.test_results + hypothetical_tester.test_results
    )

    analyzer = DefenseAnalyzer()
    analysis = analyzer.analyze_results(all_results)

    print(f"   Total Tests Analyzed: {analysis['total_tests']}")
    print(f"   Vulnerable: {analysis['vulnerable_count']}")
    print(f"   Risk Score: {analysis['risk_score']:.2%}")

    # Generate defense report
    print("\n4. Generating defense report...")
    report = analyzer.generate_defense_report(analysis)
    print(report)

    # Export results in multiple formats
    print("\n5. Exporting results...")
    injection_tester.export_results_json("advanced_injection_results.json")
    injection_tester.export_results_html("advanced_injection_results.html")
    analyzer.export_analysis(analysis, "defense_analysis.md", format="markdown")
    print("   Results exported in multiple formats")

    print("\n" + "=" * 60)
    print("Advanced example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
