// confidence-scoring.js
// Enhanced confidence scoring system for expert role matching

class ConfidenceScoring {
  constructor() {
    // Weight factors for different matching criteria
    this.weights = {
      exact_match: 1.0,        // Exact keyword match
      semantic_match: 0.8,     // Semantic similarity
      category_match: 0.6,     // Category alignment
      capability_match: 0.7,   // Capability overlap
      context_relevance: 0.5,  // Context appropriateness
      domain_specificity: 0.9, // Domain-specific terms
      negative_match: -0.5     // Competing domain terms
    };

    // Confidence thresholds
    this.thresholds = {
      very_high: 80,
      high: 60,
      medium: 40,
      low: 20,
      very_low: 10
    };

    // Domain-specific term databases
    this.domainTerms = {
      'ai-ml-engineer': {
        primary: ['neural network', 'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'model training', 'AI', 'ML', 'artificial intelligence'],
        secondary: ['data science', 'algorithm', 'prediction', 'classification', 'regression'],
        negative: ['frontend', 'css', 'html', 'ui design']
      },
      'backend-engineer': {
        primary: ['api', 'database', 'server', 'backend', 'microservice', 'rest', 'graphql', 'sql'],
        secondary: ['architecture', 'performance', 'scalability', 'infrastructure'],
        negative: ['ui', 'frontend', 'css', 'design']
      },
      'frontend-engineer': {
        primary: ['react', 'vue', 'angular', 'frontend', 'ui', 'ux', 'javascript', 'typescript', 'css'],
        secondary: ['responsive', 'component', 'state management', 'dom'],
        negative: ['database', 'sql', 'server-side', 'infrastructure']
      },
      'devops-engineer': {
        primary: ['docker', 'kubernetes', 'ci/cd', 'jenkins', 'deployment', 'infrastructure', 'terraform'],
        secondary: ['automation', 'monitoring', 'pipeline', 'cloud'],
        negative: ['ui design', 'frontend', 'marketing']
      },
      'cloud-architect': {
        primary: ['aws', 'azure', 'gcp', 'cloud', 'serverless', 'lambda', 'vpc', 's3'],
        secondary: ['architecture', 'scalability', 'cost optimization', 'multi-region'],
        negative: ['frontend', 'ui', 'graphic design']
      },
      'data-scientist': {
        primary: ['statistics', 'data analysis', 'visualization', 'pandas', 'numpy', 'hypothesis testing'],
        secondary: ['python', 'r', 'jupyter', 'exploratory analysis'],
        negative: ['infrastructure', 'devops', 'frontend']
      },
      'product-manager': {
        primary: ['product', 'roadmap', 'user story', 'requirements', 'stakeholder', 'prioritization'],
        secondary: ['agile', 'scrum', 'metrics', 'kpi'],
        negative: ['code implementation', 'database design', 'infrastructure']
      },
      'cybersecurity-expert': {
        primary: ['security', 'vulnerability', 'penetration testing', 'encryption', 'firewall', 'threat'],
        secondary: ['compliance', 'audit', 'risk assessment', 'incident response'],
        negative: ['ui design', 'marketing', 'sales']
      },
      'prompt-engineer': {
        primary: ['prompt', 'llm', 'gpt', 'claude', 'chain of thought', 'few-shot', 'prompt optimization'],
        secondary: ['ai', 'language model', 'context window', 'token'],
        negative: ['infrastructure', 'database', 'devops']
      },
      'blockchain-developer': {
        primary: ['blockchain', 'smart contract', 'ethereum', 'solidity', 'web3', 'defi', 'crypto'],
        secondary: ['consensus', 'distributed', 'ledger', 'wallet'],
        negative: ['traditional database', 'centralized', 'ui design']
      }
    };

    // Semantic similarity clusters
    this.semanticClusters = {
      technical: ['engineer', 'developer', 'architect', 'programmer', 'coder'],
      business: ['manager', 'analyst', 'consultant', 'strategist', 'advisor'],
      creative: ['designer', 'artist', 'creator', 'producer', 'writer'],
      data: ['scientist', 'analyst', 'engineer', 'researcher', 'statistician'],
      leadership: ['manager', 'director', 'lead', 'head', 'chief']
    };
  }

  /**
   * Calculate confidence score for expert match
   * @param {string} expertId - The expert role ID
   * @param {string} query - The user query
   * @param {object} context - Additional context
   * @returns {object} - Confidence score and details
   */
  calculateConfidence(expertId, query, context = {}) {
    let score = 0;
    let matchDetails = {
      exact_matches: [],
      semantic_matches: [],
      capability_matches: [],
      negative_matches: [],
      factors: {}
    };

    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(/\s+/);

    // 1. Check exact domain term matches
    const domainData = this.domainTerms[expertId] || {};
    
    if (domainData.primary) {
      domainData.primary.forEach(term => {
        if (queryLower.includes(term.toLowerCase())) {
          score += 15 * this.weights.exact_match;
          matchDetails.exact_matches.push(term);
        }
      });
    }

    if (domainData.secondary) {
      domainData.secondary.forEach(term => {
        if (queryLower.includes(term.toLowerCase())) {
          score += 8 * this.weights.semantic_match;
          matchDetails.semantic_matches.push(term);
        }
      });
    }

    if (domainData.negative) {
      domainData.negative.forEach(term => {
        if (queryLower.includes(term.toLowerCase())) {
          score += 10 * this.weights.negative_match; // Negative impact
          matchDetails.negative_matches.push(term);
        }
      });
    }

    // 2. Check semantic cluster alignment
    const expertWords = expertId.split('-');
    for (const [cluster, terms] of Object.entries(this.semanticClusters)) {
      const clusterMatch = terms.some(term => 
        expertWords.some(word => word.includes(term)) ||
        queryWords.some(word => word.includes(term))
      );
      if (clusterMatch) {
        score += 10 * this.weights.semantic_match;
        matchDetails.factors.semantic_cluster = cluster;
      }
    }

    // 3. Context relevance scoring
    if (context.category) {
      const expertCategory = this.getExpertCategory(expertId);
      if (expertCategory === context.category) {
        score += 15 * this.weights.category_match;
        matchDetails.factors.category_match = true;
      }
    }

    // 4. Query complexity bonus
    const queryComplexity = this.assessQueryComplexity(query);
    if (queryComplexity > 0.7 && matchDetails.exact_matches.length > 0) {
      score += 10; // Bonus for complex queries with good matches
      matchDetails.factors.complexity_bonus = true;
    }

    // 5. Multi-term matching bonus
    if (matchDetails.exact_matches.length >= 3) {
      score += 15; // Strong signal with multiple matches
      matchDetails.factors.multi_match_bonus = true;
    }

    // 6. Capability relevance check
    if (context.capabilities) {
      const capabilityScore = this.checkCapabilityRelevance(expertId, context.capabilities);
      score += capabilityScore * this.weights.capability_match;
      matchDetails.factors.capability_score = capabilityScore;
    }

    // Normalize score to 0-100 range
    score = Math.max(0, Math.min(100, score));

    // Determine confidence level
    const confidenceLevel = this.getConfidenceLevel(score);

    return {
      expertId: expertId,
      score: Math.round(score),
      confidence: `${Math.round(score)}%`,
      level: confidenceLevel,
      matchDetails: matchDetails,
      reasoning: this.generateReasoning(score, matchDetails)
    };
  }

  /**
   * Assess query complexity
   */
  assessQueryComplexity(query) {
    const factors = {
      length: query.split(' ').length > 10 ? 0.3 : 0,
      technical_terms: /\b(api|database|algorithm|architecture|framework)\b/i.test(query) ? 0.3 : 0,
      specificity: /\b(specific|particular|exact|precise)\b/i.test(query) ? 0.2 : 0,
      multi_concept: (query.match(/\band\b/gi) || []).length > 1 ? 0.2 : 0
    };

    return Object.values(factors).reduce((a, b) => a + b, 0);
  }

  /**
   * Get expert category
   */
  getExpertCategory(expertId) {
    const categoryMap = {
      'ai-ml-engineer': 'engineering',
      'backend-engineer': 'engineering',
      'frontend-engineer': 'engineering',
      'devops-engineer': 'engineering',
      'cloud-architect': 'engineering',
      'data-scientist': 'data',
      'data-engineer': 'data',
      'product-manager': 'business',
      'business-analyst': 'business',
      'cybersecurity-expert': 'engineering',
      'blockchain-developer': 'engineering',
      'prompt-engineer': 'engineering',
      'ux-ui-designer': 'creative',
      'technical-writer': 'creative'
    };

    return categoryMap[expertId] || 'specialist';
  }

  /**
   * Check capability relevance
   */
  checkCapabilityRelevance(expertId, requiredCapabilities) {
    // This would check against actual expert capabilities
    // Simplified for demonstration
    const matchCount = requiredCapabilities.filter(cap => 
      expertId.toLowerCase().includes(cap.toLowerCase())
    ).length;

    return (matchCount / requiredCapabilities.length) * 20;
  }

  /**
   * Get confidence level description
   */
  getConfidenceLevel(score) {
    if (score >= this.thresholds.very_high) return 'VERY HIGH';
    if (score >= this.thresholds.high) return 'HIGH';
    if (score >= this.thresholds.medium) return 'MEDIUM';
    if (score >= this.thresholds.low) return 'LOW';
    return 'VERY LOW';
  }

  /**
   * Generate reasoning explanation
   */
  generateReasoning(score, matchDetails) {
    let reasoning = [];

    if (matchDetails.exact_matches.length > 0) {
      reasoning.push(`Strong domain alignment with terms: ${matchDetails.exact_matches.join(', ')}`);
    }

    if (matchDetails.semantic_matches.length > 0) {
      reasoning.push(`Related concepts identified: ${matchDetails.semantic_matches.join(', ')}`);
    }

    if (matchDetails.negative_matches.length > 0) {
      reasoning.push(`Competing domain indicators: ${matchDetails.negative_matches.join(', ')}`);
    }

    if (matchDetails.factors.category_match) {
      reasoning.push('Category alignment confirmed');
    }

    if (matchDetails.factors.complexity_bonus) {
      reasoning.push('Complex query with strong matches');
    }

    if (matchDetails.factors.multi_match_bonus) {
      reasoning.push('Multiple strong indicators present');
    }

    if (reasoning.length === 0) {
      reasoning.push('Limited matching indicators found');
    }

    return reasoning.join('. ') + '.';
  }

  /**
   * Compare multiple experts and rank by confidence
   */
  rankExperts(expertIds, query, context = {}) {
    const rankings = expertIds.map(expertId => 
      this.calculateConfidence(expertId, query, context)
    );

    return rankings.sort((a, b) => b.score - a.score);
  }

  /**
   * Get recommendation threshold
   */
  shouldRecommend(score) {
    return score >= this.thresholds.medium;
  }

  /**
   * Batch scoring for multiple queries
   */
  batchScore(expertId, queries) {
    return queries.map(query => 
      this.calculateConfidence(expertId, query)
    );
  }

  /**
   * Update domain terms dynamically
   */
  updateDomainTerms(expertId, terms) {
    if (!this.domainTerms[expertId]) {
      this.domainTerms[expertId] = { primary: [], secondary: [], negative: [] };
    }

    if (terms.primary) {
      this.domainTerms[expertId].primary.push(...terms.primary);
    }
    if (terms.secondary) {
      this.domainTerms[expertId].secondary.push(...terms.secondary);
    }
    if (terms.negative) {
      this.domainTerms[expertId].negative.push(...terms.negative);
    }
  }

  /**
   * Get confidence statistics
   */
  getStatistics() {
    return {
      total_experts: Object.keys(this.domainTerms).length,
      thresholds: this.thresholds,
      weights: this.weights,
      semantic_clusters: Object.keys(this.semanticClusters).length
    };
  }

  /**
   * Adaptive learning - update weights based on feedback
   */
  adaptWeights(feedback) {
    // This would implement weight adjustment based on user feedback
    // Simplified for demonstration
    if (feedback.accurate) {
      // Increase weights for factors that contributed
      for (const factor in feedback.factors) {
        if (this.weights[factor]) {
          this.weights[factor] = Math.min(1.0, this.weights[factor] * 1.1);
        }
      }
    } else {
      // Decrease weights for factors that contributed to wrong match
      for (const factor in feedback.factors) {
        if (this.weights[factor]) {
          this.weights[factor] = Math.max(0.1, this.weights[factor] * 0.9);
        }
      }
    }
  }
}

module.exports = { ConfidenceScoring };
