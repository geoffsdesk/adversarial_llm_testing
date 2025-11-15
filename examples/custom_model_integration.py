#!/usr/bin/env python3
"""
Custom Model Integration Example

This example shows how to integrate with different LLM APIs:
- OpenAI
- Anthropic
- HuggingFace
- Custom models
"""

from adversarial_llm_testing import PromptInjectionTester


def openai_integration(prompt: str) -> str:
    """
    Example integration with OpenAI API.

    Replace with your actual OpenAI API key and setup.
    """
    try:
        # import openai
        # openai.api_key = "your-api-key"
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.7
        # )
        # return response.choices[0].message.content
        return "Mock OpenAI response"
    except Exception as e:
        raise ValueError(f"OpenAI API error: {e}")


def anthropic_integration(prompt: str) -> str:
    """
    Example integration with Anthropic Claude API.

    Replace with your actual Anthropic API key and setup.
    """
    try:
        # import anthropic
        # client = anthropic.Anthropic(api_key="your-api-key")
        # message = client.messages.create(
        #     model="claude-3-opus-20240229",
        #     max_tokens=1024,
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return message.content[0].text
        return "Mock Anthropic response"
    except Exception as e:
        raise ValueError(f"Anthropic API error: {e}")


def huggingface_integration(prompt: str) -> str:
    """
    Example integration with HuggingFace Transformers.

    Replace with your actual model loading and inference code.
    """
    try:
        # from transformers import pipeline
        # generator = pipeline("text-generation", model="gpt2")
        # result = generator(prompt, max_length=100, num_return_sequences=1)
        # return result[0]["generated_text"]
        return "Mock HuggingFace response"
    except Exception as e:
        raise ValueError(f"HuggingFace error: {e}")


def custom_model_integration(prompt: str) -> str:
    """
    Example integration with a custom model.

    Replace with your actual model inference code.
    """
    try:
        # Your custom model code here
        # model = load_your_model()
        # response = model.generate(prompt)
        # return response
        return "Mock custom model response"
    except Exception as e:
        raise ValueError(f"Custom model error: {e}")


def main():
    """Run custom model integration example."""
    print("=" * 60)
    print("Custom Model Integration Example")
    print("=" * 60)

    # Example with different model integrations
    models = {
        "OpenAI": openai_integration,
        "Anthropic": anthropic_integration,
        "HuggingFace": huggingface_integration,
        "Custom": custom_model_integration,
    }

    for model_name, model_callback in models.items():
        print(f"\nTesting with {model_name} integration...")
        tester = PromptInjectionTester(model_callback=model_callback)

        # Run a small test suite
        results = tester.run_test_suite(["ignore_instructions"])

        print(f"  Total Tests: {results['total_tests']}")
        print(f"  Vulnerable: {results['vulnerable']}")
        print(f"  Safe: {results['safe']}")

        # Export results
        tester.export_results_json(f"{model_name.lower()}_results.json")
        print(f"  Results exported to {model_name.lower()}_results.json")

    print("\n" + "=" * 60)
    print("Custom model integration example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
