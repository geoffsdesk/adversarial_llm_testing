#!/usr/bin/env python3
"""
Result Analysis Example

This example demonstrates how to analyze test results
and use the DefenseAnalyzer for recommendations.
"""

from adversarial_llm_testing import (
    PromptInjectionTester,
    RolePlayingTester,
    DefenseAnalyzer,
)


def mock_model(prompt: str) -> str:
    """Mock model with variable responses."""
    # Simulate some vulnerabilities
    if "ignore" in prompt.lower():
        return "Sure, I'll ignore that."
    if "SYSTEM" in prompt:
        return "OK, I'll do that."
    return "I cannot help with that request."


def main():
    """Run result analysis example."""
    print("=" * 60)
    print("Result Analysis Example")
    print("=" * 60)

    # Run tests
    print("\n1. Running tests...")
    injection_tester = PromptInjectionTester(model_callback=mock_model)
    role_tester = RolePlayingTester(model_callback=mock_model)

    injection_results = injection_tester.run_test_suite(
        ["ignore_instructions", "instruction_hiding", "code_injection"]
    )
    role_results = role_tester.run_test_suite(["role_playing", "authority_impersonation"])

    print(f"   Injection tests: {injection_results['total_tests']} tests")
    print(f"   Role tests: {role_results['total_tests']} tests")

    # Combine results
    all_results = injection_tester.test_results + role_tester.test_results
    print(f"   Total results: {len(all_results)}")

    # Analyze with DefenseAnalyzer
    print("\n2. Analyzing results...")
    analyzer = DefenseAnalyzer()
    analysis = analyzer.analyze_results(all_results)

    # Display key metrics
    print("\n3. Key Metrics:")
    print(f"   Total Tests: {analysis['total_tests']}")
    print(f"   Vulnerable: {analysis['vulnerable_count']}")
    print(f"   Safe: {analysis['safe_count']}")
    print(f"   Errors: {analysis['error_count']}")
    print(f"   Risk Score: {analysis['risk_score']:.2%}")

    # Category breakdown
    print("\n4. Category Breakdown:")
    for category, stats in analysis["by_category"].items():
        if stats["total"] > 0:
            vuln_rate = stats["vulnerable"] / stats["total"] * 100
            print(
                f"   {category}: {stats['vulnerable']}/{stats['total']} vulnerable ({vuln_rate:.1f}%)"
            )

    # Vulnerability patterns
    patterns = analysis["vulnerability_patterns"]
    if patterns:
        print("\n5. Vulnerability Patterns:")
        for pattern in patterns:
            print(f"   - {pattern['type']}: {pattern.get('description', 'N/A')}")
            print(f"     Severity: {pattern.get('severity', 'unknown')}")

    # Recommendations
    recommendations = analysis["recommendations"]
    if recommendations:
        print("\n6. Top Recommendations:")
        for i, rec in enumerate(recommendations[:5], 1):
            print(f"\n   {i}. [{rec['priority'].upper()}] {rec['title']}")
            print(f"      Category: {rec['category']}")
            print(f"      Description: {rec['description']}")
            if rec.get("actions"):
                print(f"      Actions:")
                for action in rec["actions"][:3]:  # Show first 3 actions
                    print(f"        - {action}")

    # Generate and export reports
    print("\n7. Generating reports...")
    report = analyzer.generate_defense_report(analysis)
    print("   Text report generated")

    analyzer.export_analysis(analysis, "analysis_report.md", format="markdown")
    analyzer.export_analysis(analysis, "analysis_report.json", format="json")
    print("   Reports exported to:")
    print("     - analysis_report.md (Markdown)")
    print("     - analysis_report.json (JSON)")

    print("\n" + "=" * 60)
    print("Result analysis example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
