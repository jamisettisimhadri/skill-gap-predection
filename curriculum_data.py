
# Comprehensive Curriculum Data for Skill Roadmaps

TECHNOLOGY_ROADMAPS = {
    "Python": {
        "Beginner": {
            "duration_hours": 40,
            "concepts": ["Syntax & Variables", "Control Flow (If/Else, Loops)", "Functions & Modules", "Data Structures (Lists, Dicts)", "File Handling"],
            "tools": ["VS Code", "IDLE", "Git Basics"],
            "project": "Personal Budget Tracker CLI",
            "practice": ["Solve 20 HackerRank basic problems", "Create a calculator app", "Write a script to rename files in bulk"],
            "resources": {
                "free": ["Python.org Docs", "Automate the Boring Stuff"],
                "paid": ["Udemy: Complete Python Bootcamp", "Coursera: Python for Everybody"]
            },
            "checkpoint": "Create a GitHub repo with 3 working scripts."
        },
        "Intermediate": {
            "duration_hours": 60,
            "concepts": ["OOP (Classes, Inheritance)", "Error Handling", "Decorators & Generators", "Virtual Environments", "Basic APIs (Requests)"],
            "tools": ["PyCharm/VS Code", "Pipenv/Poetry", "Postman"],
            "project": "Weather App using Public API",
            "practice": ["Scrape a website using BeautifulSoup", "Create a generic class structure", "Unit testing with PyTest"],
            "resources": {
                "free": ["RealPython Tutorials", "Corey Schafer YouTube"],
                "paid": ["Udemy: Python OOP", "DataCamp Intermediate Python"]
            },
            "checkpoint": "Deploy a simple script to Heroku or PythonAnywhere."
        },
        "Advanced": {
            "duration_hours": 80,
            "concepts": ["AsyncIO & Concurrency", "Metaprogramming", "Design Patterns", "Memory Management", "C-Extensions"],
            "tools": ["Docker", "Profiler", "Type Hinting"],
            "project": "Real-time Chat Server (Async)",
            "practice": ["Optimize a slow script", "Implement Singleton & Factory patterns", "Build a custom library package"],
            "resources": {
                "free": ["Python 3 Module of the Week", "ArjanCodes"],
                "paid": ["Powerful Python (Book)", "Talk Python Training"]
            },
            "checkpoint": "Publish a package to PyPI."
        },
        "Industry-Ready": {
            "duration_hours": 100,
            "concepts": ["Microservices Architecture", "System Design", "Cloud Integration (AWS Lambda)", "CI/CD Pipelines", "Security Best Practices"],
            "tools": ["Kubernetes", "AWS/GCP/Azure", "Jenkins/GitHub Actions"],
            "project": "Scalable Microservices E-commerce Backend",
            "practice": ["Design a system like Instagram", "Implement OAuth2 authentication", "Set up an automated build pipeline"],
            "resources": {
                "free": ["System Design Primer", "AWS Documentation"],
                "paid": ["System Design Interview (Alex Xu)", "Udacity Cloud Developer Nanodegree"]
            },
            "checkpoint": "Full-stack cloud deployment with monitoring."
        }
    },
    "Web Development": {
         "Beginner": {
            "duration_hours": 50,
            "concepts": ["HTML5 Semantic Structure", "CSS3 Modeling (Box Model)", "Responsive Design (Flexbox)", "JavaScript Basics (DOM)"],
            "tools": ["Chrome DevTools", "VS Code", "CodePen"],
            "project": "Personal Portfolio Website",
            "practice": ["Clone Google Landing Page", "Build a To-Do List in JS", "Make a responsive nav bar"],
            "resources": {
                "free": ["MDN Web Docs", "FreeCodeCamp"],
                "paid": ["Udemy: Web Developer Bootcamp", "Frontend Masters"]
            },
            "checkpoint": "Host a responsive site on Vercel/Netlify."
        },
        "Intermediate": {
            "duration_hours": 80,
            "concepts": ["ES6+ Features", "Async JS (Promises, Async/Await)", "React/Vue Basics", "State Management", "API Consumption"],
            "tools": ["Webpack/Vite", "Git/GitHub", "NPM/Yarn"],
            "project": "Movie Search App (React + API)",
            "practice": ["Refactor JS code to idiomatic ES6", "Build a reusable Component", "Implement Dark Mode"],
            "resources": {
                "free": ["React Docs", "JavaScript.info"],
                "paid": ["Udemy: React - The Complete Guide", "Scrimba React Course"]
            },
            "checkpoint": "Deploy a React app with dynamic routing."
        },
        "Advanced": {
            "duration_hours": 100,
            "concepts": ["Server-Side Rendering (Next.js)", "Performance Optimization", "Accessibility (a11y)", "Testing (Jest/Cypress)", "Authentication (JWT)"],
            "tools": ["Next.js", "TypeScript", "Lighthouse"],
            "project": "E-commerce Platform with Cart & Auth",
            "practice": ["Migrate a JS app to TypeScript", "Achieve 100 on Lighthouse score", "Implement RBAC Auth"],
            "resources": {
                "free": ["Next.js Documentation", "Patterns.dev"],
                "paid": ["Epic React by Kent C Dodds", "Testing JavaScript"]
            },
            "checkpoint": "Production-grade Next.js app with SEO optimization."
        },
        "Industry-Ready": {
            "duration_hours": 120,
            "concepts": ["Scalable Architecture", "Micro-frontends", "Cloud Deployment", "Web Security (OWASP)", "CI/CD for Frontend"],
            "tools": ["Docker", "AWS Amplify", "Santry (Monitoring)"],
            "project": "SaaS Dashboard with Real-time Data",
            "practice": ["Implement a CI/CD pipeline", "Set up error tracking", "Optimize bundle size"],
            "resources": {
                "free": ["Google Web Vitals", "OWASP Top 10"],
                "paid": ["Frontend Masters Enterprise", "AWS Certified Developer"]
            },
            "checkpoint": "Full CI/CD pipeline deploying to cloud with monitoring."
        }
    },
    "Data Science": {
         "Beginner": {
            "duration_hours": 60,
            "concepts": ["Python/R Basics", "NumPy & Pandas", "Data Visualization (Matplotlib)", "Statistics Fundamentals", "EDA"],
            "tools": ["Jupyter Notebook", "Anaconda", "Excel"],
            "project": "Exploratory Data Analysis on Titanic Dataset",
            "practice": ["Clean a messy dataset", "Visualize sales trends", "Calculate basic stats (Mean/Median/Mode)"],
            "resources": {
                "free": ["Kaggle Learn", "DataCamp Free Tracks"],
                "paid": ["Coursera: Data Science Specialization", "Udemy: Python for Data Science"]
            },
            "checkpoint": "Submit a kernel to a Kaggle competition."
        },
        "Intermediate": {
            "duration_hours": 90,
            "concepts": ["Machine Learning (Scikit-Learn)", "Supervised Learning", "Model Evaluation", "Feature Engineering", "SQL for Data Science"],
            "tools": ["Scikit-Learn", "SQL Workbench", "Git"],
            "project": "House Price Prediction Model",
            "practice": ["Train a regression model", "Perform variable encodings", "Write complex SQL queries"],
            "resources": {
                "free": ["Fast.ai", "Google ML Crash Course"],
                "paid": ["Udacity Data Scientist Nanodegree", "Coursera: Machine Learning by Andrew Ng"]
            },
            "checkpoint": "Build a model with >80% accuracy on a standard dataset."
        },
        "Advanced": {
            "duration_hours": 120,
            "concepts": ["Deep Learning (TensorFlow/PyTorch)", "NLP / Computer Vision", "Unsupervised Learning", "Big Data (Spark)", "Model Pipelines"],
            "tools": ["TensorFlow/PyTorch", "Apache Spark", "Airflow"],
            "project": "Image Classification or Sentiment Analysis App",
            "practice": ["Build a CNN/RNN model", "Process large dataset with Spark", "Create a data pipeline"],
            "resources": {
                "free": ["DeepLearning.AI", "Hugging Face Course"],
                "paid": ["Coursera: Deep Learning Specialization", "Udacity Deep Learning Nanodegree"]
            },
            "checkpoint": "Deploy a DL model as an API."
        },
        "Industry-Ready": {
            "duration_hours": 150,
            "concepts": ["MLOps", "Model Monitoring", "Cloud AI Services", "Scalable Data Arch", "A/B Testing"],
            "tools": ["MLflow", "Kubeflow", "AWS SageMaker"],
            "project": "End-to-End MLOps Pipeline for Production",
            "practice": ["Deploy model to Kubernetes", "Implement model drift monitoring", "Run an A/B test"],
            "resources": {
                "free": ["Full Stack Deep Learning", "MLOps.org"],
                "paid": ["Coursera: MLOps Specialization", "AWS Machine Learning Specialty"]
            },
            "checkpoint": " production-ready ML system with automatic retraining."
        }
    },
    # Default fallback for other skills
    "Generic": {
        "Beginner": {
            "duration_hours": 40,
            "concepts": ["Core Fundamentals", "Basic Syntax/Rules", "Environment Setup", "Simple Operations"],
            "tools": ["Basic IDE/Editor", "Command Line"],
            "project": "Hello World Project",
            "practice": ["Complete 10 basic exercises", "Read official documentation"],
            "resources": {"free": ["Official Docs", "YouTube Tutorials"], "paid": ["Udemy Beginner Course"]},
            "checkpoint": "Working basic prototype."
        },
        "Intermediate": {
            "duration_hours": 60,
            "concepts": ["Advanced Features", "Best Practices", "Integration", "Debugging"],
            "tools": ["Advanced IDE Features", "Version Control"],
            "project": "Functional Application",
            "practice": ["Refactor code", "Connect to Database"],
            "resources": {"free": ["Community Forums", "GitHub"], "paid": ["Intermediate Specialized Course"]},
            "checkpoint": "Functional app with persistence."
        },
        "Advanced": {
            "duration_hours": 80,
            "concepts": ["Optimization", "Architecture", "Security", "Scalability"],
            "tools": ["Profiling Tools", "Containerization"],
            "project": "Production-Ready System",
            "practice": ["Performance tuning", "Security audit"],
            "resources": {"free": ["whitepapers", "Conference Talks"], "paid": ["Advanced Certification"]},
            "checkpoint": "Scalable, secure deployment."
        },
        "Industry-Ready": {
            "duration_hours": 100,
            "concepts": ["Enterprise Patterns", "System Design", "Cloud Native", "Leadership"],
            "tools": ["Orchestration", "Cloud Platforms"],
            "project": "Enterprise Solution",
            "practice": ["Architecture Review", "Disaster Recovery"],
            "resources": {"free": ["Case Studies", "Engineering Blogs"], "paid": ["Professional Certification"]},
            "checkpoint": "Enterprise-grade system running in production."
        }
    }
}
