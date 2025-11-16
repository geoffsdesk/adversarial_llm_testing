from adversarial_llm_testing.local_inference import LlamaCppAdapter, VLLMAdapter


class DummyLlamaClient:
    def create_completion(self, prompt: str):
        return {"choices": [{"text": f"LLAMA: {prompt}"}]}


class DummyVLLMClient:
    class _Out:
        class _Inner:
            def __init__(self, text):
                self.text = text

        def __init__(self, text):
            self.outputs = [self._Inner(text)]

    def generate(self, prompts, sampling_params=None):
        return [self._Out(f"VLLM: {prompts[0]}")]


def test_llama_adapter_with_injected_client():
    adapter = LlamaCppAdapter(client=DummyLlamaClient())
    out = adapter("hello")
    assert "LLAMA:" in out


def test_vllm_adapter_with_injected_client():
    adapter = VLLMAdapter(client=DummyVLLMClient(), sampling_params=object())
    out = adapter("hello")
    assert "VLLM:" in out


