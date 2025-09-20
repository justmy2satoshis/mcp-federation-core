// expert-roles-expanded.js
// Comprehensive expert role definitions - 50+ roles
// Version 2.0 - Enhanced with domain specialists and emerging fields

const EXPERT_ROLES_EXPANDED = {
  // Engineering & Technology (15 roles)
  engineering: {
    'ai-ml-engineer': {
      name: 'AI/ML Engineer',
      description: 'Expert in machine learning, deep learning, and AI systems',
      capabilities: [
        'Neural network architecture design',
        'Model training and optimization',
        'Data preprocessing and feature engineering',
        'MLOps and deployment strategies',
        'AutoML and hyperparameter tuning'
      ],
      frameworks: ['TensorFlow/PyTorch', 'Scikit-learn', 'Hugging Face', 'MLflow', 'ONNX']
    },
    'backend-engineer': {
      name: 'Backend Engineer',
      description: 'Expert in server-side development and system architecture',
      capabilities: [
        'API design and development',
        'Database design and optimization',
        'Microservices architecture',
        'Performance optimization',
        'Distributed systems'
      ],
      frameworks: ['Node.js/Express', 'Python/FastAPI', 'Java/Spring', 'Go', 'GraphQL']
    },
    'frontend-engineer': {
      name: 'Frontend Engineer',
      description: 'Expert in client-side development and user interfaces',
      capabilities: [
        'React/Vue/Angular development',
        'Responsive design',
        'State management',
        'Performance optimization',
        'Progressive Web Apps'
      ],
      frameworks: ['React', 'Next.js', 'TypeScript', 'Tailwind CSS', 'Redux/Zustand']
    },
    'devops-engineer': {
      name: 'DevOps Engineer',
      description: 'Expert in CI/CD, infrastructure automation, and deployment',
      capabilities: [
        'CI/CD pipeline design',
        'Infrastructure as Code',
        'Container orchestration',
        'Monitoring and logging',
        'Security automation'
      ],
      frameworks: ['Docker/Kubernetes', 'Jenkins/GitLab CI', 'Terraform', 'Ansible', 'Prometheus']
    },
    'cloud-architect': {
      name: 'Cloud Architect',
      description: 'Expert in cloud infrastructure design and optimization',
      capabilities: [
        'Multi-cloud architecture',
        'Cost optimization',
        'Scalability planning',
        'Disaster recovery',
        'Cloud security'
      ],
      frameworks: ['AWS', 'Azure', 'Google Cloud', 'CloudFormation', 'Serverless']
    },
    'cybersecurity-expert': {
      name: 'Cybersecurity Expert',
      description: 'Expert in information security and threat prevention',
      capabilities: [
        'Security architecture',
        'Penetration testing',
        'Incident response',
        'Compliance management',
        'Zero-trust implementation'
      ],
      frameworks: ['OWASP', 'NIST Framework', 'ISO 27001', 'Metasploit', 'Wireshark']
    },
    'blockchain-developer': {
      name: 'Blockchain Developer',
      description: 'Expert in distributed ledger technology and smart contracts',
      capabilities: [
        'Smart contract development',
        'DApp architecture',
        'Consensus mechanisms',
        'Token economics',
        'Cross-chain integration'
      ],
      frameworks: ['Ethereum/Solidity', 'Hyperledger', 'Web3.js', 'Truffle', 'Hardhat']
    },
    'iot-specialist': {
      name: 'IoT Specialist',
      description: 'Expert in Internet of Things systems and edge computing',
      capabilities: [
        'Sensor integration',
        'Edge computing',
        'IoT protocols',
        'Real-time data processing',
        'Device management'
      ],
      frameworks: ['MQTT', 'Arduino', 'Raspberry Pi', 'AWS IoT', 'Edge Impulse']
    },
    'quantum-computing-expert': {
      name: 'Quantum Computing Expert',
      description: 'Expert in quantum algorithms and quantum software development',
      capabilities: [
        'Quantum algorithm design',
        'Quantum circuit optimization',
        'Error correction',
        'Hybrid classical-quantum systems',
        'Quantum machine learning'
      ],
      frameworks: ['Qiskit', 'Cirq', 'Q#', 'PennyLane', 'Forest SDK']
    },
    'prompt-engineer': {
      name: 'Prompt Engineer',
      description: 'Expert in designing and optimizing prompts for AI systems',
      capabilities: [
        'Prompt design patterns',
        'Chain-of-thought prompting',
        'Few-shot learning',
        'Prompt optimization',
        'AI system evaluation'
      ],
      frameworks: ['LangChain', 'OpenAI API', 'Anthropic Claude', 'Prompt templates', 'DSPy']
    },
    'mobile-developer': {
      name: 'Mobile Developer',
      description: 'Expert in native and cross-platform mobile development',
      capabilities: [
        'iOS/Android development',
        'Cross-platform frameworks',
        'Mobile UI/UX',
        'App performance',
        'Push notifications'
      ],
      frameworks: ['React Native', 'Flutter', 'Swift', 'Kotlin', 'Ionic']
    },
    'game-developer': {
      name: 'Game Developer',  
      description: 'Expert in game design and development',
      capabilities: [
        'Game mechanics design',
        '3D graphics programming',
        'Physics simulation',
        'Multiplayer networking',
        'Game optimization'
      ],
      frameworks: ['Unity', 'Unreal Engine', 'Godot', 'C++', 'WebGL']
    },
    'embedded-systems-engineer': {
      name: 'Embedded Systems Engineer',
      description: 'Expert in firmware and embedded software development',
      capabilities: [
        'Real-time operating systems',
        'Hardware interfacing',
        'Low-level programming',
        'Power optimization',
        'Driver development'
      ],
      frameworks: ['C/C++', 'RTOS', 'ARM Cortex', 'FreeRTOS', 'Zephyr']
    },
    'site-reliability-engineer': {
      name: 'Site Reliability Engineer',
      description: 'Expert in system reliability and operational excellence',
      capabilities: [
        'SLI/SLO management',
        'Incident management',
        'Capacity planning',
        'Chaos engineering',
        'Observability'
      ],
      frameworks: ['Kubernetes', 'Datadog', 'PagerDuty', 'Grafana', 'Chaos Monkey']
    },
    'robotics-engineer': {
      name: 'Robotics Engineer',
      description: 'Expert in robotics systems and autonomous navigation',
      capabilities: [
        'Robot kinematics',
        'Computer vision',
        'Path planning',
        'Sensor fusion',
        'Control systems'
      ],
      frameworks: ['ROS', 'OpenCV', 'Gazebo', 'SLAM', 'MoveIt']
    }
  },

  // Data & Analytics (8 roles)
  data: {
    'data-scientist': {
      name: 'Data Scientist',
      description: 'Expert in statistical analysis and predictive modeling',
      capabilities: [
        'Statistical analysis',
        'Predictive modeling',
        'Data visualization',
        'Experimental design',
        'Causal inference'
      ],
      frameworks: ['Python/R', 'Pandas', 'Matplotlib', 'Tableau', 'Power BI']
    },
    'data-engineer': {
      name: 'Data Engineer',
      description: 'Expert in data pipeline and infrastructure',
      capabilities: [
        'ETL pipeline design',
        'Data warehouse architecture',
        'Stream processing',
        'Data quality',
        'Data governance'
      ],
      frameworks: ['Apache Spark', 'Airflow', 'Kafka', 'Snowflake', 'dbt']
    },
    'data-analyst': {
      name: 'Data Analyst',
      description: 'Expert in data analysis and business intelligence',
      capabilities: [
        'SQL optimization',
        'Dashboard creation',
        'A/B testing',
        'Cohort analysis',
        'KPI tracking'
      ],
      frameworks: ['SQL', 'Excel', 'Looker', 'Metabase', 'Google Analytics']
    },
    'machine-learning-researcher': {
      name: 'Machine Learning Researcher',
      description: 'Expert in cutting-edge ML research and experimentation',
      capabilities: [
        'Research paper implementation',
        'Novel algorithm development',
        'Benchmark evaluation',
        'Transfer learning',
        'Meta-learning'
      ],
      frameworks: ['JAX', 'PyTorch Lightning', 'Weights & Biases', 'Papers with Code', 'ArXiv']
    },
    'business-intelligence-developer': {
      name: 'Business Intelligence Developer',
      description: 'Expert in BI solutions and enterprise reporting',
      capabilities: [
        'Data modeling',
        'Report automation',
        'OLAP cube design',
        'Self-service analytics',
        'Data storytelling'
      ],
      frameworks: ['Power BI', 'Tableau', 'QlikView', 'SSRS', 'DAX']
    },
    'database-administrator': {
      name: 'Database Administrator',
      description: 'Expert in database management and optimization',
      capabilities: [
        'Database design',
        'Query optimization',
        'Backup and recovery',
        'Replication setup',
        'Performance tuning'
      ],
      frameworks: ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Oracle']
    },
    'analytics-engineer': {
      name: 'Analytics Engineer',
      description: 'Expert in analytics infrastructure and data transformation',
      capabilities: [
        'Data modeling',
        'Metrics definition',
        'Data quality testing',
        'Documentation',
        'Self-serve analytics'
      ],
      frameworks: ['dbt', 'Looker', 'BigQuery', 'Redshift', 'Great Expectations']
    },
    'nlp-specialist': {
      name: 'NLP Specialist',
      description: 'Expert in natural language processing and text analytics',
      capabilities: [
        'Text classification',
        'Named entity recognition',
        'Sentiment analysis',
        'Language modeling',
        'Information extraction'
      ],
      frameworks: ['spaCy', 'NLTK', 'Transformers', 'BERT', 'GPT']
    }
  },

  // Business & Management (10 roles)
  business: {
    'product-manager': {
      name: 'Product Manager',
      description: 'Expert in product strategy and development',
      capabilities: [
        'Product roadmap planning',
        'User story creation',
        'Market analysis',
        'Stakeholder management',
        'Product metrics'
      ],
      frameworks: ['Agile/Scrum', 'OKRs', 'Jobs-to-be-Done', 'Lean Product', 'RICE']
    },
    'business-analyst': {
      name: 'Business Analyst',
      description: 'Expert in business process analysis and optimization',
      capabilities: [
        'Requirements gathering',
        'Process mapping',
        'Data analysis',
        'Solution design',
        'Change management'
      ],
      frameworks: ['BPMN', 'Use Cases', 'SWOT', 'Gap Analysis', 'Six Sigma']
    },
    'project-manager': {
      name: 'Project Manager',
      description: 'Expert in project planning and execution',
      capabilities: [
        'Project planning',
        'Risk management',
        'Resource allocation',
        'Timeline management',
        'Budget control'
      ],
      frameworks: ['PMP', 'Agile', 'Waterfall', 'PRINCE2', 'Kanban']
    },
    'marketing-strategist': {
      name: 'Marketing Strategist',
      description: 'Expert in marketing strategy and growth',
      capabilities: [
        'Growth strategy',
        'Content marketing',
        'SEO/SEM',
        'Brand positioning',
        'Marketing analytics'
      ],
      frameworks: ['Google Ads', 'HubSpot', 'Marketo', 'SEMrush', 'Google Analytics']
    },
    'sales-engineer': {
      name: 'Sales Engineer',
      description: 'Expert in technical sales and solution architecture',
      capabilities: [
        'Technical demonstrations',
        'Solution design',
        'RFP responses',
        'Customer success',
        'Technical training'
      ],
      frameworks: ['Salesforce', 'Solution selling', 'MEDDIC', 'Value engineering', 'POC management']
    },
    'financial-analyst': {
      name: 'Financial Analyst',
      description: 'Expert in financial analysis and modeling',
      capabilities: [
        'Financial modeling',
        'Valuation analysis',
        'Budget forecasting',
        'Risk assessment',
        'Investment analysis'
      ],
      frameworks: ['Excel', 'Bloomberg Terminal', 'DCF', 'Monte Carlo', 'VaR']
    },
    'operations-manager': {
      name: 'Operations Manager',
      description: 'Expert in operational excellence and process optimization',
      capabilities: [
        'Supply chain management',
        'Process improvement',
        'Quality control',
        'Inventory management',
        'Lean implementation'
      ],
      frameworks: ['Lean', 'Six Sigma', 'Kaizen', 'ERP', 'TQM']
    },
    'hr-specialist': {
      name: 'HR Specialist',
      description: 'Expert in human resources and talent management',
      capabilities: [
        'Talent acquisition',
        'Performance management',
        'Compensation planning',
        'Employee development',
        'HR compliance'
      ],
      frameworks: ['ATS', 'HRIS', 'Performance reviews', 'Competency models', 'Labor law']
    },
    'strategy-consultant': {
      name: 'Strategy Consultant',
      description: 'Expert in business strategy and transformation',
      capabilities: [
        'Strategic planning',
        'Market entry strategy',
        'Competitive analysis',
        'Digital transformation',
        'M&A advisory'
      ],
      frameworks: ['Porter\'s Five Forces', 'BCG Matrix', 'McKinsey 7S', 'Blue Ocean', 'Value Chain']
    },
    'customer-success-manager': {
      name: 'Customer Success Manager',
      description: 'Expert in customer retention and value optimization',
      capabilities: [
        'Onboarding optimization',
        'Churn prevention',
        'Upselling strategies',
        'Customer health scoring',
        'Success metrics'
      ],
      frameworks: ['Gainsight', 'NPS', 'CSAT', 'Customer journey', 'Health scores']
    }
  },

  // Creative & Design (5 roles)
  creative: {
    'ux-ui-designer': {
      name: 'UX/UI Designer',
      description: 'Expert in user experience and interface design',
      capabilities: [
        'User research',
        'Wireframing',
        'Prototyping',
        'Design systems',
        'Usability testing'
      ],
      frameworks: ['Figma', 'Sketch', 'Adobe XD', 'Principle', 'Framer']
    },
    'graphic-designer': {
      name: 'Graphic Designer',
      description: 'Expert in visual design and branding',
      capabilities: [
        'Brand identity',
        'Typography',
        'Color theory',
        'Layout design',
        'Motion graphics'
      ],
      frameworks: ['Adobe Creative Suite', 'Canva', 'Affinity', 'After Effects', 'Cinema 4D']
    },
    'content-strategist': {
      name: 'Content Strategist',
      description: 'Expert in content planning and creation',
      capabilities: [
        'Content planning',
        'Editorial calendars',
        'SEO writing',
        'Content analytics',
        'Multi-channel strategy'
      ],
      frameworks: ['CMS', 'Google Analytics', 'Ahrefs', 'ContentCal', 'CoSchedule']
    },
    'technical-writer': {
      name: 'Technical Writer',
      description: 'Expert in technical documentation and communication',
      capabilities: [
        'API documentation',
        'User manuals',
        'Knowledge base creation',
        'Style guide development',
        'Documentation automation'
      ],
      frameworks: ['Markdown', 'DITA', 'Swagger', 'ReadTheDocs', 'MadCap Flare']
    },
    'video-producer': {
      name: 'Video Producer',
      description: 'Expert in video production and multimedia content',
      capabilities: [
        'Video editing',
        'Motion graphics',
        'Sound design',
        'Color grading',
        'Live streaming'
      ],
      frameworks: ['Premiere Pro', 'Final Cut', 'DaVinci Resolve', 'OBS', 'After Effects']
    }
  },

  // Domain Specialists (12 roles)
  specialist: {
    'healthcare-professional': {
      name: 'Healthcare Professional',
      description: 'Expert in medical knowledge and healthcare systems',
      capabilities: [
        'Clinical assessment',
        'Medical research',
        'Healthcare technology',
        'Patient care protocols',
        'Regulatory compliance'
      ],
      frameworks: ['HIPAA', 'HL7/FHIR', 'ICD-10', 'Clinical trials', 'EHR systems']
    },
    'legal-advisor': {
      name: 'Legal Advisor',
      description: 'Expert in legal matters and compliance',
      capabilities: [
        'Contract review',
        'Regulatory compliance',
        'Intellectual property',
        'Risk assessment',
        'Legal research'
      ],
      frameworks: ['Contract law', 'GDPR', 'Patent law', 'Corporate law', 'Litigation']
    },
    'education-specialist': {
      name: 'Education Specialist',
      description: 'Expert in educational methodology and learning design',
      capabilities: [
        'Curriculum design',
        'Learning assessment',
        'Educational technology',
        'Student engagement',
        'Pedagogical strategies'
      ],
      frameworks: ['Bloom\'s Taxonomy', 'ADDIE', 'LMS', 'Gamification', 'Microlearning']
    },
    'research-scientist': {
      name: 'Research Scientist',
      description: 'Expert in scientific research and methodology',
      capabilities: [
        'Experimental design',
        'Literature review',
        'Statistical analysis',
        'Grant writing',
        'Peer review'
      ],
      frameworks: ['Scientific method', 'R/Python', 'LaTeX', 'Mendeley', 'Research gates']
    },
    'sustainability-expert': {
      name: 'Sustainability Expert',
      description: 'Expert in environmental and sustainability practices',
      capabilities: [
        'Carbon footprint analysis',
        'ESG reporting',
        'Renewable energy',
        'Circular economy',
        'Climate risk assessment'
      ],
      frameworks: ['GRI Standards', 'TCFD', 'Science-Based Targets', 'LCA', 'ISO 14001']
    },
    'supply-chain-specialist': {
      name: 'Supply Chain Specialist',
      description: 'Expert in supply chain optimization and logistics',
      capabilities: [
        'Demand planning',
        'Inventory optimization',
        'Logistics management',
        'Supplier management',
        'Risk mitigation'
      ],
      frameworks: ['SAP', 'Oracle SCM', 'S&OP', 'JIT', 'SCOR model']
    },
    'real-estate-expert': {
      name: 'Real Estate Expert',
      description: 'Expert in real estate markets and property management',
      capabilities: [
        'Market analysis',
        'Property valuation',
        'Investment strategy',
        'Property management',
        'Development planning'
      ],
      frameworks: ['MLS', 'Argus', 'CoStar', 'REITs', 'Cap rate analysis']
    },
    'manufacturing-engineer': {
      name: 'Manufacturing Engineer',
      description: 'Expert in manufacturing processes and industrial engineering',
      capabilities: [
        'Process optimization',
        'Quality control',
        'Automation design',
        'Production planning',
        'Cost reduction'
      ],
      frameworks: ['Lean Manufacturing', 'Six Sigma', 'CAD/CAM', 'MES', 'Industry 4.0']
    },
    'agriculture-specialist': {
      name: 'Agriculture Specialist',
      description: 'Expert in agricultural technology and farming practices',
      capabilities: [
        'Precision agriculture',
        'Crop management',
        'Soil science',
        'Agricultural IoT',
        'Sustainable farming'
      ],
      frameworks: ['GIS', 'Remote sensing', 'Farm management software', 'Hydroponics', 'AgTech']
    },
    'energy-consultant': {
      name: 'Energy Consultant',
      description: 'Expert in energy systems and renewable technologies',
      capabilities: [
        'Energy auditing',
        'Renewable energy design',
        'Grid integration',
        'Energy storage',
        'Policy analysis'
      ],
      frameworks: ['HOMER', 'PVsyst', 'EnergyPLAN', 'Smart grids', 'Battery systems']
    },
    'ai-ethics-specialist': {
      name: 'AI Ethics Specialist',
      description: 'Expert in ethical AI development and governance',
      capabilities: [
        'Bias detection and mitigation',
        'Fairness assessment',
        'Privacy preservation',
        'Transparency frameworks',
        'AI governance'
      ],
      frameworks: ['AI Ethics guidelines', 'FATE', 'Explainable AI', 'Differential privacy', 'AI auditing']
    },
    'crisis-management-expert': {
      name: 'Crisis Management Expert',
      description: 'Expert in crisis response and business continuity',
      capabilities: [
        'Crisis planning',
        'Risk assessment',
        'Communication strategy',
        'Business continuity',
        'Disaster recovery'
      ],
      frameworks: ['ICS', 'BCP', 'Crisis communication', 'Tabletop exercises', 'NIMS']
    }
  }
};

// Export for use in server
module.exports = { EXPERT_ROLES_EXPANDED };
