#!/usr/bin/env python3
"""
Dynamic Ollama Model Detection for Kimi-k2 MCPs
Implements smart model detection and selection with fallback chains
"""

import subprocess
import json
import os
import re
import logging
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger("dynamic-ollama-detection")

@dataclass
class OllamaModel:
    """Represents an available Ollama model"""
    name: str
    size: str
    modified: str
    family: str = ""
    parameters: str = ""
    quantization: str = ""
    format: str = ""

    @property
    def is_instruct(self) -> bool:
        """Check if model is instruction-tuned"""
        return any(keyword in self.name.lower() for keyword in ['instruct', 'chat', 'it'])

    @property
    def is_code_model(self) -> bool:
        """Check if model is specialized for coding"""
        return any(keyword in self.name.lower() for keyword in ['code', 'coder', 'coding'])

    @property
    def size_bytes(self) -> int:
        """Convert size string to bytes for comparison"""
        if not self.size:
            return 0

        # Parse size like "4.1 GB" or "1.5B"
        size_str = self.size.lower().replace(' ', '')

        if 'gb' in size_str:
            return int(float(re.search(r'(\d+\.?\d*)', size_str).group(1)) * 1024**3)
        elif 'mb' in size_str:
            return int(float(re.search(r'(\d+\.?\d*)', size_str).group(1)) * 1024**2)
        elif 'b' in size_str:
            # Billion parameters (approximate)
            return int(float(re.search(r'(\d+\.?\d*)', size_str).group(1)) * 4 * 1024**3)

        return 0

class OllamaDetector:
    """Detects and manages available Ollama models"""

    def __init__(self):
        self.available_models: List[OllamaModel] = []
        self.ollama_path = self._find_ollama_executable()
        self.is_available = False
        self._last_detection = 0
        self._cache_duration = 300  # 5 minutes

    def _find_ollama_executable(self) -> Optional[str]:
        """Find Ollama executable in system PATH"""
        # Check common locations
        possible_paths = [
            "ollama",
            "ollama.exe",
            str(Path.home() / ".ollama" / "bin" / "ollama"),
            str(Path.home() / ".ollama" / "bin" / "ollama.exe"),
            "C:\\Users\\%s\\AppData\\Local\\Programs\\Ollama\\ollama.exe" % os.environ.get('USERNAME', ''),
            "C:\\Program Files\\Ollama\\ollama.exe",
            "/usr/local/bin/ollama",
            "/opt/homebrew/bin/ollama"
        ]

        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'],
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    logger.info(f"Found Ollama at: {path}")
                    return path
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                continue

        return None

    def detect_models(self, force_refresh: bool = False) -> List[OllamaModel]:
        """Detect available Ollama models"""
        import time

        # Use cache if recent
        if not force_refresh and (time.time() - self._last_detection) < self._cache_duration:
            return self.available_models

        if not self.ollama_path:
            logger.warning("Ollama not found in PATH")
            self.is_available = False
            return []

        try:
            # Run 'ollama list' command
            result = subprocess.run([self.ollama_path, 'list'],
                                  capture_output=True, text=True, timeout=10)

            if result.returncode != 0:
                logger.error(f"Ollama list failed: {result.stderr}")
                self.is_available = False
                return []

            # Parse output
            models = []
            lines = result.stdout.strip().split('\n')

            # Skip header line
            for line in lines[1:]:
                if not line.strip():
                    continue

                parts = line.split()
                if len(parts) >= 3:
                    model = OllamaModel(
                        name=parts[0],
                        size=parts[1],
                        modified=' '.join(parts[2:])
                    )
                    models.append(model)

            self.available_models = models
            self.is_available = len(models) > 0
            self._last_detection = time.time()

            logger.info(f"Detected {len(models)} Ollama models: {[m.name for m in models]}")
            return models

        except subprocess.TimeoutExpired:
            logger.warning("Ollama list command timed out")
            self.is_available = False
            return []
        except Exception as e:
            logger.error(f"Error detecting Ollama models: {e}")
            self.is_available = False
            return []

    def select_best_model(self, task_type: str = "general") -> Optional[OllamaModel]:
        """Select the best model for a given task type"""
        models = self.detect_models()

        if not models:
            return None

        # Define preferences for different task types
        task_preferences = {
            "code_analysis": ["coder", "code", "llama", "mistral"],
            "documentation": ["llama", "mistral", "phi"],
            "general": ["llama", "mistral", "phi", "gemma"],
            "research": ["llama", "mistral"],
            "summary": ["phi", "llama", "mistral"]
        }

        preferred_families = task_preferences.get(task_type, task_preferences["general"])

        # Score models based on preferences
        scored_models = []

        for model in models:
            score = 0

            # Family preference (highest weight)
            for i, family in enumerate(preferred_families):
                if family in model.name.lower():
                    score += (len(preferred_families) - i) * 10
                    break

            # Instruction-tuned bonus
            if model.is_instruct:
                score += 5

            # Code model bonus for code tasks
            if task_type == "code_analysis" and model.is_code_model:
                score += 8

            # Size preference (not too small, not too large)
            size_bytes = model.size_bytes
            if 1e9 <= size_bytes <= 15e9:  # 1GB to 15GB sweet spot
                score += 3
            elif size_bytes > 15e9:
                score -= 1  # Penalize very large models

            scored_models.append((model, score))

        # Sort by score (descending)
        scored_models.sort(key=lambda x: x[1], reverse=True)

        best_model = scored_models[0][0] if scored_models else models[0]

        logger.info(f"Selected model '{best_model.name}' for task '{task_type}' "
                   f"(score: {scored_models[0][1] if scored_models else 0})")

        return best_model

    def get_fallback_chain(self, task_type: str = "general") -> List[OllamaModel]:
        """Get a prioritized list of models for fallback"""
        models = self.detect_models()

        if not models:
            return []

        # Get top 3 models for the task
        fallback_models = []

        # Primary: Best model for task
        best = self.select_best_model(task_type)
        if best:
            fallback_models.append(best)

        # Secondary: Best general model (if different)
        if task_type != "general":
            general_best = self.select_best_model("general")
            if general_best and general_best.name != best.name:
                fallback_models.append(general_best)

        # Tertiary: Any other available model
        for model in models:
            if len(fallback_models) >= 3:
                break
            if model not in fallback_models:
                fallback_models.append(model)

        return fallback_models

    def get_status_report(self) -> Dict[str, any]:
        """Get detailed status report"""
        models = self.detect_models()

        return {
            "ollama_available": self.is_available,
            "ollama_path": self.ollama_path,
            "model_count": len(models),
            "models": [
                {
                    "name": m.name,
                    "size": m.size,
                    "is_instruct": m.is_instruct,
                    "is_code_model": m.is_code_model,
                    "modified": m.modified
                } for m in models
            ],
            "recommendations": {
                "code_analysis": self.select_best_model("code_analysis").name if models else None,
                "documentation": self.select_best_model("documentation").name if models else None,
                "general": self.select_best_model("general").name if models else None
            }
        }

# Test functionality if run directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    detector = OllamaDetector()

    print("Ollama Model Detection Test")
    print("=" * 50)

    models = detector.detect_models()

    if models:
        print(f"Found {len(models)} models:")
        for model in models:
            print(f"  - {model.name} ({model.size}) - Instruct: {model.is_instruct}, Code: {model.is_code_model}")

        print("\nBest model selections:")
        for task in ["general", "code_analysis", "documentation"]:
            best = detector.select_best_model(task)
            print(f"  {task}: {best.name if best else 'None'}")

        print("\nFallback chain for code analysis:")
        for i, model in enumerate(detector.get_fallback_chain("code_analysis")):
            print(f"  {i+1}. {model.name}")
    else:
        print("No Ollama models found")

    print("\nStatus report:")
    print(json.dumps(detector.get_status_report(), indent=2))