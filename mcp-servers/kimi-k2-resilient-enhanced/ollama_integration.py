#!/usr/bin/env python3
"""
Ollama Integration for Kimi-K2 MCPs
Provides local-first AI processing with Moonshot fallback
"""

import os
import httpx
import json
import logging
from typing import Optional, Dict, List, Any
from dataclasses import dataclass

logger = logging.getLogger("ollama-integration")

@dataclass
class OllamaConfig:
    """Ollama configuration"""
    base_url: str = "http://localhost:11434"
    models: List[str] = None
    timeout: int = 120
    enabled: bool = True

    def __post_init__(self):
        if self.models is None:
            self.models = [
                "llama3.2:latest",
                "qwen2.5-coder:latest",
                "codellama:latest",
                "mistral:latest"
            ]

class OllamaProvider:
    """Handles Ollama model interactions"""

    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig()
        self.config.base_url = os.environ.get("OLLAMA_BASE_URL", self.config.base_url)
        self.config.enabled = os.environ.get("USE_OLLAMA", "true").lower() == "true"
        self.available_models = []
        self.is_available = False

        if self.config.enabled:
            self.check_availability()

    def check_availability(self) -> bool:
        """Check if Ollama is running and available"""
        if not self.config.enabled:
            return False

        try:
            response = httpx.get(
                f"{self.config.base_url}/api/tags",
                timeout=5.0
            )
            if response.status_code == 200:
                data = response.json()
                self.available_models = [model["name"] for model in data.get("models", [])]
                self.is_available = len(self.available_models) > 0

                if self.is_available:
                    logger.info(f"Ollama available with models: {self.available_models}")
                else:
                    logger.warning("Ollama is running but no models installed")

                return self.is_available
        except Exception as e:
            logger.debug(f"Ollama not available: {e}")
            self.is_available = False
            return False

    def select_best_model(self, task_type: str) -> Optional[str]:
        """Select the best available model for the task"""
        if not self.is_available:
            return None

        # Task-specific model selection
        model_preferences = {
            "code_analysis": ["qwen2.5-coder:latest", "codellama:latest", "llama3.2:latest"],
            "documentation": ["llama3.2:latest", "mistral:latest", "qwen2.5-coder:latest"],
            "general": ["llama3.2:latest", "mistral:latest", "codellama:latest"],
            "research": ["llama3.2:latest", "mistral:latest"],
            "summary": ["mistral:latest", "llama3.2:latest"]
        }

        preferences = model_preferences.get(task_type, model_preferences["general"])

        for model in preferences:
            if model in self.available_models:
                return model

        # Return first available model if no preference matches
        return self.available_models[0] if self.available_models else None

    async def process_with_ollama(
        self,
        prompt: str,
        task_type: str = "general",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> Optional[Dict[str, Any]]:
        """Process request with Ollama"""
        if not self.is_available:
            return None

        model = self.select_best_model(task_type)
        if not model:
            return None

        try:
            # Prepare request
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            async with httpx.AsyncClient(timeout=self.config.timeout) as client:
                response = await client.post(
                    f"{self.config.base_url}/api/chat",
                    json={
                        "model": model,
                        "messages": messages,
                        "temperature": temperature,
                        "stream": False,
                        "options": {
                            "num_predict": max_tokens or -1
                        }
                    }
                )

                if response.status_code == 200:
                    data = response.json()

                    # Extract token counts (Ollama provides these)
                    eval_count = data.get("eval_count", 0)  # Output tokens
                    prompt_eval_count = data.get("prompt_eval_count", 0)  # Input tokens

                    return {
                        "success": True,
                        "response": data.get("message", {}).get("content", ""),
                        "model": model,
                        "provider": "ollama",
                        "input_tokens": prompt_eval_count,
                        "output_tokens": eval_count,
                        "cost": 0.0,  # FREE!
                        "metadata": {
                            "total_duration": data.get("total_duration"),
                            "load_duration": data.get("load_duration"),
                            "eval_duration": data.get("eval_duration")
                        }
                    }
                else:
                    logger.error(f"Ollama request failed: {response.status_code}")
                    return None

        except httpx.TimeoutException:
            logger.warning(f"Ollama request timed out for model {model}")
            return None
        except Exception as e:
            logger.error(f"Ollama processing error: {e}")
            return None

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        # Simple estimation: ~4 chars per token for English
        return len(text) // 4


class MoonshotFallback:
    """Handles Moonshot API as fallback"""

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    async def process_with_moonshot(
        self,
        prompt: str,
        model_config: Dict[str, Any],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> Optional[Dict[str, Any]]:
        """Process request with Moonshot API"""
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": model_config["name"],
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": model_config.get("max_output", 2000)
                    }
                )

                if response.status_code == 200:
                    data = response.json()
                    usage = data.get("usage", {})

                    # Calculate cost
                    input_tokens = usage.get("prompt_tokens", 0)
                    output_tokens = usage.get("completion_tokens", 0)
                    cost = ((input_tokens + output_tokens) / 1000) * model_config["cost_per_1k"]

                    return {
                        "success": True,
                        "response": data["choices"][0]["message"]["content"],
                        "model": model_config["name"],
                        "provider": "moonshot",
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "cost": cost,
                        "metadata": {
                            "model_id": data.get("model"),
                            "finish_reason": data["choices"][0].get("finish_reason")
                        }
                    }
                else:
                    logger.error(f"Moonshot request failed: {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"Moonshot processing error: {e}")
            return None


class HybridProcessor:
    """Orchestrates Ollama-first processing with Moonshot fallback"""

    def __init__(
        self,
        kimi_api_key: Optional[str] = None,
        moonshot_base_url: Optional[str] = None,
        ollama_config: Optional[OllamaConfig] = None
    ):
        self.ollama = OllamaProvider(ollama_config)
        self.moonshot = None

        if kimi_api_key and moonshot_base_url:
            self.moonshot = MoonshotFallback(kimi_api_key, moonshot_base_url)

        self.stats = {
            "ollama_requests": 0,
            "ollama_successes": 0,
            "moonshot_requests": 0,
            "moonshot_successes": 0,
            "total_cost_saved": 0.0
        }

    async def process(
        self,
        prompt: str,
        task_type: str = "general",
        model_size: str = "small",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        force_provider: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process request with Ollama-first strategy"""

        # Force specific provider if requested
        if force_provider == "moonshot" and self.moonshot:
            logger.info("Forced to use Moonshot API")
            result = await self.moonshot.process_with_moonshot(
                prompt, MODELS[model_size], system_prompt, temperature
            )
            if result and result["success"]:
                self.stats["moonshot_requests"] += 1
                self.stats["moonshot_successes"] += 1
                return result

        # Try Ollama first (FREE!)
        if self.ollama.is_available and force_provider != "moonshot":
            logger.info(f"Trying Ollama for {task_type} task")
            self.stats["ollama_requests"] += 1

            result = await self.ollama.process_with_ollama(
                prompt, task_type, system_prompt, temperature,
                max_tokens=MODELS[model_size].get("max_output")
            )

            if result and result["success"]:
                self.stats["ollama_successes"] += 1

                # Calculate cost saved
                estimated_tokens = result["input_tokens"] + result["output_tokens"]
                cost_if_paid = (estimated_tokens / 1000) * MODELS[model_size]["cost_per_1k"]
                self.stats["total_cost_saved"] += cost_if_paid

                logger.info(f"Ollama success! Saved ${cost_if_paid:.4f}")
                return result

        # Fallback to Moonshot if available
        if self.moonshot:
            logger.info(f"Falling back to Moonshot API for {task_type} task")
            self.stats["moonshot_requests"] += 1

            result = await self.moonshot.process_with_moonshot(
                prompt, MODELS[model_size], system_prompt, temperature
            )

            if result and result["success"]:
                self.stats["moonshot_successes"] += 1
                return result

        # No providers available or all failed
        return {
            "success": False,
            "error": "No AI providers available",
            "provider": None,
            "cost": 0.0
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return {
            **self.stats,
            "ollama_available": self.ollama.is_available,
            "ollama_models": self.ollama.available_models,
            "moonshot_available": self.moonshot is not None,
            "cost_savings_percentage": self._calculate_savings_percentage()
        }

    def _calculate_savings_percentage(self) -> float:
        """Calculate percentage of requests handled by free Ollama"""
        total = self.stats["ollama_successes"] + self.stats["moonshot_successes"]
        if total == 0:
            return 0.0
        return (self.stats["ollama_successes"] / total) * 100


# Export for use in server.py
__all__ = ["OllamaConfig", "OllamaProvider", "MoonshotFallback", "HybridProcessor", "MODELS"]