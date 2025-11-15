# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-15

### Added

#### Core Features
- **PromptInjectionTester**: Core prompt injection testing functionality
  - Translation-based injection generation
  - Instruction hiding techniques
  - Code injection patterns (JSON, XML, SQL)
  - Format string injection
  - Unicode obfuscation
  - Multi-step injection attacks
  - Context manipulation techniques
  - Comprehensive test suite execution
  - Result export (JSON, CSV, HTML, Markdown)
  - Enhanced response safety analysis with confidence scoring
  - Configuration options for customizing tests

- **RolePlayingTester**: Role-playing and jailbreak testing
  - Role-playing prompt generation
  - Persona manipulation techniques
  - Authority impersonation
  - Context shifting techniques

- **HypotheticalFramingTester**: Hypothetical framing vulnerability testing
  - Hypothetical scenario prompts
  - Academic/research framing
  - Creative writing framing
  - Educational/training framing

- **TokenObfuscationTester**: Token obfuscation vulnerability testing
  - Unicode variations (Cyrillic, Greek, fullwidth, zero-width)
  - Character substitutions (leet speak, homoglyphs)
  - Whitespace manipulation
  - Encoding tricks (URL, Base64, Unicode normalization)
  - Tokenization edge cases

- **DefenseAnalyzer**: Test result analysis and defense recommendations
  - Pattern identification in vulnerabilities
  - Risk scoring (0.0 to 1.0)
  - Category-specific recommendations
  - Priority-based action items
  - Defense report generation (text, markdown, JSON)

#### Testing & Quality
- Comprehensive test suite with 62 tests
- 81% code coverage
- Unit tests for all testers
- Integration tests with mock callbacks
- Test fixtures and utilities

#### Code Quality
- Black code formatting configuration
- Flake8 linting configuration
- MyPy type checking configuration
- All code formatted and linted

#### CI/CD
- GitHub Actions workflow for testing
- Automated testing on Python 3.8-3.12
- Automated linting and type checking
- Code coverage reporting

#### Documentation
- Comprehensive README with usage examples
- Example scripts (basic, advanced, custom integration, batch testing, result analysis)
- Contributing guidelines (CONTRIBUTING.md)
- Security policy (SECURITY.md)
- Changelog (CHANGELOG.md)
- Project plan (PROJECT_PLAN.md)

#### Package Setup
- Proper Python package structure
- pyproject.toml with full metadata
- requirements.txt for dependencies
- MANIFEST.in for non-Python files
- Installable via pip

### Technical Details

- **Language**: Python 3.8+
- **Dependencies**: None (minimal runtime dependencies)
- **Test Framework**: pytest
- **Code Coverage**: 81%
- **License**: [To be added]

## [Unreleased]

### Planned Features
- Async support for parallel test execution
- Advanced reporting with visualizations
- CLI tool for running tests
- Additional injection techniques
- Model-specific adapters (OpenAI, Anthropic, HuggingFace)
- Pre-commit hooks
- Automated releases

## Version History

- **0.1.0** (2024-11-15): Initial release
  - Complete implementation of all 5 tester classes
  - Comprehensive test suite
  - CI/CD pipeline
  - Documentation and examples

---

[0.1.0]: https://github.com/geoffsdesk/adversarial_llm_testing/releases/tag/v0.1.0

