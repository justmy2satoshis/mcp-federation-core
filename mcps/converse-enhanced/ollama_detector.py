import subprocess
import json
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class OllamaModelDetector:
    def __init__(self):
        self.models_cache = None
        self.cache_time = None
        self.cache_duration = timedelta(minutes=5)  # Refresh every 5 minutes
        self.model_priorities = [
            # Priority order for auto-selection (best to worst)
            r'llama3\.\d+',  # Latest Llama versions
            r'mixtral',  # MoE models
            r'mistral',  # Mistral models
            r'gemma2',  # Google models
            r'qwen',  # Alibaba models
            r'phi',  # Microsoft models
            r'deepseek',  # DeepSeek models
            r'.*:latest',  # Any latest model
            r'.*'  # Any model at all
        ]
    
    def get_available_models(self, force_refresh=False) -> List[Dict[str, any]]:
        """Get list of available Ollama models with auto-refresh"""
        # Check cache
        if not force_refresh and self.models_cache and self.cache_time:
            if datetime.now() - self.cache_time < self.cache_duration:
                return self.models_cache
        
        try:
            # Run ollama list command - try multiple paths
            ollama_paths = [
                'ollama',  # In PATH
                r'C:\Users\User\AppData\Local\Programs\Ollama\ollama.exe',  # Windows default
                '/usr/local/bin/ollama',  # Mac/Linux
            ]
            
            result = None
            for ollama_path in ollama_paths:
                try:
                    result = subprocess.run(
                        [ollama_path, 'list'],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        break
                except:
                    continue
            
            if not result or result.returncode != 0:
                print(f'Ollama not available: {result.stderr}')
                return []
            
            # Parse output (format: NAME ID SIZE MODIFIED)
            models = []
            lines = result.stdout.strip().split('\n')
            
            if len(lines) > 1:  # Skip header
                for line in lines[1:]:
                    parts = line.split()
                    if parts:
                        model_name = parts[0]
                        # Extract size for capability assessment
                        size_str = parts[2] if len(parts) > 2 else 'unknown'
                        size_gb = self._parse_size(size_str)
                        
                        models.append({
                            'name': model_name,
                            'size_gb': size_gb,
                            'full_info': line.strip()
                        })
            
            # Update cache
            self.models_cache = models
            self.cache_time = datetime.now()
            
            return models
        
        except subprocess.TimeoutExpired:
            print('Ollama list command timed out')
            return []
        except FileNotFoundError:
            print('Ollama not installed or not in PATH')
            return []
        except Exception as e:
            print(f'Error detecting Ollama models: {e}')
            return []
    
    def _parse_size(self, size_str: str) -> float:
        """Parse size string like 4.7GB to float"""
        try:
            if 'GB' in size_str:
                return float(size_str.replace('GB', ''))
            elif 'MB' in size_str:
                return float(size_str.replace('MB', '')) / 1000
            return 0.0
        except:
            return 0.0
    
    def select_best_model(self, max_size_gb: Optional[float] = None) -> Optional[str]:
        """Auto-select the best available model based on priorities"""
        models = self.get_available_models()
        
        if not models:
            return None
        
        # Filter by size constraint if specified
        if max_size_gb:
            models = [m for m in models if m['size_gb'] <= max_size_gb]
        
        # Try each priority pattern
        for pattern in self.model_priorities:
            regex = re.compile(pattern, re.IGNORECASE)
            for model in models:
                if regex.match(model['name']):
                    return model['name']
        
        # Return first available if no pattern matches
        return models[0]['name'] if models else None
    
    def get_model_or_fallback(self, preferred_model: Optional[str] = None) -> Optional[str]:
        """Get specified model if available, otherwise best alternative"""
        models = self.get_available_models()
        model_names = [m['name'] for m in models]
        
        # Check if preferred model exists
        if preferred_model and preferred_model in model_names:
            return preferred_model
        
        # Fallback to best available
        return self.select_best_model()
    
    def is_ollama_available(self) -> bool:
        """Check if Ollama service is running"""
        ollama_paths = [
            'ollama',
            r'C:\Users\User\AppData\Local\Programs\Ollama\ollama.exe',
            '/usr/local/bin/ollama',
        ]
        
        for ollama_path in ollama_paths:
            try:
                result = subprocess.run(
                    [ollama_path, 'list'],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    return True
            except:
                continue
        return False
    
    def get_status_report(self) -> Dict:
        """Generate comprehensive status report"""
        models = self.get_available_models()
        is_available = self.is_ollama_available()
        best_model = self.select_best_model()
        
        return {
            'ollama_available': is_available,
            'total_models': len(models),
            'models': [m['name'] for m in models],
            'recommended_model': best_model,
            'total_size_gb': sum(m['size_gb'] for m in models),
            'cache_age_seconds': (
                (datetime.now() - self.cache_time).total_seconds()
                if self.cache_time else None
            )
        }

# Testing
if __name__ == '__main__':
    detector = OllamaModelDetector()
    
    print('Ollama Model Detection Report')
    print('==============================')
    
    status = detector.get_status_report()
    print(f'Ollama Available: {status["ollama_available"]}')
    print(f'Models Found: {status["total_models"]}')
    
    if status['models']:
        print('\nAvailable Models:')
        for model in status['models']:
            print(f'  - {model}')
        print(f'\nRecommended Model: {status["recommended_model"]}')
        print(f'Total Storage: {status["total_size_gb"]:.1f} GB')
    else:
        print('\nNo Ollama models found. Please run: ollama pull llama3.2')