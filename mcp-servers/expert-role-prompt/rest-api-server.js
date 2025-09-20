// rest-api-server.js
// REST API interface for expert-role-prompt MCP
// Provides HTTP endpoints for external integration

const express = require('express');
const cors = require('cors');
const { EXPERT_ROLES_EXPANDED } = require('./expert-roles-expanded.js');
const { ReasoningEngine } = require('./reasoning-frameworks.js');
const { ConfidenceScoring } = require('./confidence-scoring.js');

// Initialize modules
const app = express();
const reasoningEngine = new ReasoningEngine();
const confidenceScorer = new ConfidenceScoring();

// Middleware
app.use(express.json());
app.use(cors());

// Configuration
const PORT = process.env.PORT || 3456;
const API_PREFIX = '/api/v1';

// Health check endpoint
app.get(`${API_PREFIX}/health`, (req, res) => {
  res.json({
    status: 'healthy',
    version: '2.0.0',
    experts: Object.values(EXPERT_ROLES_EXPANDED).reduce((acc, cat) => acc + Object.keys(cat).length, 0),
    features: ['Chain-of-Thought', 'Tree-of-Thoughts', 'Enhanced Confidence Scoring']
  });
});

// Get all expert roles
app.get(`${API_PREFIX}/experts`, (req, res) => {
  const { category } = req.query;
  let experts = [];

  for (const [cat, roleSet] of Object.entries(EXPERT_ROLES_EXPANDED)) {
    if (!category || category === cat) {
      for (const [id, expert] of Object.entries(roleSet)) {
        experts.push({
          id: id,
          category: cat,
          ...expert
        });
      }
    }
  }

  res.json({
    total: experts.length,
    experts: experts
  });
});

// Get specific expert details
app.get(`${API_PREFIX}/experts/:expertId`, (req, res) => {
  const { expertId } = req.params;
  
  for (const category of Object.values(EXPERT_ROLES_EXPANDED)) {
    if (category[expertId]) {
      return res.json({
        id: expertId,
        ...category[expertId]
      });
    }
  }
  
  res.status(404).json({ error: 'Expert not found' });
});

// Nominate expert for task
app.post(`${API_PREFIX}/nominate`, (req, res) => {
  const { task, context } = req.body;
  
  if (!task) {
    return res.status(400).json({ error: 'Task description required' });
  }

  const allExperts = [];
  for (const [category, experts] of Object.entries(EXPERT_ROLES_EXPANDED)) {
    for (const [expertId, expert] of Object.entries(experts)) {
      allExperts.push({
        id: expertId,
        category: category,
        ...expert
      });
    }
  }

  // Score all experts
  const scoredExperts = allExperts.map(expert => {
    const confidenceResult = confidenceScorer.calculateConfidence(
      expert.id,
      task,
      context || {}
    );

    return {
      ...expert,
      ...confidenceResult
    };
  });

  // Sort by confidence score
  scoredExperts.sort((a, b) => b.score - a.score);

  // Get top 5 candidates
  const topCandidates = scoredExperts.slice(0, 5);

  res.json({
    task: task,
    best_match: topCandidates[0],
    alternatives: topCandidates.slice(1),
    total_evaluated: allExperts.length
  });
});

// Apply reasoning framework
app.post(`${API_PREFIX}/reasoning`, (req, res) => {
  const { framework, template, variables } = req.body;
  
  if (!framework || !template || !variables) {
    return res.status(400).json({ 
      error: 'Framework, template, and variables required' 
    });
  }

  try {
    let result;
    
    if (framework === 'chainOfThought') {
      result = reasoningEngine.executeChainOfThought(template, variables);
    } else if (framework === 'treeOfThoughts') {
      result = reasoningEngine.executeTreeOfThoughts(template, variables);
    } else {
      return res.status(400).json({ error: 'Invalid framework' });
    }

    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Test confidence scoring
app.post(`${API_PREFIX}/confidence/test`, (req, res) => {
  const { expertId, query, context } = req.body;
  
  if (!expertId || !query) {
    return res.status(400).json({ 
      error: 'expertId and query required' 
    });
  }

  const result = confidenceScorer.calculateConfidence(
    expertId,
    query,
    context || {}
  );

  res.json(result);
});

// Get available reasoning templates
app.get(`${API_PREFIX}/reasoning/templates`, (req, res) => {
  const templates = reasoningEngine.getAvailableTemplates();
  res.json(templates);
});

// WebSocket support for real-time features
const WebSocket = require('ws');
const server = require('http').createServer(app);
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
  console.log('WebSocket client connected');
  
  ws.on('message', (message) => {
    const data = JSON.parse(message);
    
    if (data.type === 'nominate') {
      // Real-time expert nomination
      const result = performNomination(data.task);
      ws.send(JSON.stringify({
        type: 'nomination',
        result: result
      }));
    }
  });

  ws.on('close', () => {
    console.log('WebSocket client disconnected');
  });
});

// Helper function for real-time nomination
function performNomination(task) {
  const allExperts = [];
  for (const [category, experts] of Object.entries(EXPERT_ROLES_EXPANDED)) {
    for (const [expertId, expert] of Object.entries(experts)) {
      allExperts.push({
        id: expertId,
        category: category,
        ...expert
      });
    }
  }

  const scoredExperts = allExperts.map(expert => {
    const confidenceResult = confidenceScorer.calculateConfidence(
      expert.id,
      task,
      {}
    );

    return {
      ...expert,
      ...confidenceResult
    };
  });

  scoredExperts.sort((a, b) => b.score - a.score);
  return scoredExperts[0];
}

// GraphQL endpoint (basic implementation)
app.post(`${API_PREFIX}/graphql`, (req, res) => {
  // Simplified GraphQL handler
  const { query } = req.body;
  
  if (query.includes('experts')) {
    const experts = [];
    for (const [cat, roleSet] of Object.entries(EXPERT_ROLES_EXPANDED)) {
      for (const [id, expert] of Object.entries(roleSet)) {
        experts.push({
          id: id,
          category: cat,
          ...expert
        });
      }
    }
    
    res.json({
      data: {
        experts: experts
      }
    });
  } else {
    res.status(400).json({ error: 'Invalid GraphQL query' });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
if (require.main === module) {
  server.listen(PORT, () => {
    console.log(`🚀 REST API Server running on http://localhost:${PORT}`);
    console.log(`📊 ${Object.values(EXPERT_ROLES_EXPANDED).reduce((acc, cat) => acc + Object.keys(cat).length, 0)} expert roles available`);
    console.log(`🔌 WebSocket server ready for real-time connections`);
    console.log(`📡 GraphQL endpoint available at ${API_PREFIX}/graphql`);
  });
}

module.exports = app;
