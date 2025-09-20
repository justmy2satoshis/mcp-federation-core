// enhanced-keyword-mapping.js
// Enhanced keyword mappings with weights and semantic clusters

const WEIGHTED_KEYWORD_MAPPING = {
  ai_ml_engineer: {
    primary: {
      'machine learning': 10,
      'neural network': 10,
      'deep learning': 10,
      'tensorflow': 9,
      'pytorch': 9,
      'model training': 8,
      'ai': 7,
      'artificial intelligence': 8
    },
    secondary: {
      'data science': 5,
      'python': 4,
      'gpu': 5,
      'optimization': 4
    },
    negative: {
      'frontend': -5,
      'css': -5,
      'html': -5
    }
  },
  backend_engineer: {
    primary: {
      'api': 10,
      'backend': 10,
      'server': 9,
      'database': 9,
      'microservices': 8,
      'rest': 8,
      'graphql': 8
    },
    secondary: {
      'node': 5,
      'python': 4,
      'java': 4,
      'docker': 5
    },
    negative: {
      'ui': -5,
      'css': -5,
      'react': -3
    }
  },
  frontend_engineer: {
    primary: {
      'react': 10,
      'frontend': 10,
      'ui': 10,
      'user interface': 9,
      'component': 8,
      'css': 9,
      'html': 8
    },
    secondary: {
      'javascript': 5,
      'typescript': 5,
      'webpack': 4
    },
    negative: {
      'backend': -5,
      'database': -5,
      'server': -3
    }
  }
};

const SEMANTIC_CLUSTERS = {
  'ml_cluster': [
    'machine learning',
    'neural network',
    'deep learning',
    'training',
    'model'
  ],
  'web_backend_cluster': [
    'api',
    'rest',
    'graphql',
    'server',
    'endpoint'
  ],
  'web_frontend_cluster': [
    'react',
    'component',
    'ui',
    'interface',
    'design'
  ],
  'data_cluster': [
    'data',
    'pipeline',
    'etl',
    'warehouse',
    'analytics'
  ]
};

const CATEGORY_KEYWORDS = {
  engineering: [
    'code',
    'development',
    'programming',
    'software',
    'system',
    'architecture'
  ],
  business: [
    'product',
    'strategy',
    'management',
    'analysis',
    'requirements',
    'stakeholder'
  ],
  data: [
    'data',
    'analytics',
    'statistics',
    'pipeline',
    'warehouse',
    'modeling'
  ]
};

const COMMON_WORDS_PENALTY = {
  'the': 0.1,
  'is': 0.1,
  'at': 0.1,
  'which': 0.2,
  'on': 0.2,
  'a': 0.1,
  'an': 0.1,
  'and': 0.1,
  'or': 0.1,
  'but': 0.1,
  'in': 0.2,
  'with': 0.2,
  'for': 0.2,
  'to': 0.1,
  'of': 0.1
};

module.exports = {
  WEIGHTED_KEYWORD_MAPPING,
  SEMANTIC_CLUSTERS,
  CATEGORY_KEYWORDS,
  COMMON_WORDS_PENALTY
};