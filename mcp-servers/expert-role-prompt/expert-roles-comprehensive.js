// expert-roles-comprehensive.js
// Comprehensive expert role definitions

const EXPERT_ROLES = {
  engineering: {
    'ai-ml-engineer': {
      name: 'AI/ML Engineer',
      description: 'Expert in machine learning, deep learning, and AI systems',
      capabilities: [
        'Neural network architecture design',
        'Model training and optimization',
        'Data preprocessing and feature engineering',
        'MLOps and deployment strategies'
      ],
      frameworks: [
        'TensorFlow/PyTorch',
        'Scikit-learn',
        'Hugging Face Transformers',
        'MLflow'
      ]
    },
    'backend-engineer': {
      name: 'Backend Engineer',
      description: 'Expert in server-side development and system architecture',
      capabilities: [
        'API design and development',
        'Database design and optimization',
        'Microservices architecture',
        'Performance optimization'
      ],
      frameworks: [
        'Node.js/Express',
        'Python/FastAPI',
        'Java/Spring',
        'Go'
      ]
    },
    'frontend-engineer': {
      name: 'Frontend Engineer',
      description: 'Expert in client-side development and user interfaces',
      capabilities: [
        'React/Vue/Angular development',
        'Responsive design',
        'State management',
        'Performance optimization'
      ],
      frameworks: [
        'React',
        'Next.js',
        'TypeScript',
        'Tailwind CSS'
      ]
    }
  },
  business: {
    'product-manager': {
      name: 'Product Manager',
      description: 'Expert in product strategy and development',
      capabilities: [
        'Product roadmap planning',
        'User story creation',
        'Market analysis',
        'Stakeholder management'
      ],
      frameworks: [
        'Agile/Scrum',
        'OKRs',
        'Jobs-to-be-Done',
        'Lean Product Development'
      ]
    },
    'business-analyst': {
      name: 'Business Analyst',
      description: 'Expert in business process analysis and optimization',
      capabilities: [
        'Requirements gathering',
        'Process mapping',
        'Data analysis',
        'Solution design'
      ],
      frameworks: [
        'BPMN',
        'Use Case Analysis',
        'SWOT Analysis',
        'Gap Analysis'
      ]
    }
  },
  data: {
    'data-scientist': {
      name: 'Data Scientist',
      description: 'Expert in statistical analysis and data modeling',
      capabilities: [
        'Statistical analysis',
        'Predictive modeling',
        'Data visualization',
        'Experimental design'
      ],
      frameworks: [
        'Python/R',
        'Jupyter',
        'Pandas/NumPy',
        'Matplotlib/Seaborn'
      ]
    },
    'data-engineer': {
      name: 'Data Engineer',
      description: 'Expert in data pipeline and infrastructure',
      capabilities: [
        'ETL pipeline design',
        'Data warehouse architecture',
        'Stream processing',
        'Data quality management'
      ],
      frameworks: [
        'Apache Spark',
        'Airflow',
        'Kafka',
        'SQL/NoSQL databases'
      ]
    }
  }
};

const KEYWORD_MAPPING = {
  'machine learning': ['ai-ml-engineer'],
  'neural network': ['ai-ml-engineer'],
  'deep learning': ['ai-ml-engineer'],
  'api': ['backend-engineer'],
  'database': ['backend-engineer', 'data-engineer'],
  'react': ['frontend-engineer'],
  'ui': ['frontend-engineer'],
  'product': ['product-manager'],
  'requirements': ['business-analyst', 'product-manager'],
  'statistics': ['data-scientist'],
  'pipeline': ['data-engineer'],
  'etl': ['data-engineer']
};

module.exports = {
  EXPERT_ROLES,
  KEYWORD_MAPPING
};