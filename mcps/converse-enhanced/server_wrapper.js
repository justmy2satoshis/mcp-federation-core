const { spawn } = require('child_process');
const path = require('path');

class ConverseWrapper {
  constructor() {
    this.ollamaModels = [];
    this.lastModelCheck = null;
    this.modelCheckInterval = 5 * 60 * 1000; // 5 minutes
    this.ollamaPaths = [
      'ollama',
      'C:\\Users\\User\\AppData\\Local\\Programs\\Ollama\\ollama.exe',
      '/usr/local/bin/ollama',
    ];
    this.fallbackProviders = [
      'ollama',
      'openai',
      'anthropic',
      'xai',
      'mistral',
      'openrouter'
    ];
  }

  async detectOllamaModels() {
    // Check cache
    if (this.lastModelCheck && 
        Date.now() - this.lastModelCheck < this.modelCheckInterval) {
      return this.ollamaModels;
    }

    for (const ollamaPath of this.ollamaPaths) {
      const models = await this.tryOllamaPath(ollamaPath);
      if (models.length > 0) {
        this.ollamaModels = models;
        this.lastModelCheck = Date.now();
        return models;
      }
    }
    
    return [];
  }

  tryOllamaPath(ollamaPath) {
    return new Promise((resolve) => {
      try {
        const ollama = spawn(ollamaPath, ['list']);
        let output = '';

        ollama.stdout.on('data', (data) => {
          output += data.toString();
        });

        ollama.on('close', (code) => {
          if (code === 0) {
            // Parse output
            const lines = output.split('\n').slice(1); // Skip header
            const models = lines
              .filter(line => line.trim())
              .map(line => {
                const parts = line.split(/\s+/);
                return parts[0]; // Model name
              });
            
            console.log(`Detected ${models.length} Ollama models at ${ollamaPath}:`, models);
            resolve(models);
          } else {
            resolve([]);
          }
        });

        ollama.on('error', () => {
          resolve([]);
        });

        // Timeout after 5 seconds
        setTimeout(() => {
          ollama.kill();
          resolve([]);
        }, 5000);
      } catch (e) {
        resolve([]);
      }
    });
  }

  selectBestOllamaModel(models) {
    // Priority order
    const priorities = [
      /llama3\.\d+/i,
      /mixtral/i,
      /mistral/i,
      /gemma/i,
      /qwen/i,
      /phi/i,
      /codellama/i,
      /.*:latest/,
      /.*/
    ];

    for (const pattern of priorities) {
      const match = models.find(m => pattern.test(m));
      if (match) return match;
    }

    return models[0] || null;
  }

  async routeRequest(prompt, requestedModel = 'auto') {
    // If auto mode, detect best option
    if (requestedModel === 'auto' || requestedModel === 'ollama') {
      const ollamaModels = await this.detectOllamaModels();
      
      if (ollamaModels.length > 0) {
        const bestModel = this.selectBestOllamaModel(ollamaModels);
        console.log(`Auto-selected Ollama model: ${bestModel}`);
        return {
          provider: 'ollama',
          model: bestModel,
          cost: 0,
          status: 'Using FREE local Ollama'
        };
      }
    }

    // Fallback to API providers
    for (const provider of this.fallbackProviders.slice(1)) {
      if (this.hasApiKey(provider)) {
        return {
          provider,
          model: this.getDefaultModel(provider),
          cost: this.estimateCost(provider),
          status: `Using ${provider} API (paid)`
        };
      }
    }

    return {
      provider: null,
      model: null,
      cost: 0,
      status: 'No providers available - please configure API keys or install Ollama'
    };
  }

  hasApiKey(provider) {
    const keyMap = {
      openai: 'OPENAI_API_KEY',
      anthropic: 'ANTHROPIC_API_KEY',
      xai: 'XAI_API_KEY',
      mistral: 'MISTRAL_API_KEY',
      openrouter: 'OPENROUTER_API_KEY',
    };
    return process.env[keyMap[provider]] !== undefined;
  }

  getDefaultModel(provider) {
    const defaults = {
      openai: 'gpt-4',
      anthropic: 'claude-3-sonnet',
      xai: 'grok-2',
      mistral: 'mistral-large',
      openrouter: 'auto',
    };
    return defaults[provider] || 'auto';
  }

  estimateCost(provider) {
    const costs = {
      openai: 0.03,
      anthropic: 0.025,
      xai: 0.02,
      mistral: 0.012,
      openrouter: 0.015,
    };
    return costs[provider] || 0.01;
  }
}

module.exports = ConverseWrapper;