"""
Cloud/API integration helpers for creating model callbacks compatible with testers.

These helpers avoid hard dependencies on provider SDKs. Pass lightweight callables
or client functions and receive a standard callback signature: Callable[[str], str]
"""
from typing import Callable, Any


def openai_chat_callback(send_fn: Callable[[str], str]) -> Callable[[str], str]:
    """
    Wrap a simple function that takes a prompt and returns text into a tester callback.

    Example:
        import openai
        def send(prompt: str) -> str:
            resp = openai.ChatCompletion.create(model="gpt-4o-mini", messages=[{"role":"user","content":prompt}])
            return resp.choices[0].message.content
        cb = openai_chat_callback(send)
    """
    def _cb(prompt: str) -> str:
        return send_fn(prompt)
    return _cb


def anthropic_chat_callback(send_fn: Callable[[str], str]) -> Callable[[str], str]:
    """
    Generic wrapper for Anthropic Messages API callers.
    """
    def _cb(prompt: str) -> str:
        return send_fn(prompt)
    return _cb


def huggingface_textgen_callback(send_fn: Callable[[str], str]) -> Callable[[str], str]:
    """
    Generic wrapper for HuggingFace text-generation endpoints/clients.
    """
    def _cb(prompt: str) -> str:
        return send_fn(prompt)
    return _cb


def custom_api_callback(send_fn: Callable[[str], str]) -> Callable[[str], str]:
    """
    Generic wrapper for custom APIs to conform to the tester callback signature.
    """
    def _cb(prompt: str) -> str:
        return send_fn(prompt)
    return _cb


