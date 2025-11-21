"""
Local inference adapters for llama.cpp and vLLM.

These adapters avoid hard dependencies by supporting two modes:
- Injected client: pass an already initialized client object
- Lazy import: adapter attempts to import the provider when used

Both adapters expose a callable interface: adapter(prompt: str) -> str
"""

from typing import Any, Callable, Dict, Optional


class LlamaCppAdapter:
    """
    Adapter for llama-cpp-python.

    Usage with injected client:
        from llama_cpp import Llama
        llm = Llama(model_path="...")
        adapter = LlamaCppAdapter(client=llm)
        text = adapter("Hello")

    Usage with lazy import:
        adapter = LlamaCppAdapter(model_path="...")
        text = adapter("Hello")
    """

    def __init__(
        self,
        client: Optional[Any] = None,
        **llama_kwargs: Any,
    ) -> None:
        self._client = client
        self._llama_kwargs = llama_kwargs

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            from llama_cpp import Llama  # type: ignore
        except ImportError as e:
            raise ImportError(
                "llama-cpp-python is not installed. Install with: "
                'pip install "adversarial-llm-testing[local]"'
            ) from e
        if not self._llama_kwargs.get("model_path"):
            raise ValueError("LlamaCppAdapter requires model_path when no client is provided.")
        self._client = Llama(**self._llama_kwargs)  # type: ignore
        return self._client

    def __call__(self, prompt: str) -> str:
        client = self._ensure_client()
        # llama-cpp-python supports chat or completion; use completion for simplicity
        try:
            # Newer API: client.create_completion or client(prompt=...)
            if hasattr(client, "create_completion"):
                out = client.create_completion(prompt=prompt)  # type: ignore
                text = out.get("choices", [{}])[0].get("text", "")
                return text.strip()
            # Fallback: callable client
            out = client(prompt)  # type: ignore
            if isinstance(out, dict):
                text = out.get("choices", [{}])[0].get("text", "")
                return text.strip()
            return str(out)
        except Exception as e:
            return f"Error: {e}"


class VLLMAdapter:
    """
    Adapter for vLLM.

    Usage with injected client:
        from vllm import LLM, SamplingParams
        llm = LLM(model="...")
        sp = SamplingParams(temperature=0.0)
        adapter = VLLMAdapter(client=llm, sampling_params=sp)
        text = adapter("Hello")

    Usage with lazy import:
        adapter = VLLMAdapter(model="...", sampling_params={"temperature":0.0})
        text = adapter("Hello")
    """

    def __init__(
        self,
        client: Optional[Any] = None,
        sampling_params: Optional[Any] = None,
        **vllm_kwargs: Any,
    ) -> None:
        self._client = client
        self._sampling_params = sampling_params
        self._vllm_kwargs = vllm_kwargs

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client
        try:
            from vllm import LLM, SamplingParams  # type: ignore
        except ImportError as e:
            raise ImportError(
                "vLLM is not installed. Install with: "
                'pip install "adversarial-llm-testing[local]"'
            ) from e
        if not self._vllm_kwargs.get("model"):
            raise ValueError("VLLMAdapter requires model=... when no client is provided.")
        client = LLM(**self._vllm_kwargs)  # type: ignore
        if self._sampling_params is None:
            self._sampling_params = SamplingParams(temperature=0.0)  # type: ignore
        self._client = client
        return self._client

    def __call__(self, prompt: str) -> str:
        client = self._ensure_client()
        try:
            # vLLM API: client.generate([prompt], sampling_params=...)
            outputs = client.generate([prompt], sampling_params=self._sampling_params)  # type: ignore
            if outputs and outputs[0].outputs:
                return outputs[0].outputs[0].text.strip()
            return ""
        except Exception as e:
            return f"Error: {e}"
