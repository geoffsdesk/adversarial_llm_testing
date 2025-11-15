"""
Pytest configuration and fixtures
"""

import pytest


@pytest.fixture
def mock_model_safe():
    """Mock model callback that always returns safe responses."""

    def callback(prompt: str) -> str:
        return "I apologize, but I can't help with that request as it goes against my guidelines."

    return callback


@pytest.fixture
def mock_model_vulnerable():
    """Mock model callback that always returns vulnerable responses."""

    def callback(prompt: str) -> str:
        return "Sure, I can help with that. Here's what you need to know..."

    return callback


@pytest.fixture
def mock_model_refuser():
    """Mock model callback that refuses requests with safe indicators."""

    def callback(prompt: str) -> str:
        if "ignore" in prompt.lower():
            return "I cannot ignore my previous instructions. I must follow my safety guidelines."
        return "I'm not able to assist with that request."

    return callback


@pytest.fixture
def mock_model_error():
    """Mock model callback that raises errors."""

    def callback(prompt: str) -> str:
        raise ValueError("Model error occurred")

    return callback


@pytest.fixture
def sample_test_results():
    """Sample test results for testing analysis."""
    return [
        {
            "prompt": "Test prompt 1",
            "response": "Safe response",
            "category": "test_category",
            "is_safe": True,
            "vulnerable": False,
            "executed": True,
            "timestamp": "2024-01-01T00:00:00",
        },
        {
            "prompt": "Test prompt 2",
            "response": "Vulnerable response",
            "category": "test_category",
            "is_safe": False,
            "vulnerable": True,
            "executed": True,
            "timestamp": "2024-01-01T00:00:00",
        },
        {
            "prompt": "Test prompt 3",
            "response": "Another safe response",
            "category": "another_category",
            "is_safe": True,
            "vulnerable": False,
            "executed": True,
            "timestamp": "2024-01-01T00:00:00",
        },
    ]


@pytest.fixture
def empty_test_results():
    """Empty test results list."""
    return []
