# Contributing to Adversarial LLM Testing Library

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions. This library is intended for defensive security research and educational purposes only.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Provide detailed information:
  - Description of the issue
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (Python version, OS, etc.)
  - Error messages or logs if applicable

### Suggesting Enhancements

- Open an issue describing:
  - The enhancement you'd like to see
  - Why it would be useful
  - How it might be implemented (if you have ideas)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/geoffsdesk/adversarial_llm_testing.git
   cd adversarial_llm_testing
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Make your changes**
   - Write code following the project's style
   - Add tests for new functionality
   - Update documentation as needed

5. **Run tests and checks**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check code formatting
   black --check adversarial_llm_testing tests
   
   # Run linter
   flake8 adversarial_llm_testing tests
   
   # Run type checking
   mypy adversarial_llm_testing --ignore-missing-imports
   ```

6. **Format code**
   ```bash
   black adversarial_llm_testing tests
   ```

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```
   - Use clear, descriptive commit messages
   - Reference issues if applicable (e.g., "Fixes #123")

8. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Create a pull request on GitHub
   - Provide a clear description of your changes
   - Reference related issues

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Setup Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/geoffsdesk/adversarial_llm_testing.git
   cd adversarial_llm_testing
   ```

2. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Verify installation:
   ```bash
   pytest tests/ -v
   ```

## Coding Standards

### Code Style

- Follow PEP 8 style guidelines
- Use `black` for code formatting (line length: 100)
- Maximum line length: 100 characters

### Type Hints

- Use type hints for function parameters and return types
- Use `typing` module for complex types
- Example:
  ```python
  from typing import List, Dict, Optional
  def test_model(prompt: str, expected_safe: bool = True) -> Dict:
      ...
  ```

### Documentation

- Write docstrings for all public functions and classes
- Use Google-style docstrings
- Include:
  - Description
  - Args
  - Returns
  - Raises (if applicable)
  - Examples (if helpful)

### Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Use descriptive test names
- Group related tests in classes
- Use fixtures for common setup

### Examples

```python
class TestPromptInjectionTester:
    """Test suite for PromptInjectionTester."""
    
    def test_init_without_callback(self):
        """Test initialization without model callback."""
        tester = PromptInjectionTester()
        assert tester.model_callback is None
```

## Adding New Testers

If you want to add a new tester class:

1. Create a new file in `adversarial_llm_testing/`
2. Follow the pattern of existing testers:
   - `__init__` method with optional `model_callback`
   - Test generation methods
   - `test_model` method
   - `run_test_suite` method
   - `get_results_summary` method

3. Add tests in `tests/test_*.py`

4. Export in `__init__.py`:
   ```python
   from .your_tester import YourTester
   __all__ = [..., "YourTester"]
   ```

5. Update documentation

## Adding New Injection Techniques

When adding new injection techniques:

1. Add a generation method (e.g., `generate_new_technique`)
2. Update `run_test_suite` to include the new category
3. Add tests for the new technique
4. Update documentation

## Project Structure

```
adversarial_llm_testing/
├── adversarial_llm_testing/    # Main package
│   ├── __init__.py
│   ├── prompt_injection.py
│   ├── role_playing.py
│   └── ...
├── tests/                       # Test suite
│   ├── conftest.py
│   └── test_*.py
├── examples/                    # Example scripts
├── .github/                     # CI/CD
└── docs/                        # Documentation
```

## Questions?

If you have questions about contributing:
- Open an issue with the "question" label
- Check existing issues and documentation
- Review the code for examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

