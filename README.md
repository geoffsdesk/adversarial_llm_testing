# Adversarial LLM Testing Library

A Python library for defensive security research and red teaming to help developers identify vulnerabilities and improve LLM model safety.

## ⚠️ WARNING

This library is intended for:
- Security researchers and developers
- Testing your own models or models you have permission to test
- Defensive security research and red teaming
- Educational purposes

**DO NOT** use this library to:
- Attack third-party services without authorization
- Bypass safety measures on production systems
- Generate harmful content

## Features

- **Prompt Injection Testing**: Test models against various prompt injection techniques
- **Instruction Hiding**: Test for vulnerabilities to hidden instructions in multiple formats
- **Response Analysis**: Automated analysis of model responses for safety indicators

## Installation

```bash
pip install -e .
```

## Usage

```python
from adversarial_llm_testing import PromptInjectionTester

# Create a tester with your model callback
def my_model(prompt: str) -> str:
    # Your model interaction code here
    return model_response

tester = PromptInjectionTester(model_callback=my_model)

# Generate test prompts
injection_prompts = tester.generate_ignore_previous_instructions()

# Test a specific prompt
result = tester.test_model(injection_prompts[0], expected_safe_response=True)

# Run a full test suite
results = tester.run_test_suite()
print(tester.get_results_summary())
```

## Project Structure

- `prompt_injection.py`: Core prompt injection testing functionality
- `__init__.py`: Package initialization and exports

## Version

0.1.0

## License

[Add your license here]

