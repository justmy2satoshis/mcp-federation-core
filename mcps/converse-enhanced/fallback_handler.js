const { spawn } = require('child_process');

class FallbackHandler {
  constructor() {
    this.ollamaPaths = [
      'ollama',
      'C:\\Users\\User\\AppData\\Local\\Programs\\Ollama\\ollama.exe',
      '/usr/local/bin/ollama',
    ];
    
    this.setupInstructions = {
      ollama: [
        'Install Ollama: https://ollama.ai',
        'Pull a model: ollama pull llama3.2',
        'Verify: ollama list'
      ],
      openai: [
        'Get API key: https://platform.openai.com/api-keys',
        'Set environment: export OPENAI_API_KEY=sk-...',
        'Add to .env file for persistence'
      ],
      xai: [
        'Get xAI/Grok API key: https://console.x.ai',
        'Set environment: export XAI_API_KEY=xai-...',
        'Grok models provide high-quality responses'
      ],
      general: [
        'Option 1: Install Ollama for FREE local AI',
        'Option 2: Configure API keys for cloud providers',
        'Option 3: Use OpenRouter for multiple providers'
      ]
    };
  }

  async handleNoProviders(attemptedProviders = []) {
    const response = {
      error: 'No AI providers available',
      attempted: attemptedProviders,
      recommendations: [],
      quickFix: null
    };

    // Check what's missing
    const hasOllama = await this.checkOllama();
    const hasApiKeys = this.checkApiKeys();

    if (!hasOllama && !hasApiKeys) {
      response.quickFix = 'Install Ollama for immediate FREE access';
      response.recommendations = this.setupInstructions.ollama;
    } else if (!hasOllama) {
      response.quickFix = 'Configure API keys in environment';
      response.recommendations = this.setupInstructions.openai;
    }

    response.message = this.formatUserMessage(response);
    return response;
  }

  formatUserMessage(response) {
    let message = 'Converse MCP: No AI providers currently available\n\n';
    
    if (response.quickFix) {
      message += `Quick Fix: ${response.quickFix}\n\n`;
    }
    
    message += 'Setup Options:\n';
    response.recommendations.forEach((rec, i) => {
      message += `${i + 1}. ${rec}\n`;
    });
    
    message += '\nOnce configured, Converse MCP will automatically use the best available provider.';
    message += '\n\nProvider Priority: Ollama (free) > OpenAI > Anthropic > xAI/Grok > Others';
    return message;
  }

  async checkOllama() {
    for (const ollamaPath of this.ollamaPaths) {
      try {
        const result = await new Promise((resolve, reject) => {
          const ollama = spawn(ollamaPath, ['list']);
          
          ollama.on('close', (code) => {
            resolve(code === 0);
          });
          
          ollama.on('error', () => {
            resolve(false);
          });
          
          setTimeout(() => {
            ollama.kill();
            resolve(false);
          }, 2000);
        });
        
        if (result) return true;
      } catch {
        continue;
      }
    }
    return false;
  }

  checkApiKeys() {
    const keys = [
      'OPENAI_API_KEY',
      'ANTHROPIC_API_KEY',
      'XAI_API_KEY',
      'MISTRAL_API_KEY',
      'OPENROUTER_API_KEY'
    ];
    return keys.some(key => process.env[key]);
  }
  
  async generateStatusReport() {
    const hasOllama = await this.checkOllama();
    const apiKeys = this.getConfiguredApis();
    
    let report = 'Converse MCP Status Report\n';
    report += '==========================\n\n';
    
    if (hasOllama) {
      report += 'Ollama: AVAILABLE (FREE local AI)\n';
      const models = await this.getOllamaModels();
      if (models.length > 0) {
        report += `  Models: ${models.join(', ')}\n`;
      }
    } else {
      report += 'Ollama: NOT AVAILABLE\n';
      report += '  Tip: Install from https://ollama.ai for free local AI\n';
    }
    
    report += '\nAPI Providers:\n';
    if (apiKeys.length > 0) {
      apiKeys.forEach(api => {
        report += `  - ${api}: CONFIGURED\n`;
      });
    } else {
      report += '  None configured\n';
    }
    
    report += '\nCost Optimization: ' + (hasOllama ? 'ENABLED (95% savings)' : 'DISABLED');
    
    return report;
  }
  
  getConfiguredApis() {
    const apiMap = {
      'OPENAI_API_KEY': 'OpenAI',
      'ANTHROPIC_API_KEY': 'Anthropic',
      'XAI_API_KEY': 'xAI/Grok',
      'MISTRAL_API_KEY': 'Mistral',
      'OPENROUTER_API_KEY': 'OpenRouter'
    };
    
    return Object.entries(apiMap)
      .filter(([key]) => process.env[key])
      .map(([, name]) => name);
  }
  
  async getOllamaModels() {
    for (const ollamaPath of this.ollamaPaths) {
      try {
        const result = await new Promise((resolve) => {
          const ollama = spawn(ollamaPath, ['list']);
          let output = '';
          
          ollama.stdout.on('data', (data) => {
            output += data.toString();
          });
          
          ollama.on('close', (code) => {
            if (code === 0) {
              const lines = output.split('\n').slice(1);
              const models = lines
                .filter(line => line.trim())
                .map(line => line.split(/\s+/)[0]);
              resolve(models);
            } else {
              resolve([]);
            }
          });
          
          ollama.on('error', () => resolve([]));
          
          setTimeout(() => {
            ollama.kill();
            resolve([]);
          }, 2000);
        });
        
        if (result.length > 0) return result;
      } catch {
        continue;
      }
    }
    return [];
  }
}

module.exports = FallbackHandler;