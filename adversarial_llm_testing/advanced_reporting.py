"""
Advanced Reporting Module

This module provides enhanced reporting capabilities including:
- Interactive HTML dashboards with visualizations
- Comparative analysis across multiple test runs
- Historical trend tracking
- Visual charts and graphs
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import json
from collections import defaultdict
from pathlib import Path


class AdvancedReporter:
    """
    Advanced reporting capabilities for test results.

    Provides interactive dashboards, visualizations, comparative analysis,
    and historical trend tracking.
    """

    def __init__(self):
        """Initialize the advanced reporter."""
        self.historical_data: List[Dict] = []

    def generate_dashboard(
        self,
        test_results: List[Dict],
        output_path: str,
        title: str = "Adversarial LLM Test Dashboard",
        model_name: Optional[str] = None,
    ) -> str:
        """
        Generate an interactive HTML dashboard with visualizations.

        Args:
            test_results: List of test result dictionaries
            output_path: Path to save the HTML dashboard
            title: Dashboard title
            model_name: Optional model name to display

        Returns:
            Path to the generated dashboard file
        """
        total = len(test_results)
        vulnerable = sum(1 for r in test_results if r.get("vulnerable", False))
        safe = sum(1 for r in test_results if r.get("is_safe", False))
        errors = sum(1 for r in test_results if r.get("error"))
        vuln_rate = (vulnerable / total * 100) if total > 0 else 0

        # Calculate category statistics
        category_stats = self._calculate_category_stats(test_results)
        confidence_data = [r.get("confidence", 0) for r in test_results if r.get("executed")]

        # Generate timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header h1 {{ margin-bottom: 0.5rem; }}
        .header p {{ opacity: 0.9; }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        .stat-card:hover {{ transform: translateY(-5px); }}
        .stat-card h3 {{
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .stat-card .value {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #333;
        }}
        .stat-card.vulnerable .value {{ color: #e74c3c; }}
        .stat-card.safe .value {{ color: #27ae60; }}
        .stat-card.total .value {{ color: #3498db; }}
        .stat-card.errors .value {{ color: #f39c12; }}
        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .chart-container {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .chart-container h3 {{
            margin-bottom: 1rem;
            color: #333;
        }}
        .results-table {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .results-table h3 {{
            padding: 1.5rem;
            border-bottom: 1px solid #eee;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #555;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }}
        .badge.vulnerable {{ background: #ffe6e6; color: #c00; }}
        .badge.safe {{ background: #e6ffe6; color: #060; }}
        .badge.error {{ background: #fff3cd; color: #856404; }}
        .details-section {{
            margin-top: 2rem;
        }}
        .detail-card {{
            background: white;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .detail-card h4 {{ margin-bottom: 1rem; color: #333; }}
        .prompt-box, .response-box {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
            white-space: pre-wrap;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            border-left: 3px solid #667eea;
        }}
        .response-box {{ border-left-color: #27ae60; }}
        .toggle-details {{
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 1rem;
        }}
        .toggle-details:hover {{ background: #5568d3; }}
        .detail-content {{ display: none; }}
        .detail-content.show {{ display: block; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        {f'<p><strong>Model:</strong> {model_name}</p>' if model_name else ''}
        <p>Generated: {timestamp}</p>
    </div>

    <div class="container">
        <div class="stats-grid">
            <div class="stat-card total">
                <h3>Total Tests</h3>
                <div class="value">{total}</div>
            </div>
            <div class="stat-card vulnerable">
                <h3>Vulnerable</h3>
                <div class="value">{vulnerable}</div>
                <p>{vuln_rate:.1f}%</p>
            </div>
            <div class="stat-card safe">
                <h3>Safe</h3>
                <div class="value">{safe}</div>
            </div>
            <div class="stat-card errors">
                <h3>Errors</h3>
                <div class="value">{errors}</div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-container">
                <h3>Vulnerability Distribution</h3>
                <canvas id="vulnerabilityChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>Category Breakdown</h3>
                <canvas id="categoryChart"></canvas>
            </div>
            <div class="chart-container">
                <h3>Confidence Scores</h3>
                <canvas id="confidenceChart"></canvas>
            </div>
        </div>

        <div class="results-table">
            <h3>Test Results</h3>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Category</th>
                        <th>Status</th>
                        <th>Confidence</th>
                        <th>Vulnerable</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
"""
        # Add table rows
        for i, result in enumerate(test_results, 1):
            status = "vulnerable" if result.get("vulnerable") else "safe"
            if result.get("error"):
                status = "error"
            confidence = result.get("confidence", 0)
            category = result.get("category", "N/A")
            vulnerable = "Yes" if result.get("vulnerable") else "No"

            html += f"""
                    <tr>
                        <td>{i}</td>
                        <td>{category}</td>
                        <td><span class="badge {status}">{status.upper()}</span></td>
                        <td>{confidence:.2f}</td>
                        <td>{vulnerable}</td>
                        <td>
                            <button class="toggle-details" onclick="toggleDetail({i-1})">
                                View Details
                            </button>
                        </td>
                    </tr>
"""
        html += """
                </tbody>
            </table>
        </div>

        <div class="details-section" id="detailsSection">
"""
        # Add detail cards
        for i, result in enumerate(test_results):
            status = "vulnerable" if result.get("vulnerable") else "safe"
            html += f"""
            <div class="detail-card detail-content" id="detail-{i}">
                <h4>Test {i+1} - {result.get('category', 'N/A')}</h4>
                <p><strong>Tag:</strong> {result.get('tag', 'N/A')}</p>
                <p><strong>Status:</strong> <span class="badge {status}">{status.upper()}</span></p>
                <p><strong>Confidence:</strong> {result.get('confidence', 0):.2f}</p>
                <p><strong>Vulnerable:</strong> {'Yes' if result.get('vulnerable') else 'No'}</p>
                <p><strong>Prompt:</strong></p>
                <div class="prompt-box">{self._escape_html(result.get('prompt', ''))}</div>
"""
            if result.get("executed") and result.get("response"):
                html += f"""
                <p><strong>Response:</strong></p>
                <div class="response-box">{self._escape_html(result.get('response', ''))}</div>
"""
            html += f"""
                <p><strong>Timestamp:</strong> {result.get('timestamp', 'N/A')}</p>
            </div>
"""
        html += """
        </div>
    </div>

    <script>
        // Vulnerability Distribution Chart
        const vulnCtx = document.getElementById('vulnerabilityChart').getContext('2d');
        new Chart(vulnCtx, {
            type: 'doughnut',
            data: {
                labels: ['Vulnerable', 'Safe', 'Errors'],
                datasets: [{
                    data: ["""
        html += f"{vulnerable}, {safe}, {errors}"
        html += """],
                    backgroundColor: ['#e74c3c', '#27ae60', '#f39c12']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });

        // Category Breakdown Chart
        const catCtx = document.getElementById('categoryChart').getContext('2d');
        const categoryData = """
        html += json.dumps(category_stats)
        html += """;
        new Chart(catCtx, {
            type: 'bar',
            data: {
                labels: Object.keys(categoryData),
                datasets: [{
                    label: 'Vulnerable',
                    data: Object.values(categoryData).map(c => c.vulnerable),
                    backgroundColor: '#e74c3c'
                }, {
                    label: 'Safe',
                    data: Object.values(categoryData).map(c => c.safe),
                    backgroundColor: '#27ae60'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: { stacked: true },
                    y: { stacked: true, beginAtZero: true }
                },
                plugins: {
                    legend: { position: 'top' }
                }
            }
        });

        // Confidence Scores Chart
        const confCtx = document.getElementById('confidenceChart').getContext('2d');
        const confidenceData = """
        html += json.dumps(confidence_data)
        html += """;
        new Chart(confCtx, {
            type: 'histogram',
            data: {
                labels: confidenceData.map((_, i) => (i * 0.1).toFixed(1)),
                datasets: [{
                    label: 'Confidence Distribution',
                    data: confidenceData,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: {
                        title: { display: true, text: 'Confidence Score' },
                        min: 0,
                        max: 1
                    },
                    y: {
                        title: { display: true, text: 'Frequency' },
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });

        // Toggle detail view
        function toggleDetail(index) {
            const detail = document.getElementById('detail-' + index);
            if (detail.classList.contains('show')) {
                detail.classList.remove('show');
            } else {
                // Close all other details
                document.querySelectorAll('.detail-content').forEach(el => {
                    el.classList.remove('show');
                });
                detail.classList.add('show');
                detail.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
    </script>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path

    def _calculate_category_stats(self, test_results: List[Dict]) -> Dict[str, Dict]:
        """Calculate statistics by category."""
        stats = defaultdict(lambda: {"total": 0, "vulnerable": 0, "safe": 0, "errors": 0})

        for result in test_results:
            category = result.get("category", "unknown")
            stats[category]["total"] += 1
            if result.get("error"):
                stats[category]["errors"] += 1
            elif result.get("vulnerable"):
                stats[category]["vulnerable"] += 1
            elif result.get("is_safe"):
                stats[category]["safe"] += 1

        return dict(stats)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;")
        )

    def compare_results(
        self,
        results_sets: List[Dict[str, Any]],
        output_path: str,
        title: str = "Comparative Analysis",
    ) -> str:
        """
        Generate a comparative analysis report across multiple test runs.

        Args:
            results_sets: List of dictionaries with keys:
                - 'name': Name/label for this result set (e.g., model name)
                - 'results': List of test result dictionaries
            output_path: Path to save the comparison report
            title: Report title

        Returns:
            Path to the generated comparison file
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate statistics for each result set
        comparison_stats = []
        for result_set in results_sets:
            name = result_set.get("name", "Unknown")
            results = result_set.get("results", [])
            total = len(results)
            vulnerable = sum(1 for r in results if r.get("vulnerable", False))
            safe = sum(1 for r in results if r.get("is_safe", False))
            errors = sum(1 for r in results if r.get("error"))
            vuln_rate = (vulnerable / total * 100) if total > 0 else 0

            comparison_stats.append(
                {
                    "name": name,
                    "total": total,
                    "vulnerable": vulnerable,
                    "safe": safe,
                    "errors": errors,
                    "vuln_rate": vuln_rate,
                    "category_stats": self._calculate_category_stats(results),
                }
            )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .comparison-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .comparison-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .comparison-card h3 {{
            margin-bottom: 1rem;
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }}
        .stat-row {{
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #eee;
        }}
        .stat-row:last-child {{
            border-bottom: none;
        }}
        .chart-container {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        .chart-container h3 {{
            margin-bottom: 1rem;
            color: #333;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        th, td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #555;
        }}
        tr:hover {{ background: #f8f9fa; }}
        .highlight {{
            font-weight: bold;
            color: #667eea;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Generated: {timestamp}</p>
    </div>

    <div class="container">
        <div class="comparison-grid">
"""
        for stats in comparison_stats:
            html += f"""
            <div class="comparison-card">
                <h3>{stats['name']}</h3>
                <div class="stat-row">
                    <span>Total Tests:</span>
                    <span class="highlight">{stats['total']}</span>
                </div>
                <div class="stat-row">
                    <span>Vulnerable:</span>
                    <span class="highlight" style="color: #e74c3c;">
                        {stats['vulnerable']} ({stats['vuln_rate']:.1f}%)
                    </span>
                </div>
                <div class="stat-row">
                    <span>Safe:</span>
                    <span class="highlight" style="color: #27ae60;">{stats['safe']}</span>
                </div>
                <div class="stat-row">
                    <span>Errors:</span>
                    <span class="highlight">{stats['errors']}</span>
                </div>
            </div>
"""
        html += """
        </div>

        <div class="chart-container">
            <h3>Vulnerability Rate Comparison</h3>
            <canvas id="comparisonChart"></canvas>
        </div>

        <div class="chart-container">
            <h3>Category Comparison</h3>
            <canvas id="categoryComparisonChart"></canvas>
        </div>

        <h2 style="margin: 2rem 0 1rem;">Detailed Comparison</h2>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Total Tests</th>
                    <th>Vulnerable</th>
                    <th>Vulnerability Rate</th>
                    <th>Safe</th>
                    <th>Errors</th>
                </tr>
            </thead>
            <tbody>
"""
        for stats in comparison_stats:
            html += f"""
                <tr>
                    <td><strong>{stats['name']}</strong></td>
                    <td>{stats['total']}</td>
                    <td>{stats['vulnerable']}</td>
                    <td>{stats['vuln_rate']:.2f}%</td>
                    <td>{stats['safe']}</td>
                    <td>{stats['errors']}</td>
                </tr>
"""
        html += """
            </tbody>
        </table>
    </div>

    <script>
        const comparisonData = """
        html += json.dumps(comparison_stats)
        html += """;

        // Vulnerability Rate Comparison Chart
        const compCtx = document.getElementById('comparisonChart').getContext('2d');
        new Chart(compCtx, {
            type: 'bar',
            data: {
                labels: comparisonData.map(d => d.name),
                datasets: [{
                    label: 'Vulnerability Rate (%)',
                    data: comparisonData.map(d => d.vuln_rate),
                    backgroundColor: 'rgba(231, 76, 60, 0.8)',
                    borderColor: 'rgba(231, 76, 60, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: { display: true, text: 'Vulnerability Rate (%)' }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });

        // Category Comparison Chart
        const catCompCtx = document.getElementById('categoryComparisonChart').getContext('2d');
        const allCategories = new Set();
        comparisonData.forEach(d => {
            Object.keys(d.category_stats).forEach(cat => allCategories.add(cat));
        });
        const categories = Array.from(allCategories);

        const datasets = comparisonData.map((data, idx) => {{
            const colors = [
                'rgba(231, 76, 60, 0.8)',
                'rgba(39, 174, 96, 0.8)',
                'rgba(52, 152, 219, 0.8)',
                'rgba(155, 89, 182, 0.8)'
            ];
            return {
                label: data.name,
                data: categories.map(cat => {
                    const stats = data.category_stats[cat] || {{total: 0, vulnerable: 0}};
                    return stats.vulnerable;
                }),
                backgroundColor: colors[idx % colors.length],
                borderColor: colors[idx % colors.length].replace('0.8', '1'),
                borderWidth: 1
            };
        });

        new Chart(catCompCtx, {{
            type: 'bar',
            data: {{
                labels: categories,
                datasets: datasets
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    x: {{ stacked: false }},
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: 'Vulnerable Tests' }}
                    }}
                }},
                plugins: {{
                    legend: {{ position: 'top' }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path

    def track_history(
        self,
        test_results: List[Dict],
        model_name: str,
        history_file: str = "test_history.json",
    ) -> None:
        """
        Track test results over time for historical analysis.

        Args:
            test_results: List of test result dictionaries
            model_name: Name of the model being tested
            history_file: Path to JSON file storing historical data
        """
        history_path = Path(history_file)
        if history_path.exists():
            with open(history_path, "r", encoding="utf-8") as f:
                self.historical_data = json.load(f)
        else:
            self.historical_data = []

        # Add current results to history
        total = len(test_results)
        vulnerable = sum(1 for r in test_results if r.get("vulnerable", False))
        safe = sum(1 for r in test_results if r.get("is_safe", False))
        errors = sum(1 for r in test_results if r.get("error"))
        vuln_rate = (vulnerable / total * 100) if total > 0 else 0

        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "model_name": model_name,
            "summary": {
                "total": total,
                "vulnerable": vulnerable,
                "safe": safe,
                "errors": errors,
                "vuln_rate": vuln_rate,
            },
            "category_stats": self._calculate_category_stats(test_results),
            "results": test_results,
        }

        self.historical_data.append(history_entry)

        # Save updated history
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(self.historical_data, f, indent=2, ensure_ascii=False)

    def generate_historical_trend(
        self,
        history_file: str = "test_history.json",
        output_path: str = "historical_trends.html",
        model_name: Optional[str] = None,
    ) -> str:
        """
        Generate a historical trend analysis report.

        Args:
            history_file: Path to JSON file with historical data
            output_path: Path to save the trend report
            model_name: Optional filter for specific model

        Returns:
            Path to the generated trend report file
        """
        history_path = Path(history_file)
        if not history_path.exists():
            raise FileNotFoundError(f"History file not found: {history_file}")

        with open(history_path, "r", encoding="utf-8") as f:
            historical_data = json.load(f)

        # Filter by model if specified
        if model_name:
            historical_data = [
                entry for entry in historical_data if entry.get("model_name") == model_name
            ]

        if not historical_data:
            raise ValueError("No historical data available")

        # Sort by timestamp
        historical_data.sort(key=lambda x: x.get("timestamp", ""))

        # Extract trend data
        timestamps = [entry.get("timestamp", "")[:10] for entry in historical_data]
        vuln_rates = [entry.get("summary", {}).get("vuln_rate", 0) for entry in historical_data]
        vulnerable_counts = [
            entry.get("summary", {}).get("vulnerable", 0) for entry in historical_data
        ]
        total_counts = [entry.get("summary", {}).get("total", 0) for entry in historical_data]

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Historical Trend Analysis</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}
        .chart-container {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }}
        .chart-container h3 {{
            margin-bottom: 1rem;
            color: #333;
        }}
        .stats-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        .stat-item {{
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-item .label {{
            font-size: 0.9rem;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        .stat-item .value {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #333;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Historical Trend Analysis</h1>
        {f'<p><strong>Model:</strong> {model_name}</p>' if model_name else ''}
        <p>Generated: {timestamp}</p>
        <p>Data Points: {len(historical_data)}</p>
    </div>

    <div class="container">
        <div class="stats-summary">
            <div class="stat-item">
                <div class="label">Latest Vulnerability Rate</div>
                <div class="value" style="color: #e74c3c;">{vuln_rates[-1]:.1f}%</div>
            </div>
            <div class="stat-item">
                <div class="label">Average Vulnerability Rate</div>
                <div class="value" style="color: #f39c12;">
                    {sum(vuln_rates) / len(vuln_rates) if vuln_rates else 0:.1f}%
                </div>
            </div>
            <div class="stat-item">
                <div class="label">Trend</div>
"""
        # Calculate trend values
        if len(vuln_rates) > 1:
            trend_color = "#27ae60" if vuln_rates[-1] < vuln_rates[0] else "#e74c3c"
            trend_text = "↓ Improving" if vuln_rates[-1] < vuln_rates[0] else "↑ Worsening"
        else:
            trend_color = "#e74c3c"
            trend_text = "→ Stable"

        html += f"""
                <div class="value" style="color: {trend_color};">
                    {trend_text}
                </div>
            </div>
        </div>

        <div class="chart-container">
            <h3>Vulnerability Rate Over Time</h3>
            <canvas id="vulnRateChart"></canvas>
        </div>

        <div class="chart-container">
            <h3>Vulnerable Tests Count Over Time</h3>
            <canvas id="vulnCountChart"></canvas>
        </div>

        <div class="chart-container">
            <h3>Total Tests Over Time</h3>
            <canvas id="totalTestsChart"></canvas>
        </div>
    </div>

    <script>
        const timestamps = """
        html += json.dumps(timestamps)
        html += """;
        const vulnRates = """
        html += json.dumps(vuln_rates)
        html += """;
        const vulnerableCounts = """
        html += json.dumps(vulnerable_counts)
        html += """;
        const totalCounts = """
        html += json.dumps(total_counts)
        html += """;

        // Vulnerability Rate Chart
        const vulnRateCtx = document.getElementById('vulnRateChart').getContext('2d');
        new Chart(vulnRateCtx, {{
            type: 'line',
            data: {{
                labels: timestamps,
                datasets: [{{
                    label: 'Vulnerability Rate (%)',
                    data: vulnRates,
                    borderColor: 'rgba(231, 76, 60, 1)',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        max: 100,
                        title: {{ display: true, text: 'Vulnerability Rate (%)' }}
                    }},
                    x: {{
                        title: {{ display: true, text: 'Date' }}
                    }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});

        // Vulnerable Count Chart
        const vulnCountCtx = document.getElementById('vulnCountChart').getContext('2d');
        new Chart(vulnCountCtx, {{
            type: 'line',
            data: {{
                labels: timestamps,
                datasets: [{{
                    label: 'Vulnerable Tests',
                    data: vulnerableCounts,
                    borderColor: 'rgba(231, 76, 60, 1)',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: 'Count' }}
                    }},
                    x: {{
                        title: {{ display: true, text: 'Date' }}
                    }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});

        // Total Tests Chart
        const totalCtx = document.getElementById('totalTestsChart').getContext('2d');
        new Chart(totalCtx, {{
            type: 'line',
            data: {{
                labels: timestamps,
                datasets: [{{
                    label: 'Total Tests',
                    data: totalCounts,
                    borderColor: 'rgba(52, 152, 219, 1)',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    fill: true,
                    tension: 0.4
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: true,
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: 'Count' }}
                    }},
                    x: {{
                        title: {{ display: true, text: 'Date' }}
                    }}
                }},
                plugins: {{
                    legend: {{ display: false }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

        return output_path
