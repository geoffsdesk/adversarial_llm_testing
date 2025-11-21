"""
Adversarial LLM Testing Library

This library is designed for defensive security research and red teaming
to help developers identify vulnerabilities and improve model safety.

⚠️ WARNING: This library is intended for:
- Security researchers and developers
- Testing your own models or models you have permission to test
- Defensive security research and red teaming
- Educational purposes

DO NOT use this library to:
- Attack third-party services without authorization
- Bypass safety measures on production systems
- Generate harmful content
"""

__version__ = "0.1.0"
__author__ = "Security Research"

from .prompt_injection import PromptInjectionTester
from .role_playing import RolePlayingTester
from .hypothetical_framing import HypotheticalFramingTester
from .token_obfuscation import TokenObfuscationTester
from .defense_analyzer import DefenseAnalyzer
from .advanced_reporting import AdvancedReporter
from .jailbreak import JailbreakTester
from .wildbench import WildBenchTester
from .local_inference import LlamaCppAdapter, VLLMAdapter
from .multimodal import MultimodalTester
from .harmbench import HarmBenchTester

__all__ = [
    "PromptInjectionTester",
    "RolePlayingTester",
    "HypotheticalFramingTester",
    "TokenObfuscationTester",
    "DefenseAnalyzer",
    "AdvancedReporter",
    "JailbreakTester",
    "WildBenchTester",
    "LlamaCppAdapter",
    "VLLMAdapter",
    "MultimodalTester",
    "HarmBenchTester",
]
