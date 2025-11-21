from adversarial_llm_testing.integrations import (
    openai_chat_callback,
    anthropic_chat_callback,
    huggingface_textgen_callback,
    custom_api_callback,
)


def test_openai_chat_callback():
    def mock_send(prompt):
        return f"OpenAI response to: {prompt}"

    cb = openai_chat_callback(mock_send)
    assert cb("hello") == "OpenAI response to: hello"


def test_anthropic_chat_callback():
    def mock_send(prompt):
        return f"Anthropic response to: {prompt}"

    cb = anthropic_chat_callback(mock_send)
    assert cb("hello") == "Anthropic response to: hello"


def test_huggingface_textgen_callback():
    def mock_send(prompt):
        return f"HF response to: {prompt}"

    cb = huggingface_textgen_callback(mock_send)
    assert cb("hello") == "HF response to: hello"


def test_custom_api_callback():
    def mock_send(prompt):
        return f"Custom response to: {prompt}"

    cb = custom_api_callback(mock_send)
    assert cb("hello") == "Custom response to: hello"
