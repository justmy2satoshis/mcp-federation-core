#!/usr/bin/env node

/**
 * Enhanced Expert Role Prompt MCP Server v2.0
 * Now with 50+ roles, CoT/ToT reasoning, and improved confidence scoring
 */

const { Server } = require('@modelcontextprotocol/sdk/server/index.js');
const { StdioServerTransport } = require('@modelcontextprotocol/sdk/server/stdio.js');
const { 
  CallToolRequestSchema, 
  ListToolsRequestSchema 
} = require('@modelcontextprotocol/sdk/types.js');

// Import enhanced modules
const { EXPERT_ROLES_EXPANDED } = require('./expert-roles-expanded.js');
const { REASONING_FRAMEWORKS, ReasoningEngine } = require('./reasoning-frameworks.js');
const { ConfidenceScoring } = require('./confidence-scoring.js');

// Import original keyword mapping (still useful)
const { 
  WEIGHTED_KEYWORD_MAPPING, 
  SEMANTIC_CLUSTERS, 
  CATEGORY_KEYWORDS,
  COMMON_WORDS_PENALTY
} = require('./enhanced-keyword-mapping.js');

// Initialize modules
const reasoningEngine = new ReasoningEngine();
const confidenceScorer = new ConfidenceScoring();
// Enhanced workflow templates with reasoning integration
const WORKFLOW_TEMPLATES_ENHANCED = {
  'research-and-report': {
    name: 'Research and Report Generation',
    description: 'Comprehensive research workflow with structured reporting',
    reasoning: 'chainOfThought',
    template: 'research',
    steps: ['Research planning', 'Data collection', 'Analysis', 'Report generation']
  },
  'code-review-and-optimize': {
    name: 'Code Review and Optimization',
    description: 'Complete code review workflow with optimization recommendations',
    reasoning: 'chainOfThought',
    template: 'technical',
    steps: ['Code analysis', 'Performance review', 'Security check', 'Optimization']
  },
  'data-analysis-pipeline': {
    name: 'Data Analysis Pipeline',
    description: 'End-to-end data analysis workflow',
    reasoning: 'treeOfThoughts',
    template: 'exploration-tree',
    steps: ['Data ingestion', 'Cleaning', 'Analysis', 'Visualization']
  },
  'ml-model-development': {
    name: 'Machine Learning Model Development',
    description: 'Complete ML pipeline from data preparation to deployment',
    reasoning: 'chainOfThought',
    template: 'technical',
    steps: ['Data preparation', 'Feature engineering', 'Model training', 'Evaluation', 'Deployment']
  },
  'security-audit-workflow': {
    name: 'Security Audit and Assessment',
    description: 'Comprehensive security evaluation and remediation workflow',
    reasoning: 'treeOfThoughts',
    template: 'decision-tree',
    steps: ['Vulnerability scanning', 'Risk assessment', 'Penetration testing', 'Remediation planning', 'Implementation']
  },
  'product-launch-strategy': {
    name: 'Product Launch Strategy',
    description: 'End-to-end product launch planning and execution',
    reasoning: 'chainOfThought',
    template: 'strategic',
    steps: ['Market research', 'Strategy planning', 'Execution roadmap', 'Launch preparation', 'Post-launch monitoring']
  },
  'incident-response-protocol': {
    name: 'Production Incident Response',
    description: 'Systematic incident management and resolution workflow',
    reasoning: 'treeOfThoughts',
    template: 'scenario-tree',
    steps: ['Detection', 'Triage', 'Diagnosis', 'Resolution', 'Post-mortem']
  },
  'architecture-design-review': {
    name: 'System Architecture Design Review',
    description: 'Comprehensive architecture evaluation and optimization',
    reasoning: 'chainOfThought',
    template: 'analytical',
    steps: ['Current state analysis', 'Requirements review', 'Design evaluation', 'Recommendations', 'Implementation plan']
  },
  'creative-ideation': {
    name: 'Creative Ideation Workflow',
    description: 'Structured creative problem solving and innovation',
    reasoning: 'chainOfThought',
    template: 'creative',
    steps: ['Problem exploration', 'Ideation', 'Concept development', 'Prototyping', 'Testing']
  },
  'strategic-planning': {
    name: 'Strategic Business Planning',
    description: 'Comprehensive strategic analysis and planning',
    reasoning: 'treeOfThoughts',
    template: 'decision-tree',
    steps: ['Market analysis', 'SWOT', 'Strategy formulation', 'Implementation plan', 'KPI definition']
  }
};

// Custom workflow storage (for user-created workflows)
let customWorkflows = {};

// Server instance
const server = new Server(
  {
    name: 'expert-role-prompt-enhanced',
    version: '2.0.0',
    description: 'Enhanced expert role prompting with 50+ roles, CoT/ToT reasoning, and improved confidence scoring'
  },
  {
    capabilities: {
      tools: {
        nominate: 'Nominate the best expert with enhanced confidence scoring',
        enhance: 'Enhance prompts with expert context and reasoning frameworks',
        list_roles: 'List all 50+ available expert roles',
        get_capabilities: 'Get detailed expert capabilities',
        execute_workflow: 'Execute workflow with integrated reasoning',
        create_workflow: 'Create custom workflow templates',
        chain_workflows: 'Chain multiple workflows together',
        list_workflows: 'List all available workflows',
        apply_reasoning: 'Apply Chain-of-Thought or Tree-of-Thoughts reasoning',
        test_confidence: 'Test confidence scoring for expert matching'
      }
    }
  }
);
// Enhanced expert nomination with improved confidence scoring
async function nominateExpertEnhanced(task) {
  console.error('\n🔍 Enhanced Expert Nomination Starting...');
  console.error(`Task: ${task.substring(0, 100)}...`);

  const queryLower = task.toLowerCase();
  const allExperts = [];

  // Collect all experts from all categories
  for (const [category, experts] of Object.entries(EXPERT_ROLES_EXPANDED)) {
    for (const [expertId, expert] of Object.entries(experts)) {
      allExperts.push({
        id: expertId,
        category: category,
        ...expert
      });
    }
  }

  console.error(`\n📊 Evaluating ${allExperts.length} expert roles...`);

  // Score all experts using enhanced confidence scoring
  const scoredExperts = allExperts.map(expert => {
    const confidenceResult = confidenceScorer.calculateConfidence(
      expert.id,
      task,
      { category: expert.category, capabilities: expert.capabilities }
    );

    return {
      ...expert,
      ...confidenceResult
    };
  });

  // Sort by confidence score
  scoredExperts.sort((a, b) => b.score - a.score);

  // Get top 3 candidates
  const topCandidates = scoredExperts.slice(0, 3);
  const bestMatch = topCandidates[0];

  console.error('\n🏆 Top 3 Candidates:');
  topCandidates.forEach((candidate, index) => {
    console.error(`${index + 1}. ${candidate.name} (${candidate.id})`);
    console.error(`   Score: ${candidate.score}% (${candidate.level})`);
    console.error(`   Reasoning: ${candidate.reasoning}`);
  });

  return {
    best_match: bestMatch,
    alternatives: topCandidates.slice(1),
    total_evaluated: allExperts.length
  };
}

// Enhanced prompt with reasoning frameworks
async function enhancePromptWithReasoning(expertId, task, reasoningType = 'analytical') {
  const expert = findExpertById(expertId);
  if (!expert) {
    throw new Error(`Expert '${expertId}' not found`);
  }

  // Apply Chain-of-Thought reasoning
  let reasoningResult = null;
  if (reasoningType && REASONING_FRAMEWORKS.chainOfThought[reasoningType]) {
    const variables = {
      expert_role: expert.name,
      problem_statement: task,
      core_challenge: 'To be analyzed',
      constraints: 'To be identified',
      success_criteria: 'To be defined',
      // ... other variables would be filled based on task analysis
    };

    reasoningResult = reasoningEngine.executeChainOfThought(reasoningType, variables);
  }

  // Apply constitutional principles
  const constitutionalCheck = reasoningEngine.applyConstitutionalPrinciples(task);

  // Generate enhanced prompt
  const enhancedPrompt = `
## Expert Role: ${expert.name}

### Expertise Applied
${expert.description}

### Core Capabilities
${expert.capabilities.map(cap => `- ${cap}`).join('\n')}

### Frameworks & Tools
${expert.frameworks.map(fw => `- ${fw}`).join('\n')}

${reasoningResult ? `### Structured Reasoning (${reasoningResult.template})
${reasoningResult.reasoning}` : ''}

### Constitutional Principles Applied
✅ ${constitutionalCheck.principles_checked} principles verified

### Task Analysis
"${task}"

### Expert Approach
As ${expert.name}, I will:
1. Leverage my expertise in ${expert.capabilities[0]}
2. Apply best practices from ${expert.frameworks[0]}
3. Ensure ${constitutionalCheck.compliance[0].principle}
4. Deliver actionable insights and recommendations

Let me proceed with this task using my specialized knowledge and proven methodologies.
`;

  return {
    expert: expert,
    enhanced_prompt: enhancedPrompt,
    reasoning: reasoningResult,
    constitutional_check: constitutionalCheck
  };
}

// Helper function to find expert by ID
function findExpertById(expertId) {
  for (const category of Object.values(EXPERT_ROLES_EXPANDED)) {
    if (category[expertId]) {
      return category[expertId];
    }
  }
  return null;
}
// Tool handlers
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'nominate_expert',
      description: 'Nominate the best expert role for a given task with enhanced confidence scoring',
      inputSchema: {
        type: 'object',
        properties: {
          task_description: {
            type: 'string',
            description: 'The task to analyze for expert nomination'
          },
          context: {
            type: 'string',
            description: 'Additional context (optional)'
          }
        },
        required: ['task_description']
      }
    },
    {
      name: 'enhance_prompt',
      description: 'Enhance a prompt with expert frameworks, methodologies, and reasoning',
      inputSchema: {
        type: 'object',
        properties: {
          expert_id: {
            type: 'string',
            description: 'The expert role ID to use for enhancement'
          },
          task_description: {
            type: 'string',
            description: 'The task to enhance'
          },
          reasoning_type: {
            type: 'string',
            enum: ['analytical', 'technical', 'creative', 'strategic', 'research'],
            description: 'Type of reasoning to apply (optional)'
          }
        },
        required: ['expert_id', 'task_description']
      }
    },
    {
      name: 'list_expert_roles',
      description: 'List all available expert roles with categories',
      inputSchema: {
        type: 'object',
        properties: {
          category: {
            type: 'string',
            description: 'Filter by category (optional)'
          }
        }
      }
    },
    {
      name: 'get_expert_capabilities',
      description: 'Get detailed information about a specific expert role',
      inputSchema: {
        type: 'object',
        properties: {
          expert_id: {
            type: 'string',
            description: 'The expert role ID to get information for'
          }
        },
        required: ['expert_id']
      }
    },
    {
      name: 'execute_workflow',
      description: 'Execute a pre-defined workflow template with reasoning',
      inputSchema: {
        type: 'object',
        properties: {
          template_name: {
            type: 'string',
            description: 'Name of the workflow template to execute'
          },
          context: {
            type: 'object',
            description: 'Context data for the workflow'
          }
        },
        required: ['template_name']
      }
    },
    {
      name: 'apply_reasoning',
      description: 'Apply Chain-of-Thought or Tree-of-Thoughts reasoning',
      inputSchema: {
        type: 'object',
        properties: {
          framework: {
            type: 'string',
            enum: ['chainOfThought', 'treeOfThoughts'],
            description: 'Reasoning framework to use'
          },
          template: {
            type: 'string',
            description: 'Template name within the framework'
          },
          variables: {
            type: 'object',
            description: 'Variables to populate in the template'
          }
        },
        required: ['framework', 'template', 'variables']
      }
    },
    {
      name: 'test_confidence',
      description: 'Test confidence scoring for expert matching',
      inputSchema: {
        type: 'object',
        properties: {
          expert_id: {
            type: 'string',
            description: 'Expert ID to test'
          },
          query: {
            type: 'string',
            description: 'Query to test against'
          }
        },
        required: ['expert_id', 'query']
      }
    },
    {
      name: 'create_custom_workflow',
      description: 'Create a custom workflow template',
      inputSchema: {
        type: 'object',
        properties: {
          name: {
            type: 'string',
            description: 'Name for the custom workflow'
          },
          description: {
            type: 'string',
            description: 'Description of the workflow'
          },
          steps: {
            type: 'array',
            items: { type: 'object' },
            description: 'Array of workflow steps'
          }
        },
        required: ['name', 'description', 'steps']
      }
    },
    {
      name: 'chain_workflows',
      description: 'Execute multiple workflows in sequence',
      inputSchema: {
        type: 'object',
        properties: {
          workflows: {
            type: 'array',
            items: { type: 'string' },
            description: 'Array of workflow names to chain'
          },
          context: {
            type: 'object',
            description: 'Initial context data'
          }
        },
        required: ['workflows']
      }
    },
    {
      name: 'list_workflows',
      description: 'List available workflow templates',
      inputSchema: {
        type: 'object',
        properties: {
          domain: {
            type: 'string',
            description: 'Filter by domain (optional)'
          }
        }
      }
    }
  ]
}));
// Tool execution handler
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case 'nominate_expert': {
        const result = await nominateExpertEnhanced(args.task_description);
        
        return {
          content: [
            {
              type: 'text',
              text: `🎯 Expert Nomination Results

📊 Task: ${args.task_description}

🎯 Best Match: ${result.best_match.name}
📁 Category: ${result.best_match.category}
⭐ Confidence: ${result.best_match.confidence} (${result.best_match.level})
🔍 Matched Keywords: ${result.best_match.matchDetails.exact_matches.join(', ')}

💡 Expertise: ${result.best_match.description}
🛠️ Key Capabilities: ${result.best_match.capabilities.slice(0, 3).join(', ')}

📝 Reasoning: ${result.best_match.reasoning}

🔄 Alternative Experts:
${result.alternatives.map((alt, i) => `${i + 1}. ${alt.name} (${alt.confidence})`).join('\n')}

📈 Evaluated ${result.total_evaluated} expert roles total`
            }
          ]
        };
      }

      case 'enhance_prompt': {
        const result = await enhancePromptWithReasoning(
          args.expert_id,
          args.task_description,
          args.reasoning_type
        );
        
        return {
          content: [
            {
              type: 'text',
              text: result.enhanced_prompt
            }
          ]
        };
      }

      case 'list_expert_roles': {
        let result = '📚 Available Expert Roles\n\n';
        let totalCount = 0;
        
        for (const [category, experts] of Object.entries(EXPERT_ROLES_EXPANDED)) {
          if (!args.category || args.category === category) {
            result += `📁 ${category.toUpperCase()}\n\n`;
            
            for (const [id, expert] of Object.entries(experts)) {
              result += `• ${expert.name} (${id})\n`;
              result += `  ${expert.description}\n`;
              result += `  Capabilities: ${expert.capabilities.slice(0, 3).join(', ')}\n\n`;
              totalCount++;
            }
          }
        }
        
        result = `📚 Available Expert Roles (${totalCount} total)\n\n` + result;
        
        return {
          content: [{ type: 'text', text: result }]
        };
      }

      case 'get_expert_capabilities': {
        const expert = findExpertById(args.expert_id);
        if (!expert) {
          throw new Error(`Expert '${args.expert_id}' not found`);
        }

        const result = `🎯 Expert Capabilities: ${expert.name}

📝 Description: ${expert.description}

🛠️ Core Capabilities:
${expert.capabilities.map(cap => `• ${cap}`).join('\n')}

📚 Frameworks & Tools:
${expert.frameworks.map(fw => `• ${fw}`).join('\n')}

💡 Best For:
• ${expert.capabilities[0]}
• ${expert.capabilities[1] || 'Advanced problem solving'}
• ${expert.capabilities[2] || 'Strategic planning'}`;

        return {
          content: [{ type: 'text', text: result }]
        };
      }

      case 'apply_reasoning': {
        let result;
        
        if (args.framework === 'chainOfThought') {
          result = reasoningEngine.executeChainOfThought(args.template, args.variables);
        } else if (args.framework === 'treeOfThoughts') {
          result = reasoningEngine.executeTreeOfThoughts(args.template, args.variables);
        } else {
          throw new Error(`Unknown framework: ${args.framework}`);
        }

        return {
          content: [
            {
              type: 'text',
              text: `🧠 ${result.framework} Applied

📋 Template: ${result.template}

${result.reasoning || ''}

${result.analysis || ''}`
            }
          ]
        };
      }

      case 'test_confidence': {
        const result = confidenceScorer.calculateConfidence(
          args.expert_id,
          args.query,
          {}
        );

        return {
          content: [
            {
              type: 'text',
              text: `🔬 Confidence Test Results

Expert: ${args.expert_id}
Query: "${args.query}"

📊 Score: ${result.score}%
📈 Confidence: ${result.confidence}
🎯 Level: ${result.level}

Matched Terms:
• Exact: ${result.matchDetails.exact_matches.join(', ') || 'None'}
• Semantic: ${result.matchDetails.semantic_matches.join(', ') || 'None'}
• Negative: ${result.matchDetails.negative_matches.join(', ') || 'None'}

Reasoning: ${result.reasoning}`
            }
          ]
        };
      }

      case 'execute_workflow': {
        const workflow = WORKFLOW_TEMPLATES_ENHANCED[args.template_name] || customWorkflows[args.template_name];
        
        if (!workflow) {
          throw new Error(`Workflow '${args.template_name}' not found`);
        }

        let reasoningResult = null;
        if (workflow.reasoning && workflow.template) {
          // Apply reasoning framework
          const framework = workflow.reasoning;
          const template = workflow.template;
          
          // Prepare variables from context
          const variables = args.context || {};
          
          if (framework === 'chainOfThought') {
            reasoningResult = reasoningEngine.executeChainOfThought(template, variables);
          } else if (framework === 'treeOfThoughts') {
            reasoningResult = reasoningEngine.executeTreeOfThoughts(template, variables);
          }
        }

        const result = `🔄 Workflow Execution: ${workflow.name}

📋 Description: ${workflow.description}

📍 Steps:
${workflow.steps.map((step, i) => `${i + 1}. ${step}`).join('\n')}

${reasoningResult ? `
🧠 Reasoning Framework Applied:
${reasoningResult.reasoning || reasoningResult.analysis}` : ''}

✅ Workflow ready for execution`;

        return {
          content: [{ type: 'text', text: result }]
        };
      }

      case 'create_custom_workflow': {
        customWorkflows[args.name] = {
          name: args.name,
          description: args.description,
          steps: args.steps,
          custom: true,
          created: new Date().toISOString()
        };

        return {
          content: [
            {
              type: 'text',
              text: `✅ Custom workflow '${args.name}' created successfully!

📋 Description: ${args.description}
📍 Steps: ${args.steps.length}

Use 'execute_workflow' with template_name: '${args.name}' to run this workflow.`
            }
          ]
        };
      }

      case 'chain_workflows': {
        const results = [];
        let currentContext = args.context || {};

        for (const workflowName of args.workflows) {
          const workflow = WORKFLOW_TEMPLATES_ENHANCED[workflowName] || customWorkflows[workflowName];
          
          if (!workflow) {
            results.push(`❌ Workflow '${workflowName}' not found`);
            continue;
          }

          results.push(`✅ ${workflow.name}: ${workflow.steps.length} steps`);
          
          // Pass context from one workflow to the next
          currentContext = { ...currentContext, previous: workflowName };
        }

        return {
          content: [
            {
              type: 'text',
              text: `⛓️ Workflow Chain Execution

Workflows to execute:
${results.join('\n')}

🔄 Total workflows: ${args.workflows.length}
📊 Total steps: ${results.filter(r => r.startsWith('✅')).reduce((acc, r) => acc + parseInt(r.match(/(\d+) steps/)[1]), 0)}

✅ Chain ready for execution`
            }
          ]
        };
      }

      case 'list_workflows': {
        const allWorkflows = { ...WORKFLOW_TEMPLATES_ENHANCED, ...customWorkflows };
        let result = `📚 Available Workflow Templates (${Object.keys(allWorkflows).length} total)\n\n`;

        for (const [key, workflow] of Object.entries(allWorkflows)) {
          result += `• ${workflow.name} (${key})\n`;
          result += `  📋 ${workflow.description}\n`;
          result += `  ⚙️ Steps: ${workflow.steps.length}`;
          result += workflow.reasoning ? ` | 🧠 ${workflow.reasoning}` : '';
          result += workflow.custom ? ' | 🎨 Custom' : '';
          result += '\n\n';
        }

        return {
          content: [{ type: 'text', text: result }]
        };
      }

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  } catch (error) {
    console.error('Tool execution error:', error);
    return {
      content: [
        {
          type: 'text',
          text: `Error: ${error.message}`
        }
      ],
      isError: true
    };
  }
});

// Start the server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('🚀 Enhanced Expert Role Prompt MCP Server v2.0 running');
  console.error(`📊 ${Object.values(EXPERT_ROLES_EXPANDED).reduce((acc, cat) => acc + Object.keys(cat).length, 0)} expert roles loaded`);
  console.error('🧠 Chain-of-Thought and Tree-of-Thoughts reasoning enabled');
  console.error('📈 Enhanced confidence scoring active');
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
