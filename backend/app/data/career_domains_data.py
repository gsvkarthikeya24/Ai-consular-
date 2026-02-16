"""
Comprehensive Career Domains Data for AI Consular System
Contains 30+ engineering career paths with detailed requirements, roadmaps, and guidance
"""

CAREER_DOMAINS = {
    # ============================================================================
    # SOFTWARE & AI DOMAINS
    # ============================================================================
    
    "full_stack_developer": {
        "domain_id": "full_stack_developer",
        "title": "Full Stack Web Developer",
        "category": "Software & AI",
        "description": "Build complete web applications handling both frontend and backend development. Work with modern frameworks and databases to create scalable solutions.",
        "required_education": ["B.Tech/BE in CS/IT/ECE", "MCA", "Self-taught with strong portfolio"],
        "key_skills": [
            {"name": "JavaScript/TypeScript", "level": "Advanced"},
            {"name": "React/Vue/Angular", "level": "Advanced"},
            {"name": "Node.js/Python/Java", "level": "Intermediate"},
            {"name": "SQL/NoSQL Databases", "level": "Intermediate"},
            {"name": "REST APIs", "level": "Advanced"},
            {"name": "Git/GitHub", "level": "Intermediate"},
            {"name": "Docker/Kubernetes", "level": "Basic"},
            {"name": "Cloud Platforms (AWS/Azure)", "level": "Basic"}
        ],
        "certifications": [
            "AWS Certified Developer",
            "Meta Front-End Developer",
            "Google Cloud Professional",
            "Microsoft Certified: Azure Developer"
        ],
        "roadmap_phases": [
            {
                "phase": "Foundation (Months 1-3)",
                "duration": "3 months",
                "focus": "HTML, CSS, JavaScript fundamentals. Build static websites. Learn Git basics."
            },
            {
                "phase": "Frontend Mastery (Months 4-6)",
                "duration": "3 months",
                "focus": "React.js, state management (Redux), responsive design, API integration."
            },
            {
                "phase": "Backend Development (Months 7-10)",
                "duration": "4 months",
                "focus": "Node.js/Express or Python/FastAPI. Database design (MongoDB, PostgreSQL). Authentication (JWT)."
            },
            {
                "phase": "Full Stack Projects (Months 11-12)",
                "duration": "2 months",
                "focus": "Build 2-3 complete applications. Deploy to cloud. Add to portfolio."
            }
        ],
        "entry_requirements": {
            "degree": "Not mandatory (portfolio-driven)",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹3-6 LPA",
            "mid_level": "₹8-15 LPA",
            "senior": "₹18-35 LPA"
        },
        "top_companies": ["Google", "Amazon", "Microsoft", "Flipkart", "Zomato", "Swiggy", "Razorpay", "CRED"],
        "job_market_outlook": "High demand (500K+ openings annually in India)",
        "keywords_for_ats": ["React", "Node.js", "JavaScript", "API", "MongoDB", "PostgreSQL", "AWS", "Docker", "Git"]
    },
    
    "ai_engineer": {
        "domain_id": "ai_engineer",
        "title": "AI Engineer (Applied AI Developer)",
        "category": "Software & AI",
        "description": "Build AI-powered features within products using existing APIs, LLMs, and RAG (Retrieval-Augmented Generation). Bridge the gap between model development and real-world application.",
        "required_education": ["B.Tech in CS/IT/ECE", "M.Tech in AI/ML preferred"],
        "key_skills": [
            {"name": "Python", "level": "Advanced"},
            {"name": "OpenAI/Gemini/Claude APIs", "level": "Advanced"},
            {"name": "LangChain/LlamaIndex", "level": "Intermediate"},
            {"name": "RAG (Retrieval-Augmented Generation)", "level": "Advanced"},
            {"name": "Vector Databases (Pinecone, Weaviate)", "level": "Intermediate"},
            {"name": "Prompt Engineering", "level": "Advanced"},
            {"name": "FastAPI/Flask", "level": "Intermediate"},
            {"name": "Cloud ML Services", "level": "Basic"}
        ],
        "certifications": [
            "DeepLearning.AI LLM Specialization",
            "AWS Machine Learning Specialty",
            "Google Cloud ML Engineer"
        ],
        "roadmap_phases": [
            {
                "phase": "Python & ML Basics (Months 1-2)",
                "duration": "2 months",
                "focus": "Python advanced concepts. NumPy, Pandas. Basic ML concepts."
            },
            {
                "phase": "LLM API Integration (Months 3-4)",
                "duration": "2 months",
                "focus": "OpenAI API, Gemini API. Prompt engineering. Build chatbot applications."
            },
            {
                "phase": "RAG & Vector DBs (Months 5-7)",
                "duration": "3 months",
                "focus": "Implement RAG pipelines. Work with embeddings. Use Pinecone/Weaviate."
            },
            {
                "phase": "Production AI Apps (Months 8-10)",
                "duration": "3 months",
                "focus": "Deploy AI features. LangChain orchestration. Build 2-3 production apps."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT/ECE",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹6-12 LPA",
            "mid_level": "₹15-30 LPA",
            "senior": "₹35-60 LPA"
        },
        "top_companies": ["OpenAI", "Google", "Microsoft", "Anthropic", "Perplexity", "Vercel", "Indian AI startups"],
        "job_market_outlook": "Exploding demand (GenAI revolution)",
        "keywords_for_ats": ["LLM", "RAG", "Prompt Engineering", "OpenAI", "LangChain", "Vector DB", "Python", "AI"]
    },
    
    "ml_engineer": {
        "domain_id": "ml_engineer",
        "title": "Machine Learning Engineer",
        "category": "Software & AI",
        "description": "Focus on training, optimizing, and deploying predictive models at scale. Handle the full lifecycle from data preparation to production deployment.",
        "required_education": ["B.Tech in CS/IT/ECE with strong math", "M.Tech in AI/ML preferred for research roles"],
        "key_skills": [
            {"name": "Python", "level": "Advanced"},
            {"name": "TensorFlow/PyTorch", "level": "Advanced"},
            {"name": "scikit-learn", "level": "Advanced"},
            {"name": "Feature Engineering", "level": "Advanced"},
            {"name": "Model Optimization", "level": "Intermediate"},
            {"name": "Statistics & Probability", "level": "Advanced"},
            {"name": "SQL & Data Pipelines", "level": "Intermediate"},
            {"name": "MLOps Tools", "level": "Basic"}
        ],
        "certifications": [
            "TensorFlow Developer Certificate",
            "AWS Machine Learning Specialty",
            "Coursera ML Specialization (Andrew Ng)",
            "Fast.ai Practical Deep Learning"
        ],
        "roadmap_phases": [
            {
                "phase": "Math & Python (Months 1-3)",
                "duration": "3 months",
                "focus": "Linear algebra, calculus, statistics. Python for data science (NumPy, Pandas, Matplotlib)."
            },
            {
                "phase": "Classical ML (Months 4-6)",
                "duration": "3 months",
                "focus": "Supervised & unsupervised learning. scikit-learn. Kaggle competitions (beginner)."
            },
            {
                "phase": "Deep Learning (Months 7-10)",
                "duration": "4 months",
                "focus": "Neural networks. TensorFlow/PyTorch. CNNs, RNNs, Transformers basics."
            },
            {
                "phase": "Production ML (Months 11-12)",
                "duration": "2 months",
                "focus": "Model deployment. API creation. MLflow for tracking. Portfolio projects."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech with strong math background",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹6-10 LPA",
            "mid_level": "₹12-25 LPA",
            "senior": "₹30-50 LPA"
        },
        "top_companies": ["Google", "Microsoft", "Amazon", "Netflix", "Uber", "PhonePe", "Razorpay", "Flipkart"],
        "job_market_outlook": "Very high demand",
        "keywords_for_ats": ["Machine Learning", "Python", "TensorFlow", "PyTorch", "scikit-learn", "Deep Learning", "Model Deployment"]
    },
    
    "genai_llm_engineer": {
        "domain_id": "genai_llm_engineer",
        "title": "Generative AI / LLM Engineer",
        "category": "Software & AI",
        "description": "Specialize in building and fine-tuning Large Language Model systems, prompt engineering, and embedding-driven applications.",
        "required_education": ["B.Tech CS/IT", "M.Tech AI/ML/NLP preferred"],
        "key_skills": [
            {"name": "Python", "level": "Advanced"},
            {"name": "Transformer Architecture", "level": "Advanced"},
            {"name": "Hugging Face Transformers", "level": "Advanced"},
            {"name": "Fine-tuning (LoRA, QLoRA)", "level": "Advanced"},
            {"name": "Prompt Engineering", "level": "Advanced"},
            {"name": "LangChain/LlamaIndex", "level": "Advanced"},
            {"name": "Vector Embeddings", "level": "Advanced"},
            {"name": "GPU Computing (CUDA)", "level": "Intermediate"}
        ],
        "certifications": [
            "DeepLearning.AI Generative AI Specialization",
            "Hugging Face Course",
            "Stanford CS224N (NLP)",
            "Fast.ai Part 2"
        ],
        "roadmap_phases": [
            {
                "phase": "NLP Foundations (Months 1-3)",
                "duration": "3 months",
                "focus": "Text preprocessing, tokenization, word embeddings (Word2Vec, GloVe)."
            },
            {
                "phase": "Transformer Deep Dive (Months 4-6)",
                "duration": "3 months",
                "focus": "Attention mechanism, BERT, GPT architecture. Hugging Face library."
            },
            {
                "phase": "LLM Fine-Tuning (Months 7-9)",
                "duration": "3 months",
                "focus": "LoRA, QLoRA, PEFT techniques. Fine-tune open-source models (Llama, Mistral)."
            },
            {
                "phase": "Production LLM Systems (Months 10-12)",
                "duration": "3 months",
                "focus": "Build RAG pipelines. Optimize inference. Deploy LLM apps. Portfolio projects."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹8-15 LPA",
            "mid_level": "₹18-35 LPA",
            "senior": "₹40-75 LPA"
        },
        "top_companies": ["OpenAI", "Anthropic", "Google DeepMind", "Meta AI", "Cohere", "Hugging Face", "Indian AI startups"],
        "job_market_outlook": "Explosive growth (2024-2026 boom)",
        "keywords_for_ats": ["LLM", "Fine-tuning", "Transformers", "GPT", "BERT", "Hugging Face", "RAG", "Prompt Engineering"]
    },
    
    "mlops_engineer": {
        "domain_id": "mlops_engineer",
        "title": "MLOps Engineer",
        "category": "Software & AI",
        "description": "Focus on infrastructure, CI/CD pipelines, containerization (Docker, Kubernetes), and monitoring models in production to ensure reliability.",
        "required_education": ["B.Tech CS/IT/ECE", "Strong DevOps + ML background"],
        "key_skills": [
            {"name": "Python", "level": "Advanced"},
            {"name": "Docker/Kubernetes", "level": "Advanced"},
            {"name": "CI/CD (Jenkins, GitHub Actions)", "level": "Advanced"},
            {"name": "MLflow/Kubeflow", "level": "Advanced"},
            {"name": "Cloud Platforms (AWS/GCP/Azure)", "level": "Advanced"},
            {"name": "Terraform/Ansible", "level": "Intermediate"},
            {"name": "Monitoring (Prometheus, Grafana)", "level": "Intermediate"},
            {"name": "ML Frameworks", "level": "Basic"}
        ],
        "certifications": [
            "AWS Machine Learning Specialty",
            "Kubernetes (CKA)",
            "Terraform Associate",
            "MLOps Specialization (Coursera)"
        ],
        "roadmap_phases": [
            {
                "phase": "DevOps Fundamentals (Months 1-3)",
                "duration": "3 months",
                "focus": "Linux, Docker, CI/CD basics, Git workflows."
            },
            {
                "phase": "Cloud & Kubernetes (Months 4-6)",
                "duration": "3 months",
                "focus": "AWS/GCP services, Kubernetes orchestration, container management."
            },
            {
                "phase": "ML Pipeline Automation (Months 7-9)",
                "duration": "3 months",
                "focus": "MLflow, Kubeflow, model versioning, experiment tracking."
            },
            {
                "phase": "Production Monitoring (Months 10-12)",
                "duration": "3 months",
                "focus": "Model monitoring, A/B testing, drift detection, alerting systems."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹6-12 LPA",
            "mid_level": "₹15-28 LPA",
            "senior": "₹30-55 LPA"
        },
        "top_companies": ["Google", "Amazon", "Microsoft", "Netflix", "Uber", "Airbnb", "PhonePe"],
        "job_market_outlook": "High demand (critical for ML scalability)",
        "keywords_for_ats": ["MLOps", "Kubernetes", "Docker", "CI/CD", "MLflow", "AWS", "Model Deployment", "DevOps"]
    },
    
    "data_scientist": {
        "domain_id": "data_scientist",
        "title": "Data Scientist",
        "category": "Software & AI",
        "description": "Analyze complex data to extract insights, build predictive models, and drive data-driven business decisions.",
        "required_education": ["B.Tech/BE with strong math/stats", "M.Tech/MS in Data Science preferred"],
        "key_skills": [
            {"name": "Python/R", "level": "Advanced"},
            {"name": "SQL", "level": "Advanced"},
            {"name": "Statistics & Probability", "level": "Advanced"},
            {"name": "Machine Learning", "level": "Advanced"},
            {"name": "Data Visualization (Tableau, PowerBI)", "level": "Intermediate"},
            {"name": "Pandas, NumPy", "level": "Advanced"},
            {"name": "Scikit-learn", "level": "Advanced"},
            {"name": "Business Acumen", "level": "Intermediate"}
        ],
        "certifications": [
            "IBM Data Science Professional",
            "Google Data Analytics",
            "Microsoft Certified: Azure Data Scientist",
            "Kaggle (Competitions Master)"
        ],
        "roadmap_phases": [
            {
                "phase": "Statistics & Python (Months 1-3)",
                "duration": "3 months",
                "focus": "Descriptive & inferential statistics. Python for data analysis (Pandas, NumPy)."
            },
            {
                "phase": "Data Analysis & Visualization (Months 4-5)",
                "duration": "2 months",
                "focus": "SQL mastery. Create dashboards with Tableau/PowerBI. EDA best practices."
            },
            {
                "phase": "Machine Learning (Months 6-9)",
                "duration": "4 months",
                "focus": "Supervised/unsupervised learning. Model evaluation. Feature engineering."
            },
            {
                "phase": "Business Projects (Months 10-12)",
                "duration": "3 months",
                "focus": "Work on real business case studies. Build portfolio. Kaggle competitions."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech with strong quantitative skills",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹5-10 LPA",
            "mid_level": "₹12-22 LPA",
            "senior": "₹25-45 LPA"
        },
        "top_companies": ["Google", "Amazon", "Flipkart", "Walmart", "Accenture", "Deloitte", "McKinsey", "BCG"],
        "job_market_outlook": "High demand",
        "keywords_for_ats": ["Data Science", "Python", "SQL", "Machine Learning", "Statistics", "Pandas", "Visualization"]
    },
    
    "data_analyst": {
        "domain_id": "data_analyst",
        "title": "Data Analyst",
        "category": "Software & AI",
        "description": "Transform raw data into meaningful insights through visualization, reporting, and statistical analysis.",
        "required_education": ["B.Tech/BE any branch", "BCA/MCA", "Commerce with analytics certs"],
        "key_skills": [
            {"name": "SQL", "level": "Advanced"},
            {"name": "Excel (Advanced)", "level": "Advanced"},
            {"name": "Tableau/PowerBI", "level": "Advanced"},
            {"name": "Python (Basic)", "level": "Basic"},
            {"name": "Statistics", "level": "Intermediate"},
            {"name": "Data Cleaning", "level": "Advanced"},
            {"name": "Business Intelligence", "level": "Intermediate"}
        ],
        "certifications": [
            "Google Data Analytics Professional",
            "Microsoft Power BI Data Analyst",
            "Tableau Desktop Specialist",
            "Excel Expert Certification"
        ],
        "roadmap_phases": [
            {
                "phase": "Excel & SQL (Months 1-2)",
                "duration": "2 months",
                "focus": "Advanced Excel (pivot tables, VLOOKUP). SQL queries, joins, aggregations."
            },
            {
                "phase": "Visualization Tools (Months 3-5)",
                "duration": "3 months",
                "focus": "Master Tableau or PowerBI. Create interactive dashboards. Tell data stories."
            },
            {
                "phase": "Python for Analysis (Months 6-7)",
                "duration": "2 months",
                "focus": "Pandas for data manipulation. Basic statistical analysis."
            },
            {
                "phase": "Portfolio Projects (Months 8-10)",
                "duration": "3 months",
                "focus": "Analyze real datasets. Build dashboards. Document insights."
            }
        ],
        "entry_requirements": {
            "degree": "Not mandatory (certification sufficient)",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹3-6 LPA",
            "mid_level": "₹7-14 LPA",
            "senior": "₹16-28 LPA"
        },
        "top_companies": ["Accenture", "Deloitte", "EY", "KPMG", "Flipkart", "Amazon", "Swiggy", "Zomato"],
        "job_market_outlook": "Very high demand (entry-friendly)",
        "keywords_for_ats": ["SQL", "Tableau", "PowerBI", "Excel", "Data Analysis", "Visualization", "Python"]
    },
    
    "data_engineer": {
        "domain_id": "data_engineer",
        "title": "Data Engineer",
        "category": "Software & AI",
        "description": "Build and maintain data pipelines, ETL processes, and data infrastructure to enable analytics and ML.",
        "required_education": ["B.Tech CS/IT/ECE", "Strong programming background"],
        "key_skills": [
            {"name": "Python/Java/Scala", "level": "Advanced"},
            {"name": "SQL", "level": "Advanced"},
            {"name": "Apache Spark", "level": "Advanced"},
            {"name": "Airflow/Prefect", "level": "Intermediate"},
            {"name": "Cloud Data Services (AWS/GCP)", "level": "Advanced"},
            {"name": "Data Warehousing (Snowflake, Redshift)", "level": "Intermediate"},
            {"name": "Kafka/RabbitMQ", "level": "Basic"},
            {"name": "Docker/Kubernetes", "level": "Basic"}
        ],
        "certifications": [
            "AWS Data Analytics Specialty",
            "Google Cloud Professional Data Engineer",
            "Databricks Certified",
            "Snowflake SnowPro"
        ],
        "roadmap_phases": [
            {
                "phase": "Programming & SQL (Months 1-3)",
                "duration": "3 months",
                "focus": "Python advanced concepts. Complex SQL (window functions, CTEs)."
            },
            {
                "phase": "ETL & Pipelines (Months 4-6)",
                "duration": "3 months",
                "focus": "Apache Airflow. Build ETL workflows. Data transformation best practices."
            },
            {
                "phase": "Big Data Tools (Months 7-9)",
                "duration": "3 months",
                "focus": "Apache Spark. Process large datasets. Work with distributed systems."
            },
            {
                "phase": "Cloud Data Engineering (Months 10-12)",
                "duration": "3 months",
                "focus": "AWS/GCP data services. Snowflake. Build production data pipelines."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹5-9 LPA",
            "mid_level": "₹12-24 LPA",
            "senior": "₹28-50 LPA"
        },
        "top_companies": ["Google", "Amazon", "Flipkart", "Uber", "Netflix", "Airbnb", "PhonePe", "Razorpay"],
        "job_market_outlook": "Very high demand (critical role)",
        "keywords_for_ats": ["Data Engineering", "ETL", "SQL", "Python", "Spark", "Airflow", "AWS", "Snowflake"]
    },
    
    "computer_vision_engineer": {
        "domain_id": "computer_vision_engineer",
        "title": "Computer Vision Engineer",
        "category": "Software & AI",
        "description": "Specialize in training models to interpret visual data (images/videos) for applications like autonomous vehicles, medical imaging, and surveillance.",
        "required_education": ["B.Tech CS/IT/ECE", "M.Tech in CV/AI preferred"],
        "key_skills": [
            {"name": "Python", "level": "Advanced"},
            {"name": "OpenCV", "level": "Advanced"},
            {"name": "TensorFlow/PyTorch", "level": "Advanced"},
            {"name": "CNNs (ResNet, YOLO, etc.)", "level": "Advanced"},
            {"name": "Image Processing", "level": "Advanced"},
            {"name": "Object Detection", "level": "Advanced"},
            {"name": "C++ (Performance)", "level": "Intermediate"}
        ],
        "certifications": [
            "Stanford CS231n (Convolutional Neural Networks)",
            "Deep Learning Specialization",
            "OpenCV Bootcamp"
        ],
        "roadmap_phases": [
            {
                "phase": "Image Processing Basics (Months 1-2)",
                "duration": "2 months",
                "focus": "OpenCV fundamentals. Image transformations, filtering, edge detection."
            },
            {
                "phase": "Deep Learning for CV (Months 3-6)",
                "duration": "4 months",
                "focus": "CNNs architecture. Transfer learning. Image classification projects."
            },
            {
                "phase": "Advanced CV (Months 7-10)",
                "duration": "4 months",
                "focus": "Object detection (YOLO, Faster R-CNN). Semantic segmentation. Video analysis."
            },
            {
                "phase": "Deployment (Months 11-12)",
                "duration": "2 months",
                "focus": "Optimize models (TensorRT). Deploy on edge devices. Portfolio projects."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT/ECE",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹6-12 LPA",
            "mid_level": "₹15-30 LPA",
            "senior": "₹35-60 LPA"
        },
        "top_companies": ["Tesla", "Waymo", "Nvidia", "Google", "Microsoft", "Amazon", "Healthcare AI startups"],
        "job_market_outlook": "Growing (autonomous vehicles, healthcare AI)",
        "keywords_for_ats": ["Computer Vision", "OpenCV", "YOLO", "CNNs", "Object Detection", "PyTorch", "Image Processing"]
    },
    
    "nlp_engineer": {
        "domain_id": "nlp_engineer",
        "title": "NLP Engineer (Natural Language Processing)",
        "category": "Software & AI",
        "description": "Build systems that understand and generate human language - chatbots, voice AI, translation, sentiment analysis.",
        "required_education": ["B.Tech CS/IT", "M.Tech in NLP/AI preferred"],
        "key_skills": [
            {"name": "Python", "level": "Advanced"},
            {"name": "NLTK/spaCy", "level": "Advanced"},
            {"name": "Transformers (BERT, GPT)", "level": "Advanced"},
            {"name": "Hugging Face", "level": "Advanced"},
            {"name": "Text Preprocessing", "level": "Advanced"},
            {"name": "Named Entity Recognition", "level": "Intermediate"},
            {"name": "Sentiment Analysis", "level": "Intermediate"}
        ],
        "certifications": [
            "Stanford CS224N (NLP)",
            "DeepLearning.AI NLP Specialization",
            "Hugging Face Course"
        ],
        "roadmap_phases": [
            {
                "phase": "Text Processing (Months 1-2)",
                "duration": "2 months",
                "focus": "Tokenization, stemming, lemmatization. Regular expressions. NLTK/spaCy."
            },
            {
                "phase": "Classical NLP (Months 3-4)",
                "duration": "2 months",
                "focus": "TF-IDF, word embeddings (Word2Vec). Build text classifiers."
            },
            {
                "phase": "Transformers (Months 5-8)",
                "duration": "4 months",
                "focus": "BERT, GPT architecture. Fine-tune for tasks (classification, NER)."
            },
            {
                "phase": "Production NLP (Months 9-12)",
                "duration": "4 months",
                "focus": "Build chatbots. Deploy NLP models. Work with LLM APIs."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹6-11 LPA",
            "mid_level": "₹14-28 LPA",
            "senior": "₹32-55 LPA"
        },
        "top_companies": ["Google", "Microsoft", "Amazon Alexa", "Apple Siri", "Indian AI startups", "Chatbot companies"],
        "job_market_outlook": "High demand (voice AI, chatbots boom)",
        "keywords_for_ats": ["NLP", "BERT", "Transformers", "Hugging Face", "Text Processing", "Chatbot", "Python"]
    },
    
    # ============================================================================
    # CYBERSECURITY & BANKING DOMAINS
    # ============================================================================
    
    "banking_security_engineer": {
        "domain_id": "banking_security_engineer",
        "title": "Banking Security Engineer",
        "category": "Cybersecurity & Banking",
        "description": "Protect financial assets, customer data, and digital infrastructure in banking. Requires deep technical expertise and strong regulatory compliance knowledge.",
        "required_education": ["B.Tech CS/IT/ECE", "M.Tech in Cybersecurity preferred"],
        "key_skills": [
            {"name": "Identity and Access Management (IAM)", "level": "Advanced"},
            {"name": "Privileged Access Management (PAM)", "level": "Advanced"},
            {"name": "Multi-Factor Authentication (MFA)", "level": "Intermediate"},
            {"name": "Network Security (Firewalls, IDS/IPS)", "level": "Advanced"},
            {"name": "Cloud Security (AWS/Azure/GCP)", "level": "Advanced"},
            {"name": "CSPM (Cloud Security Posture Management)", "level": "Intermediate"},
            {"name": "Application Security (OWASP Top 10)", "level": "Advanced"},
            {"name": "Cryptography & PKI", "level": "Advanced"},
            {"name": "SIEM (Splunk, ELK)", "level": "Intermediate"},
            {"name": "PCI-DSS Compliance", "level": "Advanced"},
            {"name": "ISO 27001/27002", "level": "Intermediate"},
            {"name": "Python/PowerShell Scripting", "level": "Intermediate"},
            {"name": "Linux & Windows Server Security", "level": "Advanced"}
        ],
        "certifications": [
            "CISSP (Certified Information Systems Security Professional)",
            "CISM (Certified Information Security Manager)",
            "CEH (Certified Ethical Hacker)",
            "CCSP (Certified Cloud Security Professional)",
            "OSCP (Offensive Security Certified Professional)",
            "PCI-DSS Internal Auditor"
        ],
        "roadmap_phases": [
            {
                "phase": "Security Fundamentals (Months 1-3)",
                "duration": "3 months",
                "focus": "Network security basics. Cryptography. Authentication mechanisms. Linux security."
            },
            {
                "phase": "IAM & PAM Specialization (Months 4-6)",
                "duration": "3 months",
                "focus": "Active Directory hardening. MFA implementation. PAM tools (CyberArk). RBAC/ABAC."
            },
            {
                "phase": "Cloud & Application Security (Months 7-10)",
                "duration": "4 months",
                "focus": "AWS/Azure security services. OWASP Top 10. Secure coding. API security. CSPM tools."
            },
            {
                "phase": "Compliance & SOC Operations (Months 11-14)",
                "duration": "4 months",
                "focus": "PCI-DSS requirements. ISO 27001 framework. SIEM monitoring. Incident response. VAPT."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT/ECE",
            "gate_required": False,
            "certifications_mandatory": "CISSP or CEH preferred"
        },
        "salary_range": {
            "fresher": "₹5-9 LPA",
            "mid_level": "₹12-22 LPA",
            "senior": "₹25-45 LPA"
        },
        "top_companies": ["HDFC Bank", "ICICI Bank", "Axis Bank", "SBI", "Paytm", "PhonePe", "Razorpay", "CRED"],
        "job_market_outlook": "Critical demand (financial security priority)",
        "keywords_for_ats": ["IAM", "PAM", "PCI-DSS", "CISSP", "Cloud Security", "SIEM", "Banking Security", "MFA", "PKI"]
    },
    
    "cybersecurity_analyst": {
        "domain_id": "cybersecurity_analyst",
        "title": "Cybersecurity Analyst",
        "category": "Cybersecurity & Banking",
        "description": "Monitor security systems, detect threats, respond to incidents, and protect organizational assets from cyberattacks.",
        "required_education": ["B.Tech CS/IT/ECE", "Cybersecurity certifications"],
        "key_skills": [
            {"name": "SIEM Tools (Splunk, QRadar)", "level": "Advanced"},
            {"name": "Threat Intelligence", "level": "Intermediate"},
            {"name": "Incident Response", "level": "Advanced"},
            {"name": "Network Security", "level": "Intermediate"},
            {"name": "Malware Analysis", "level": "Basic"},
            {"name": "Security Frameworks (NIST, MITRE)", "level": "Intermediate"},
            {"name": "Log Analysis", "level": "Advanced"}
        ],
        "certifications": [
            "CompTIA Security+",
            "CEH (Certified Ethical Hacker)",
            "GIAC Security Essentials (GSEC)",
            "CySA+ (Cybersecurity Analyst)"
        ],
        "roadmap_phases": [
            {
                "phase": "Security Basics (Months 1-2)",
                "duration": "2 months",
                "focus": "Network protocols. OS security. Attack types. Get Security+ cert."
            },
            {
                "phase": "SOC Analyst Training (Months 3-5)",
                "duration": "3 months",
                "focus": "SIEM tools (Splunk). Log analysis. Incident detection."
            },
            {
                "phase": "Threat Hunting (Months 6-8)",
                "duration": "3 months",
                "focus": "Analyze IOCs. Use MITRE ATT&CK. Investigate incidents."
            },
            {
                "phase": "Advanced Analysis (Months 9-12)",
                "duration": "4 months",
                "focus": "Malware analysis basics. Forensics. Get CEH certification."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech CS/IT",
            "gate_required": False,
            "certifications_mandatory": "Security+ recommended"
        },
        "salary_range": {
            "fresher": "₹4-7 LPA",
            "mid_level": "₹9-18 LPA",
            "senior": "₹20-35 LPA"
        },
        "top_companies": ["TCS", "Wipro", "Infosys", "Accenture", "IBM", "Deloitte", "PwC", "Banks"],
        "job_market_outlook": "Very high demand (SOC teams growing)",
        "keywords_for_ats": ["SIEM", "Splunk", "Incident Response", "Threat Analysis", "Security+", "CEH", "Log Analysis"]
    },
    
    # ============================================================================
    # AEROSPACE & DEFENSE DOMAINS
    # ============================================================================
    
    "drdo_scientist_ece": {
        "domain_id": "drdo_scientist_ece",
        "title": "DRDO Scientist - Electronics & Communication",
        "category": "Aerospace & Defense",
        "description": "Work on radar systems, communication systems, and electronic warfare for India's defense research organization.",
        "required_education": ["First Class B.Tech/BE in ECE or Electronics or Telecommunication"],
        "key_skills": [
            {"name": "Digital Signal Processing", "level": "Advanced"},
            {"name": "Radar Systems", "level": "Advanced"},
            {"name": "Communication Systems", "level": "Advanced"},
            {"name": "Microwave Engineering", "level": "Intermediate"},
            {"name": "VLSI Design", "level": "Intermediate"},
            {"name": "Embedded Systems", "level": "Intermediate"},
            {"name": "RF Engineering", "level": "Advanced"}
        ],
        "certifications": [
            "GATE EC (Mandatory)",
            "Projects in defense electronics"
        ],
        "roadmap_phases": [
            {
                "phase": "GATE EC Preparation (12 months before exam)",
                "duration": "12 months",
                "focus": "Complete GATE ECE syllabus. Practice previous papers. Target 500+ rank."
            },
            {
                "phase": "Domain Specialization (During final year)",
                "duration": "6 months",
                "focus": "Focus on radar/communication projects. Read research papers. Build technical projects."
            },
            {
                "phase": "DRDO RAC Application",
                "duration": "Ongoing",
                "focus": "Apply when notifications released. Prepare for interview. Study defense applications."
            }
        ],
        "entry_requirements": {
            "degree": "First Class B.Tech ECE",
            "gate_required": True,
            "gate_subject": "EC (Electronics)",
            "age_limit": "28-35 years (with relaxations)",
            "nationality": "Indian citizen",
            "certifications_mandatory": "Valid GATE score"
        },
        "salary_range": {
            "scientist_b": "₹5.6-9 LPA (Pay Level 10)",
            "scientist_c": "₹7-11 LPA",
            "senior": "₹12-20+ LPA"
        },
        "top_organizations": ["DRDO (All labs)", "Defense PSUs post-experience"],
        "job_market_outlook": "Stable government job (high prestige)",
        "keywords_for_ats": ["GATE EC", "Radar Systems", "DSP", "Communication", "Electronics", "DRDO", "Defense"]
    },
    
    "drdo_scientist_mechanical": {
        "domain_id": "drdo_scientist_mechanical",
        "title": "DRDO Scientist - Mechanical Engineering",
        "category": "Aerospace & Defense",
        "description": "Essential for missile design, combat vehicle development, aeronautical systems, and material manufacturing.",
        "required_education": ["First Class B.Tech/BE in Mechanical Engineering"],
        "key_skills": [
            {"name": "CAD/CAM (SolidWorks, CATIA)", "level": "Advanced"},
            {"name": "Finite Element Analysis", "level": "Advanced"},
            {"name": "Thermodynamics", "level": "Advanced"},
            {"name": "Fluid Mechanics", "level": "Advanced"},
            {"name": "Material Science", "level": "Intermediate"},
            {"name": "Manufacturing Processes", "level": "Advanced"},
            {"name": "Aerospace Structures", "level": "Intermediate"}
        ],
        "certifications": [
            "GATE ME (Mandatory)",
            "CATIA/SolidWorks certification"
        ],
        "roadmap_phases": [
            {
                "phase": "GATE ME Preparation (12 months)",
                "duration": "12 months",
                "focus": "Complete GATE ME syllabus. Focus on TOM, Thermodynamics, FM."
            },
            {
                "phase": "CAD/FEA Skills (6 months)",
                "duration": "6 months",
                "focus": "Master SolidWorks/CATIA. Learn ANSYS for FEA. Design projects."
            },
            {
                "phase": "Defense Projects (Final year)",
                "duration": "6 months",
                "focus": "Missile/aircraft component design. Thermal analysis. Manufacturing simulations."
            }
        ],
        "entry_requirements": {
            "degree": "First Class B.Tech Mechanical",
            "gate_required": True,
            "gate_subject": "ME (Mechanical)",
            "age_limit": "28-35 years",
            "nationality": "Indian citizen",
            "certifications_mandatory": "Valid GATE score"
        },
        "salary_range": {
            "scientist_b": "₹5.6-9 LPA",
            "scientist_c": "₹7-11 LPA",
            "senior": "₹12-20+ LPA"
        },
        "top_organizations": ["DRDO", "HAL", "BEL", "ISRO (post-experience)"],
        "job_market_outlook": "High demand for missile & aircraft programs",
        "keywords_for_ats": ["GATE ME", "CAD", "CATIA", "FEA", "ANSYS", "Missile Design", "DRDO", "Mechanical"]
    },
    
    "drdo_scientist_cse": {
        "domain_id": "drdo_scientist_cse",
        "title": "DRDO Scientist - Computer Science",
        "category": "Aerospace & Defense",
        "description": "Required for AI-based battlefield systems, cyber security, and software development for defense applications.",
        "required_education": ["First Class B.Tech/BE in CS/IT"],
        "key_skills": [
            {"name": "Data Structures & Algorithms", "level": "Advanced"},
            {"name": "Artificial Intelligence", "level": "Advanced"},
            {"name": "Cybersecurity", "level": "Advanced"},
            {"name": "Computer Networks", "level": "Advanced"},
            {"name": "Operating Systems", "level": "Advanced"},
            {"name": "Embedded Systems", "level": "Intermediate"},
            {"name": "Image Processing", "level": "Intermediate"}
        ],
        "certifications": [
            "GATE CS (Mandatory)",
            "Cybersecurity certifications (bonus)"
        ],
        "roadmap_phases": [
            {
                "phase": "GATE CS Preparation (12 months)",
                "duration": "12 months",
                "focus": "DSA, OS, Networks, DBMS, TOC. Target top 500 rank."
            },
            {
                "phase": "AI/Cybersecurity Focus (6 months)",
                "duration": "6 months",
                "focus": "Machine Learning projects. Network security. Cryptography."
            },
            {
                "phase": "Defense Software Projects (Final year)",
                "duration": "6 months",
                "focus": "Embedded AI systems. Secure communication. Image analysis for surveillance."
            }
        ],
        "entry_requirements": {
            "degree": "First Class B.Tech CS/IT",
            "gate_required": True,
            "gate_subject": "CS (Computer Science)",
            "age_limit": "28-35 years",
            "nationality": "Indian citizen",
            "certifications_mandatory": "Valid GATE score"
        },
        "salary_range": {
            "scientist_b": "₹5.6-9 LPA",
            "scientist_c": "₹7-11 LPA",
            "senior": "₹12-20+ LPA"
        },
        "top_organizations": ["DRDO CAIR", "DRDO DLRL", "DRDO LASTEC", "Defense Cyber Agency"],
        "job_market_outlook": "Growing (AI in defense, cyber warfare)",
        "keywords_for_ats": ["GATE CS", "AI", "Cybersecurity", "DSA", "Computer Networks", "DRDO", "Defense"]
    },
    
    "aerospace_engineer": {
        "domain_id": "aerospace_engineer",
        "title": "Aerospace Engineer",
        "category": "Aerospace & Defense",
        "description": "Design, develop, and test aircraft, spacecraft, satellites, and missiles.",
        "required_education": ["B.Tech/BE in Aerospace/Aeronautical Engineering"],
        "key_skills": [
            {"name": "Aerodynamics", "level": "Advanced"},
            {"name": "Aircraft Structures", "level": "Advanced"},
            {"name": "Propulsion Systems", "level": "Advanced"},
            {"name": "Flight Mechanics", "level": "Advanced"},
            {"name": "CAD (CATIA, SolidWorks)", "level": "Advanced"},
            {"name": "CFD (Computational Fluid Dynamics)", "level": "Intermediate"},
            {"name": "MATLAB/Simulink", "level": "Intermediate"}
        ],
        "certifications": [
            "GATE AE (for PSU/ISRO)",
            "CATIA V5 Certification",
            "Six Sigma (DMAIC)"
        ],
        "roadmap_phases": [
            {
                "phase": "Core Aerospace Subjects (3rd-4th year)",
                "duration": "18 months",
                "focus": "Master aerodynamics, structures, propulsion. Excel in projects."
            },
            {
                "phase": "CAD/CFD Skills (Final year)",
                "duration": "6 months",
                "focus": "Learn CATIA V5. CFD simulations (ANSYS Fluent). Design aircraft components."
            },
            {
                "phase": "GATE AE Prep (if targeting PSU/ISRO)",
                "duration": "12 months",
                "focus": "GATE Aerospace Engineering syllabus preparation."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech Aerospace/Aeronautical",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹4-8 LPA",
            "mid_level": "₹10-20 LPA",
            "senior": "₹22-40 LPA"
        },
        "top_companies": ["HAL", "ISRO", "DRDO", "Boeing India", "Airbus India", "Tata Advanced Systems"],
        "job_market_outlook": "Moderate demand (specialized field)",
        "keywords_for_ats": ["Aerospace", "Aerodynamics", "CATIA", "CFD", "Aircraft Design", "GATE AE", "Propulsion"]
    },
    
    # ============================================================================
    # CORE ENGINEERING DOMAINS
    # ============================================================================
    
    "mechanical_engineer": {
        "domain_id": "mechanical_engineer",
        "title": "Mechanical Engineer",
        "category": "Core Engineering",
        "description": "Design, analyze, and manufacture mechanical systems. Work in automotive, manufacturing, energy, and HVAC sectors.",
        "required_education": ["B.Tech/BE in Mechanical Engineering"],
        "key_skills": [
            {"name": "CAD (SolidWorks, AutoCAD)", "level": "Advanced"},
            {"name": "Finite Element Analysis (ANSYS)", "level": "Intermediate"},
            {"name": "Manufacturing Processes", "level": "Advanced"},
            {"name": "Thermodynamics", "level": "Advanced"},
            {"name": "Strength of Materials", "level": "Advanced"},
            {"name": "GD&T (Geometric Dimensioning)", "level": "Intermediate"}
        ],
        "certifications": [
            "GATE ME (for PSUs)",
            "SolidWorks CSWA/CSWP",
            "Six Sigma Green Belt",
            "AutoCAD Professional"
        ],
        "roadmap_phases": [
            {
                "phase": "CAD Mastery (Months 1-3)",
                "duration": "3 months",
                "focus": "SolidWorks complete course. Design machine components. Get CSWA certified."
            },
            {
                "phase": "FEA & Simulation (Months 4-6)",
                "duration": "3 months",
                "focus": "ANSYS Workbench. Stress analysis. Thermal simulations."
            },
            {
                "phase": "Industry Projects (Months 7-12)",
                "duration": "6 months",
                "focus": "Internship in manufacturing. Design projects. Build portfolio."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech Mechanical",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹3-6 LPA",
            "mid_level": "₹7-14 LPA",
            "senior": "₹16-30 LPA"
        },
        "top_companies": ["Tata Motors", "Mahindra", "L&T", "Siemens", "GE", "Bosch", "Ashok Leyland"],
        "job_market_outlook": "Stable demand (core sector)",
        "keywords_for_ats": ["Mechanical", "SolidWorks", "CAD", "ANSYS", "FEA", "Manufacturing", "GATE ME"]
    },
    
    "civil_engineer": {
        "domain_id": "civil_engineer",
        "title": "Civil Engineer",
        "category": "Core Engineering",
        "description": "Design and supervise construction of infrastructure - buildings, roads, bridges, dams, water supply systems.",
        "required_education": ["B.Tech/BE in Civil Engineering"],
        "key_skills": [
            {"name": "AutoCAD", "level": "Advanced"},
            {"name": "Structural Analysis (STAAD.Pro)", "level": "Advanced"},
            {"name": "Concrete Design", "level": "Advanced"},
            {"name": "Surveying", "level": "Intermediate"},
            {"name": "Project Management", "level": "Intermediate"},
            {"name": "Estimation & Costing", "level": "Advanced"}
        ],
        "certifications": [
            "GATE CE (for PSUs)",
            "AutoCAD Certified Professional",
            "STAAD.Pro Certification",
            "PMP (for senior roles)"
        ],
        "roadmap_phases": [
            {
                "phase": "Software Skills (Months 1-4)",
                "duration": "4 months",
                "focus": "Master AutoCAD. Learn STAAD.Pro for structural analysis."
            },
            {
                "phase": "Site Experience (Months 5-12)",
                "duration": "8 months",
                "focus": "Internship at construction site. Learn estimation. Site supervision."
            },
            {
                "phase": "GATE Prep (if PSU target)",
                "duration": "12 months",
                "focus": "GATE Civil Engineering preparation."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech Civil",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹2.5-5 LPA",
            "mid_level": "₹6-12 LPA",
            "senior": "₹14-25 LPA"
        },
        "top_companies": ["L&T", "Tata Projects", "Shapoorji Pallonji", "NCC", "NBCC", "PWD", "PSUs"],
        "job_market_outlook": "Steady demand (infrastructure boom)",
        "keywords_for_ats": ["Civil Engineering", "AutoCAD", "STAAD.Pro", "Structural Design", "Construction", "GATE CE"]
    },
    
    "electrical_engineer_eee": {
        "domain_id": "electrical_engineer_eee",
        "title": "Electrical & Electronics Engineer (EEE)",
        "category": "Core Engineering",
        "description": "Work on power systems, control systems, electrical machines, and electronics applications.",
        "required_education": ["B.Tech/BE in Electrical & Electronics Engineering"],
        "key_skills": [
            {"name": "Power Systems", "level": "Advanced"},
            {"name": "Control Systems", "level": "Advanced"},
            {"name": "Electrical Machines", "level": "Advanced"},
            {"name": "MATLAB/Simulink", "level": "Intermediate"},
            {"name": "PLC Programming", "level": "Intermediate"},
            {"name": "AutoCAD Electrical", "level": "Basic"}
        ],
        "certifications": [
            "GATE EE (for PSUs)",
            "PLC & SCADA",
            "Power System Automation",
            "Six Sigma"
        ],
        "roadmap_phases": [
            {
                "phase": "Core EEE Concepts (During college)",
                "duration": "Ongoing",
                "focus": "Power systems, machines, control theory. Excel in labs."
            },
            {
                "phase": "Industry Tools (Months 1-4)",
                "duration": "4 months",
                "focus": "MATLAB/Simulink. PLC programming. SCADA basics."
            },
            {
                "phase": "GATE EE (if PSU target)",
                "duration": "12 months",
                "focus": "Prepare GATE Electrical Engineering."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech EEE",
            "gate_required": False,
            "certifications_mandatory": False
        },
        "salary_range": {
            "fresher": "₹3-6 LPA",
            "mid_level": "₹7-15 LPA",
            "senior": "₹17-32 LPA"
        },
        "top_companies": ["Siemens", "ABB", "Schneider Electric", "L&T", "BHEL", "Power Grid", "PSUs"],
        "job_market_outlook": "Stable (power sector growth)",
        "keywords_for_ats": ["Electrical", "Power Systems", "PLC", "SCADA", "Control Systems", "GATE EE", "MATLAB"]
    },
    
    "automation_engineer": {
        "domain_id": "automation_engineer",
        "title": "Automation Engineer",
        "category": "Core Engineering",
        "description": "Design and implement automated systems for manufacturing, industrial processes, and robotics.",
        "required_education": ["B.Tech in EEE/ECE/Mechanical/Instrumentation"],
        "key_skills": [
            {"name": "PLC Programming (Siemens, Allen Bradley)", "level": "Advanced"},
            {"name": "SCADA/HMI", "level": "Advanced"},
            {"name": "Industrial Robotics", "level": "Intermediate"},
            {"name": "Control Systems", "level": "Advanced"},
            {"name": "Python (for automation)", "level": "Intermediate"},
            {"name": "DCS (Distributed Control Systems)", "level": "Basic"}
        ],
        "certifications": [
            "Siemens PLC Certification",
            "Rockwell Automation",
            "Industrial Robotics",
            "Six Sigma Green Belt"
        ],
        "roadmap_phases": [
            {
                "phase": "PLC & SCADA (Months 1-4)",
                "duration": "4 months",
                "focus": "Siemens TIA Portal or Allen Bradley. Ladder logic. SCADA design."
            },
            {
                "phase": "Robotics & Advanced Control (Months 5-8)",
                "duration": "4 months",
                "focus": "Industrial robots (ABB, KUKA). Motion control. System integration."
            },
            {
                "phase": "Industry Projects (Months 9-12)",
                "duration": "4 months",
                "focus": "Internship in automation company. Hands-on PLC projects."
            }
        ],
        "entry_requirements": {
            "degree": "B.Tech EEE/ECE/Mechanical",
            "gate_required": False,
            "certifications_mandatory": "PLC certification preferred"
        },
        "salary_range": {
            "fresher": "₹4-7 LPA",
            "mid_level": "₹8-16 LPA",
            "senior": "₹18-35 LPA"
        },
        "top_companies": ["Siemens", "ABB", "Rockwell Automation", "Honeywell", "Bosch", "L&T", "KUKA"],
        "job_market_outlook": "Growing (Industry 4.0 adoption)",
        "keywords_for_ats": ["Automation", "PLC", "SCADA", "Robotics", "Siemens", "Control Systems", "Industrial"]
    }
}


# Category groupings for easy filtering
CAREER_CATEGORIES = {
    "Software & AI": [
        "full_stack_developer",
        "ai_engineer",
        "ml_engineer",
        "genai_llm_engineer",
        "mlops_engineer",
        "data_scientist",
        "data_analyst",
        "data_engineer",
        "computer_vision_engineer",
        "nlp_engineer"
    ],
    "Cybersecurity & Banking": [
        "banking_security_engineer",
        "cybersecurity_analyst"
    ],
    "Aerospace & Defense": [
        "drdo_scientist_ece",
        "drdo_scientist_mechanical",
        "drdo_scientist_cse",
        "aerospace_engineer"
    ],
    "Core Engineering": [
        "mechanical_engineer",
        "civil_engineer",
        "electrical_engineer_eee",
        "automation_engineer"
    ]
}


def get_domain_by_id(domain_id: str):
    """Get domain details by ID"""
    return CAREER_DOMAINS.get(domain_id)


def get_domains_by_category(category: str):
    """Get all domains in a category"""
    domain_ids = CAREER_CATEGORIES.get(category, [])
    return [CAREER_DOMAINS[did] for did in domain_ids if did in CAREER_DOMAINS]


def get_all_domains():
    """Get all career domains"""
    return list(CAREER_DOMAINS.values())


def search_domains(keyword: str):
    """Search domains by keyword"""
    keyword_lower = keyword.lower()
    results = []
    for domain in CAREER_DOMAINS.values():
        if (keyword_lower in domain['title'].lower() or 
            keyword_lower in domain['description'].lower() or
            any(keyword_lower in skill['name'].lower() for skill in domain['key_skills'])):
            results.append(domain)
    return results
