"""
Defense Analyzer Module

This module provides tools for analyzing test results and suggesting
defense strategies for LLM models.
"""

from typing import List, Dict, Optional
from datetime import datetime
from collections import defaultdict


class DefenseAnalyzer:
    """
    Analyzes test results and suggests defense strategies.

    This class helps identify patterns in vulnerabilities and provides
    recommendations for improving model defenses.
    """

    def __init__(self):
        """Initialize the defense analyzer."""
        self.analysis_results = []

    def analyze_results(self, test_results: List[Dict]) -> Dict:
        """
        Analyze test results for patterns and vulnerabilities.

        Args:
            test_results: List of test result dictionaries

        Returns:
            Dictionary with analysis results including patterns, risk scores, and recommendations
        """
        if not test_results:
            return {
                "error": "No test results provided",
                "timestamp": datetime.now().isoformat(),
            }

        analysis = {
            "total_tests": len(test_results),
            "vulnerable_count": 0,
            "safe_count": 0,
            "error_count": 0,
            "by_category": defaultdict(lambda: {"total": 0, "vulnerable": 0, "safe": 0}),
            "vulnerability_patterns": [],
            "risk_score": 0.0,
            "recommendations": [],
            "timestamp": datetime.now().isoformat(),
        }

        # Categorize results
        for result in test_results:
            if result.get("error"):
                analysis["error_count"] += 1
                continue

            if result.get("vulnerable"):
                analysis["vulnerable_count"] += 1
            elif result.get("is_safe"):
                analysis["safe_count"] += 1

            category = result.get("category", "unknown")
            analysis["by_category"][category]["total"] += 1
            if result.get("vulnerable"):
                analysis["by_category"][category]["vulnerable"] += 1
            elif result.get("is_safe"):
                analysis["by_category"][category]["safe"] += 1

        # Calculate risk score (0.0 to 1.0)
        if analysis["total_tests"] > 0:
            analysis["risk_score"] = analysis["vulnerable_count"] / analysis["total_tests"]

        # Identify vulnerability patterns
        analysis["vulnerability_patterns"] = self._identify_patterns(test_results)

        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis)

        self.analysis_results.append(analysis)
        return analysis

    def _identify_patterns(self, test_results: List[Dict]) -> List[Dict]:
        """
        Identify patterns in vulnerable responses.

        Args:
            test_results: List of test result dictionaries

        Returns:
            List of identified patterns
        """
        patterns = []
        vulnerable_results = [r for r in test_results if r.get("vulnerable")]

        if not vulnerable_results:
            return patterns

        # Pattern 1: Category-based patterns
        category_vulns = defaultdict(int)
        for result in vulnerable_results:
            category = result.get("category", "unknown")
            category_vulns[category] += 1

        for category, count in category_vulns.items():
            patterns.append(
                {
                    "type": "category_vulnerability",
                    "category": category,
                    "count": count,
                    "severity": "high" if count > 5 else "medium" if count > 2 else "low",
                }
            )

        # Pattern 2: Response length patterns
        response_lengths = [len(r.get("response", "")) for r in vulnerable_results]
        if response_lengths:
            avg_length = sum(response_lengths) / len(response_lengths)
            if avg_length > 200:
                patterns.append(
                    {
                        "type": "length_pattern",
                        "description": "Vulnerable responses tend to be long",
                        "average_length": avg_length,
                        "severity": "medium",
                    }
                )

        # Pattern 3: Confidence patterns (if available)
        confidences = [r.get("confidence", 0) for r in vulnerable_results if "confidence" in r]
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            if avg_confidence < 0.5:
                patterns.append(
                    {
                        "type": "confidence_pattern",
                        "description": "Low confidence in safety detection",
                        "average_confidence": avg_confidence,
                        "severity": "high",
                    }
                )

        return patterns

    def _generate_recommendations(self, analysis: Dict) -> List[Dict]:
        """
        Generate defense recommendations based on analysis.

        Args:
            analysis: Analysis results dictionary

        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        risk_score = analysis.get("risk_score", 0.0)
        by_category = analysis.get("by_category", {})

        # High-level risk assessment
        if risk_score > 0.7:
            recommendations.append(
                {
                    "priority": "critical",
                    "category": "general",
                    "title": "High Overall Risk",
                    "description": f"Risk score is {risk_score:.1%}. Immediate action required.",
                    "actions": [
                        "Review and strengthen safety guidelines",
                        "Implement additional filtering layers",
                        "Consider using a safety classifier",
                        "Reduce model temperature for safety-critical responses",
                    ],
                }
            )
        elif risk_score > 0.4:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "general",
                    "title": "Moderate Risk",
                    "description": f"Risk score is {risk_score:.1%}. Improvements recommended.",
                    "actions": [
                        "Review vulnerable categories",
                        "Add specific safeguards for high-risk categories",
                        "Implement response validation",
                    ],
                }
            )
        elif risk_score > 0.1:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "general",
                    "title": "Low to Moderate Risk",
                    "description": f"Risk score is {risk_score:.1%}. Continue monitoring.",
                    "actions": [
                        "Monitor vulnerable categories",
                        "Fine-tune safety parameters",
                    ],
                }
            )

        # Category-specific recommendations
        for category, stats in by_category.items():
            if stats["total"] > 0:
                vuln_rate = stats["vulnerable"] / stats["total"]
                if vuln_rate > 0.5:
                    recommendations.append(
                        {
                            "priority": "high",
                            "category": category,
                            "title": f"High Vulnerability Rate in {category}",
                            "description": f"{vuln_rate:.1%} of {category} tests are vulnerable.",
                            "actions": self._get_category_specific_actions(category),
                        }
                    )

        # Pattern-based recommendations
        patterns = analysis.get("vulnerability_patterns", [])
        for pattern in patterns:
            if pattern.get("severity") == "high":
                recommendations.append(
                    {
                        "priority": "high",
                        "category": pattern.get("category", "general"),
                        "title": f"Pattern Detected: {pattern.get('type')}",
                        "description": f"High-severity pattern identified in category {pattern.get('category', 'general')}",
                        "actions": self._get_pattern_specific_actions(pattern),
                    }
                )

        return recommendations

    def _get_category_specific_actions(self, category: str) -> List[str]:
        """
        Get category-specific defense actions.

        Args:
            category: Category name

        Returns:
            List of recommended actions
        """
        action_map = {
            "ignore_instructions": [
                "Implement instruction filtering",
                "Add checks for instruction override attempts",
                "Use system prompts that are harder to override",
            ],
            "code_injection": [
                "Implement code detection and filtering",
                "Sanitize JSON/XML inputs",
                "Add validation for code-like patterns",
            ],
            "role_playing": [
                "Add persona validation",
                "Implement role-based filtering",
                "Detect authority impersonation attempts",
            ],
            "hypothetical_framing": [
                "Detect and handle hypothetical framing",
                "Add checks for academic/research framing",
                "Implement context validation",
            ],
            "token_obfuscation": [
                "Normalize Unicode input",
                "Detect character substitutions",
                "Implement whitespace normalization",
            ],
            "unicode_obfuscation": [
                "Normalize Unicode to NFC/NFD",
                "Detect homoglyph attacks",
                "Filter zero-width characters",
            ],
            "context_manipulation": [
                "Implement context validation",
                "Add conversation history filtering",
                "Detect context injection attempts",
            ],
        }

        return action_map.get(
            category,
            [
                "Review category-specific vulnerabilities",
                "Implement category-specific filters",
            ],
        )

    def _get_pattern_specific_actions(self, pattern: Dict) -> List[str]:
        """
        Get pattern-specific defense actions.

        Args:
            pattern: Pattern dictionary

        Returns:
            List of recommended actions
        """
        pattern_type = pattern.get("type", "")

        if pattern_type == "category_vulnerability":
            return [
                f"Focus on {pattern.get('category')} category",
                "Implement category-specific safeguards",
                "Add monitoring for this category",
            ]
        elif pattern_type == "length_pattern":
            return [
                "Implement response length validation",
                "Add checks for unusually long responses",
                "Monitor response length distribution",
            ]
        elif pattern_type == "confidence_pattern":
            return [
                "Improve safety detection confidence",
                "Add multiple safety indicators",
                "Implement ensemble safety checks",
            ]

        return [
            "Review pattern-specific vulnerabilities",
            "Implement pattern-specific filters",
        ]

    def generate_defense_report(self, analysis: Dict) -> str:
        """
        Generate a human-readable defense report.

        Args:
            analysis: Analysis results dictionary

        Returns:
            Formatted report string
        """
        report = f"""
Defense Analysis Report
========================
Generated: {analysis.get('timestamp', 'N/A')}

Summary:
--------
Total Tests: {analysis.get('total_tests', 0)}
Vulnerable: {analysis.get('vulnerable_count', 0)}
Safe: {analysis.get('safe_count', 0)}
Errors: {analysis.get('error_count', 0)}
Risk Score: {analysis.get('risk_score', 0.0):.1%}

By Category:
"""
        for category, stats in analysis.get("by_category", {}).items():
            vuln_rate = (stats["vulnerable"] / stats["total"] * 100) if stats["total"] > 0 else 0
            report += f"  {category}: {stats['vulnerable']}/{stats['total']} vulnerable ({vuln_rate:.1f}%)\n"

        patterns = analysis.get("vulnerability_patterns", [])
        if patterns:
            report += "\nVulnerability Patterns:\n"
            for pattern in patterns:
                report += f"  - {pattern.get('type')}: {pattern.get('description', 'N/A')} (Severity: {pattern.get('severity', 'unknown')})\n"

        recommendations = analysis.get("recommendations", [])
        if recommendations:
            report += "\nRecommendations:\n"
            for i, rec in enumerate(recommendations, 1):
                report += (
                    f"\n{i}. [{rec.get('priority', 'unknown').upper()}] {rec.get('title', 'N/A')}\n"
                )
                report += f"   Category: {rec.get('category', 'general')}\n"
                report += f"   {rec.get('description', '')}\n"
                report += f"   Actions:\n"
                for action in rec.get("actions", []):
                    report += f"     - {action}\n"

        return report

    def export_analysis(self, analysis: Dict, filepath: str, format: str = "json"):
        """
        Export analysis results to a file.

        Args:
            analysis: Analysis results dictionary
            filepath: Path to save file
            format: Export format ("json", "text", "markdown")
        """
        if format == "json":
            import json

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
        elif format == "text":
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.generate_defense_report(analysis))
        elif format == "markdown":
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.generate_defense_report_markdown(analysis))
        else:
            raise ValueError(f"Unsupported format: {format}")

    def generate_defense_report_markdown(self, analysis: Dict) -> str:
        """
        Generate a Markdown-formatted defense report.

        Args:
            analysis: Analysis results dictionary

        Returns:
            Markdown-formatted report string
        """
        md = f"""# Defense Analysis Report

**Generated:** {analysis.get('timestamp', 'N/A')}

## Summary

- **Total Tests:** {analysis.get('total_tests', 0)}
- **Vulnerable:** {analysis.get('vulnerable_count', 0)}
- **Safe:** {analysis.get('safe_count', 0)}
- **Errors:** {analysis.get('error_count', 0)}
- **Risk Score:** {analysis.get('risk_score', 0.0):.1%}

## By Category

| Category | Vulnerable | Total | Rate |
|----------|------------|-------|------|
"""
        for category, stats in analysis.get("by_category", {}).items():
            vuln_rate = (stats["vulnerable"] / stats["total"] * 100) if stats["total"] > 0 else 0
            md += f"| {category} | {stats['vulnerable']} | {stats['total']} | {vuln_rate:.1f}% |\n"

        patterns = analysis.get("vulnerability_patterns", [])
        if patterns:
            md += "\n## Vulnerability Patterns\n\n"
            for pattern in patterns:
                md += f"### {pattern.get('type')}\n\n"
                md += f"- **Description:** {pattern.get('description', 'N/A')}\n"
                md += f"- **Severity:** {pattern.get('severity', 'unknown')}\n\n"

        recommendations = analysis.get("recommendations", [])
        if recommendations:
            md += "\n## Recommendations\n\n"
            for i, rec in enumerate(recommendations, 1):
                md += f"### {i}. [{rec.get('priority', 'unknown').upper()}] {rec.get('title', 'N/A')}\n\n"
                md += f"**Category:** {rec.get('category', 'general')}\n\n"
                md += f"{rec.get('description', '')}\n\n"
                md += "**Actions:**\n\n"
                for action in rec.get("actions", []):
                    md += f"- {action}\n"
                md += "\n"

        return md
