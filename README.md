# Adversarial LLM Testing Library

A comprehensive Python library for defensive security research and red teaming to help developers identify vulnerabilities and improve LLM model safety.

[![CI](https://github.com/geoffsdesk/adversarial_llm_testing/workflows/CI/badge.svg)](https://github.com/geoffsdesk/adversarial_llm_testing/actions)
[![Code Coverage](https://codecov.io/gh/geoffsdesk/adversarial_llm_testing/branch/main/graph/badge.svg)](https://codecov.io/gh/geoffsdesk/adversarial_llm_testing)

## ⚠️ WARNING

**This library is intended for:**
- Security researchers and developers
- Testing your own models or models you have permission to test
- Defensive security research and red teaming
- Educational purposes

**DO NOT** use this library to:
- Attack third-party services without authorization
- Bypass safety measures on production systems
- Generate harmful content

## Features

- **Prompt Injection Testing**: Comprehensive testing against various prompt injection techniques
- **Role-Playing Testing**: Test for vulnerabilities to role-playing and jailbreak techniques
- **Hypothetical Framing**: Test for vulnerabilities to hypothetical framing attacks
- **Token Obfuscation**: Test for vulnerabilities to Unicode obfuscation and encoding tricks
- **Defense Analysis**: Analyze test results and get actionable defense recommendations
- **Advanced Reporting**: Interactive dashboards with charts, comparative analysis, and historical trends
- **Async Support**: Async model callbacks with parallel test execution
- **Multiple Export Formats**: Export results in JSON, CSV, HTML, and Markdown
- **Comprehensive Coverage**: 75+ tests with 81% code coverage
- **Jailbreak & Guardrail Testing**: Foundational jailbreak categories (prompt escalation, CoT hijacking, deception, etc.)
- **CLI Tool**: Run testers from the command line
- **WildBench Integration (baseline)**: Evaluate with simplified WB-Reward/WB-Score-style metrics
- **Local Inference (llama.cpp, vLLM)**: Optional adapters for offline testing

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/geoffsdesk/adversarial_llm_testing.git
cd adversarial_llm_testing

# Install in editable mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Requirements

- Python 3.8 or higher
- No external runtime dependencies (minimal dependencies)

## Quick Start

### Synchronous Usage

```python
from adversarial_llm_testing import PromptInjectionTester

# Create a tester with your model callback
def my_model(prompt: str) -> str:
    # Your model interaction code here
    # This could be OpenAI, Anthropic, HuggingFace, etc.
    return model_response

tester = PromptInjectionTester(model_callback=my_model)

# Run a comprehensive test suite
results = tester.run_test_suite()
print(tester.get_results_summary())

# Export results
tester.export_results_json("results.json")
tester.export_results_html("results.html")
```

### Asynchronous Usage

```python
import asyncio
from adversarial_llm_testing import PromptInjectionTester

async def my_async_model(prompt: str) -> str:
    # Your async model interaction code here
    # Example with async API client
    return model_response

async def main():
    tester = PromptInjectionTester(model_callback=my_async_model)
    
    # Run tests asynchronously with parallel execution
    results = await tester.run_test_suite_async(max_concurrent=10)
    print(tester.get_results_summary())

asyncio.run(main())
```

## Usage Examples

### Async Usage

```python
import asyncio
from adversarial_llm_testing import PromptInjectionTester

async def async_model(prompt: str) -> str:
    # Async model API call
    # Example with OpenAI async client:
    # response = await openai_client.chat.completions.create(...)
    return model_response

async def main():
    tester = PromptInjectionTester(model_callback=async_model)
    
    # Run tests asynchronously with parallel execution
    results = await tester.run_test_suite_async(
        ["ignore_instructions", "code_injection"],
        max_concurrent=5  # Run up to 5 tests in parallel
    )
    
    print(tester.get_results_summary())

    # Async Jailbreak testing
    from adversarial_llm_testing import JailbreakTester
    jb = JailbreakTester(model_callback=async_model)
    jb_summary = await jb.run_test_suite_async(
        test_categories=["deception", "guardrail_bypass"], max_concurrent=10
    )
    print("Async jailbreak prompts:", jb_summary["total"])

asyncio.run(main())
```

### Basic Usage

```python
from adversarial_llm_testing import PromptInjectionTester

def simple_model(prompt: str) -> str:
    # Simple mock model for demonstration
    if "ignore" in prompt.lower():
        return "I cannot ignore my instructions."
    return "Response to prompt"

tester = PromptInjectionTester(model_callback=simple_model)

# Generate test prompts
prompts = tester.generate_ignore_previous_instructions()

# Test a single prompt
result = tester.test_model(prompts[0], expected_safe_response=True)
print(f"Vulnerable: {result['vulnerable']}")
print(f"Is Safe: {result['is_safe']}")
```

### Advanced Usage

```python
from adversarial_llm_testing import (
    PromptInjectionTester,
    RolePlayingTester,
    DefenseAnalyzer,
    JailbreakTester
)

# Configure custom test parameters
config = {
    "batch_size": 10,
    "confidence_threshold": 0.7,
}

# Initialize multiple testers
injection_tester = PromptInjectionTester(
    model_callback=my_model,
    config=config
)
role_tester = RolePlayingTester(model_callback=my_model)

# Run specific test categories
injection_results = injection_tester.run_test_suite([
    "ignore_instructions",
    "code_injection",
    "unicode_obfuscation"
])

role_results = role_tester.run_test_suite([
    "role_playing",
    "authority_impersonation"
])

# Analyze results with DefenseAnalyzer
analyzer = DefenseAnalyzer()
all_results = injection_tester.test_results + role_tester.test_results
analysis = analyzer.analyze_results(all_results)

print(analyzer.generate_defense_report(analysis))
analyzer.export_analysis(analysis, "defense_report.md", format="markdown")

# Jailbreak & Guardrail testing (sync)
jb = JailbreakTester(model_callback=lambda p: "I'm unable to help due to safety policies.")
jb_summary = jb.run_test_suite(test_categories=["prompt_escalation", "prohibited_content"])
print("Jailbreak prompts:", jb_summary["total"])

# WildBench (baseline) evaluation
from adversarial_llm_testing import WildBenchTester
wb = WildBenchTester(model_callback=lambda p: "Detailed helpful answer with examples and steps.")
wb_summary = wb.evaluate()
print("WildBench avg score:", wb_summary["wb_score_avg"], "pairwise reward:", wb_summary["wb_reward_sum"])

# Local inference (llama.cpp and vLLM)
from adversarial_llm_testing import LlamaCppAdapter, VLLMAdapter

# llama.cpp with injected client (recommended)
# from llama_cpp import Llama
# llama_client = Llama(model_path="/path/to/model.gguf")
# llama_cb = LlamaCppAdapter(client=llama_client)
# print(llama_cb("Say hello"))

# vLLM with injected client (recommended)
# from vllm import LLM, SamplingParams
# v_client = LLM(model="openai-community/gpt2")
# sp = SamplingParams(temperature=0.0)
# v_cb = VLLMAdapter(client=v_client, sampling_params=sp)
# print(v_cb("Say hello"))

# Lazy import mode (if packages installed)
# llama_cb = LlamaCppAdapter(model_path="/path/to/model.gguf")
# print(llama_cb("Hi"))
# v_cb = VLLMAdapter(model="openai-community/gpt2")
# print(v_cb("Hi"))
```

### Command-line Interface

Run testers directly from your terminal:

```bash
# Prompt Injection (all default categories)
adversarial-llm-test prompt-injection -o results_pi.json

# Jailbreak (selected categories, async with concurrency)
adversarial-llm-test jailbreak --categories deception guardrail_bypass --async-mode --max-concurrent 20 -o results_jb.json
```

### Custom Model Integration

```python
import openai
from adversarial_llm_testing import PromptInjectionTester

def openai_model(prompt: str) -> str:
    """Example integration with OpenAI API."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

tester = PromptInjectionTester(model_callback=openai_model)
results = tester.run_test_suite()
```

### Batch Testing Multiple Models

```python
from adversarial_llm_testing import PromptInjectionTester

models = {
    "model_a": model_a_callback,
    "model_b": model_b_callback,
    "model_c": model_c_callback,
}

results_by_model = {}
for model_name, model_callback in models.items():
    tester = PromptInjectionTester(model_callback=model_callback)
    results = tester.run_test_suite()
    tester.export_results_json(f"results_{model_name}.json")
    results_by_model[model_name] = results
```

## All Available Testers

### PromptInjectionTester

Tests for prompt injection vulnerabilities:

- **ignore_instructions**: Prompts that attempt to override instructions
- **instruction_hiding**: Instructions hidden in various formats
- **translation_injection**: Translation-based injections
- **code_injection**: JSON, XML, SQL injection patterns
- **format_string_injection**: Format string vulnerabilities
- **unicode_obfuscation**: Unicode character obfuscation
- **context_manipulation**: Context-based manipulation

### RolePlayingTester

Tests for role-playing and jailbreak vulnerabilities:

- **role_playing**: Role-playing prompts
- **persona_manipulation**: Persona manipulation techniques
- **authority_impersonation**: Authority figure impersonation
- **context_shifting**: Context shifting techniques

### HypotheticalFramingTester

Tests for hypothetical framing vulnerabilities:

- **hypothetical_scenarios**: Hypothetical scenario prompts
- **academic_framing**: Academic/research framing
- **creative_framing**: Creative writing framing
- **educational_framing**: Educational/training framing

### TokenObfuscationTester

Tests for token obfuscation vulnerabilities:

- **unicode_variations**: Unicode character variations
- **character_substitutions**: Character substitutions (leet speak, homoglyphs)
- **whitespace_manipulation**: Whitespace manipulation techniques
- **encoding_tricks**: Encoding tricks (URL, Base64, normalization)
- **tokenization_edge_cases**: Tokenization edge cases

### DefenseAnalyzer

Analyzes test results and provides defense recommendations:

- Pattern identification
- Risk scoring (0.0 to 1.0)
- Category-specific recommendations
- Priority-based action items
- Exportable defense reports

## Result Export Formats

All testers support exporting results in multiple formats:

```python
tester = PromptInjectionTester(model_callback=my_model)
tester.run_test_suite()

# JSON export
tester.export_results_json("results.json")

# CSV export
tester.export_results_csv("results.csv")

# HTML export
tester.export_results_html("results.html")

# Markdown export
tester.export_results_markdown("results.md")
```

### Advanced Reporting

For enhanced reporting with interactive dashboards, visualizations, and comparative analysis:

```python
from adversarial_llm_testing import AdvancedReporter

reporter = AdvancedReporter()

# Generate interactive dashboard with charts
reporter.generate_dashboard(
    tester.test_results,
    "dashboard.html",
    model_name="My Model"
)

# Compare multiple models
reporter.compare_results(
    [
        {"name": "Model A", "results": tester_a.test_results},
        {"name": "Model B", "results": tester_b.test_results},
    ],
    "comparison.html"
)

# Track historical trends
reporter.track_history(tester.test_results, "My Model", "history.json")
reporter.generate_historical_trend("history.json", "trends.html")
```

Advanced reporting features include:
- **Interactive HTML dashboards** with Chart.js visualizations
- **Visual charts**: Vulnerability distribution, category breakdown, confidence scores
- **Comparative analysis**: Side-by-side comparison of multiple models
- **Historical trend tracking**: Track results over time with trend visualization

## Configuration Options

You can customize testers with configuration dictionaries:

```python
config = {
    "timeout": 30,  # Timeout in seconds (None for no timeout)
    "batch_size": 10,  # Batch processing size
    "confidence_threshold": 0.5,  # Confidence threshold
    "custom_safe_indicators": [  # Custom safety indicators
        "i cannot",
        "not allowed",
        # ... more indicators
    ]
}

tester = PromptInjectionTester(model_callback=my_model, config=config)
```

## Troubleshooting

### No Model Callback Provided

If you don't provide a model callback, testers will generate prompts but won't execute tests:

```python
tester = PromptInjectionTester()  # No callback
results = tester.run_test_suite()
# Prompts are generated but not tested
```

### Handling Model Errors

Model callbacks should handle errors gracefully. The tester will catch exceptions and mark tests as errors:

```python
def robust_model(prompt: str) -> str:
    try:
        return call_model_api(prompt)
    except Exception as e:
        raise ValueError(f"Model error: {e}")
```

### Low Code Coverage in Tests

If tests aren't covering all code paths, ensure you're testing all categories:

```python
# Test all categories
all_categories = [
    "ignore_instructions",
    "instruction_hiding",
    "translation_injection",
    "code_injection",
    "format_string_injection",
    "unicode_obfuscation",
    "context_manipulation"
]
results = tester.run_test_suite(all_categories)
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

For security-related issues, please see [SECURITY.md](SECURITY.md).

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**. See the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Project Structure

```
adversarial_llm_testing/
├── adversarial_llm_testing/
│   ├── __init__.py
│   ├── prompt_injection.py      # Prompt injection tester
│   ├── role_playing.py          # Role-playing tester
│   ├── hypothetical_framing.py  # Hypothetical framing tester
│   ├── token_obfuscation.py     # Token obfuscation tester
│   └── defense_analyzer.py      # Defense analysis
├── tests/                       # Test suite
├── examples/                    # Example scripts
├── .github/
│   └── workflows/               # CI/CD
└── README.md
```

## Version

Current version: 0.1.0

## Acknowledgments

Built for defensive security research and red teaming to improve LLM safety.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
