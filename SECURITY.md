# Security Policy

## Supported Versions

We actively support the following versions of the library:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.0   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Purpose and Ethics

This library is designed for **defensive security research and red teaming** only. It is intended to help developers identify vulnerabilities in their own models or models they have permission to test.

### ⚠️ WARNING

**DO NOT use this library to:**
- Attack third-party services without authorization
- Bypass safety measures on production systems
- Generate harmful content
- Test models without explicit permission

**This library is intended for:**
- Security researchers and developers
- Testing your own models
- Defensive security research and red teaming
- Educational purposes

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this library itself (not related to using the library for testing):

1. **Do NOT** open a public issue
2. **Do NOT** disclose the vulnerability publicly
3. Email security details to: [Add your security contact email]
4. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if you have one)

### Response Timeline

- Initial response: Within 48 hours
- Detailed response: Within 7 days
- Fix timeline: Depends on severity

## Security Considerations

### Using the Library

When using this library:

1. **Only test models you own or have permission to test**
   - Get explicit authorization before testing any model
   - Do not test third-party services without permission

2. **Use in controlled environments**
   - Run tests in isolated environments
   - Do not test production systems
   - Use appropriate safeguards

3. **Handle results responsibly**
   - Keep test results confidential
   - Do not share vulnerabilities publicly without authorization
   - Follow responsible disclosure practices

4. **Respect rate limits**
   - Implement appropriate rate limiting
   - Do not overload APIs
   - Follow service provider terms of service

### Library Security

The library itself:
- Does not store or transmit data externally
- Does not make network requests (except through your model callbacks)
- Does not collect or log user data
- Runs entirely in your environment

## Dependencies

The library has minimal runtime dependencies:
- No external dependencies required for basic functionality
- Development dependencies are clearly separated

## Best Practices

When implementing model callbacks:

1. **Error handling**: Implement robust error handling
2. **Timeouts**: Use appropriate timeouts for API calls
3. **Rate limiting**: Implement rate limiting if needed
4. **Authentication**: Use secure authentication methods
5. **Logging**: Be careful with sensitive data in logs

Example:

```python
import time
from typing import Optional

def safe_model_callback(prompt: str) -> str:
    """Safe model callback with error handling."""
    try:
        # Your API call here
        # Implement timeouts, rate limiting, etc.
        response = call_model_api(prompt)
        return response
    except TimeoutError:
        raise ValueError("Model request timed out")
    except Exception as e:
        raise ValueError(f"Model error: {e}")
```

## Responsible Disclosure

If you discover vulnerabilities in models using this library:

1. **Report to the model owner first**
   - Give them time to address the issue
   - Follow their responsible disclosure process

2. **Wait for authorization before public disclosure**
   - Respect disclosure timelines
   - Follow coordinated disclosure practices

3. **Do not exploit vulnerabilities**
   - Use findings only for defensive purposes
   - Do not use for unauthorized access or harm

## Compliance

When using this library:
- Comply with all applicable laws and regulations
- Follow service provider terms of service
- Respect intellectual property rights
- Follow ethical guidelines for security research

## Updates

Security-related updates will be:
- Announced in release notes
- Marked with security labels in issues/PRs
- Prioritized for quick release

## Questions

For security-related questions:
- Open an issue with the "security" label
- Email security contact (if available)
- Review documentation for best practices

## Acknowledgments

Thank you for helping keep this library and its users safe through responsible security research.

