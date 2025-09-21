#!/usr/bin/env node

/**
 * Ollama Integration Test Suite
 * Tests Ollama connectivity and model responses
 */

const http = require('http');

class OllamaTest {
  constructor(baseUrl = 'http://localhost:11434') {
    this.baseUrl = baseUrl;
    this.testResults = [];
  }

  async makeRequest(endpoint, data) {
    return new Promise((resolve, reject) => {
      const url = new URL(endpoint, this.baseUrl);
      const postData = JSON.stringify(data);

      const options = {
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(postData)
        }
      };

      const req = http.request(options, (res) => {
        let body = '';
        res.on('data', (chunk) => body += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(body));
          } catch (e) {
            resolve(body);
          }
        });
      });

      req.on('error', reject);
      req.write(postData);
      req.end();
    });
  }

  async testConnection() {
    console.log('🔍 Testing Ollama connection...');
    try {
      const response = await fetch(`${this.baseUrl}/api/tags`);
      const data = await response.json();

      if (data.models && data.models.length > 0) {
        console.log(`✅ Connection successful! Found ${data.models.length} models:`);
        data.models.forEach(model => {
          console.log(`   - ${model.name} (${model.details.parameter_size})`);
        });
        this.testResults.push({ test: 'connection', status: 'passed' });
        return true;
      }
    } catch (error) {
      console.log(`❌ Connection failed: ${error.message}`);
      this.testResults.push({ test: 'connection', status: 'failed', error: error.message });
      return false;
    }
  }

  async testModel(modelName, prompt) {
    console.log(`\n🤖 Testing model: ${modelName}`);
    console.log(`📝 Prompt: "${prompt}"`);

    const startTime = Date.now();

    try {
      const response = await this.makeRequest('/api/generate', {
        model: modelName,
        prompt: prompt,
        stream: false
      });

      const duration = Date.now() - startTime;

      if (response.response) {
        console.log(`✅ Response received in ${duration}ms`);
        console.log(`📄 Response: ${response.response.substring(0, 200)}...`);

        this.testResults.push({
          test: `model_${modelName}`,
          status: 'passed',
          duration: duration,
          response_length: response.response.length
        });
        return true;
      }
    } catch (error) {
      console.log(`❌ Model test failed: ${error.message}`);
      this.testResults.push({
        test: `model_${modelName}`,
        status: 'failed',
        error: error.message
      });
      return false;
    }
  }

  async runAllTests() {
    console.log('╔══════════════════════════════════════════════╗');
    console.log('║       🧪 Ollama Integration Test Suite       ║');
    console.log('╚══════════════════════════════════════════════╝\n');

    // Test connection
    const connected = await this.testConnection();
    if (!connected) {
      console.log('\n⚠️  Cannot proceed without connection');
      return this.generateReport();
    }

    // Test available models
    const models = ['llama3.2:3b', 'phi3:mini', 'codellama:7b'];
    const prompts = {
      'llama3.2:3b': 'Hello! Please respond with a brief greeting.',
      'phi3:mini': 'What is 2 + 2?',
      'codellama:7b': 'Write a Python hello world function.'
    };

    for (const model of models) {
      if (prompts[model]) {
        await this.testModel(model, prompts[model]);
      }
    }

    return this.generateReport();
  }

  generateReport() {
    console.log('\n╔══════════════════════════════════════════════╗');
    console.log('║              📊 Test Results                 ║');
    console.log('╚══════════════════════════════════════════════╝\n');

    const passed = this.testResults.filter(r => r.status === 'passed').length;
    const failed = this.testResults.filter(r => r.status === 'failed').length;

    console.log(`Total Tests: ${this.testResults.length}`);
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);

    if (passed === this.testResults.length) {
      console.log('\n🎉 All tests passed! Ollama integration is ready.');
    } else {
      console.log('\n⚠️  Some tests failed. Please check the errors above.');
    }

    return this.testResults;
  }
}

// Run tests if executed directly
if (require.main === module) {
  const tester = new OllamaTest();
  tester.runAllTests().then(results => {
    process.exit(results.every(r => r.status === 'passed') ? 0 : 1);
  });
}

module.exports = OllamaTest;