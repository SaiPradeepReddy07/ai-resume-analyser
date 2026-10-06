"""
Skills Taxonomy & Dictionary
Structured repository of technical skills grouped across 7 major software engineering domains.
Includes canonical naming, regex patterns with boundary guards, and common aliases.
"""

from typing import Dict, List, Set

SKILLS_TAXONOMY: Dict[str, List[str]] = {
    "Programming": [
        "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#",
        "Go", "Rust", "Ruby", "PHP", "SQL", "Swift", "Kotlin", "Scala", "R"
    ],
    "Frontend": [
        "HTML", "CSS", "React", "Next.js", "Angular", "Vue", "Tailwind CSS",
        "Redux", "SASS", "Bootstrap", "Webpack", "Vite", "jQuery"
    ],
    "Backend": [
        "FastAPI", "Django", "Flask", "Node.js", "Express", "Spring Boot",
        "ASP.NET", "GraphQL", "Celery", "REST API", "gRPC", "Microservices"
    ],
    "Database": [
        "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "Oracle",
        "Cassandra", "Elasticsearch", "DynamoDB", "Firebase"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Git",
        "Linux", "Nginx", "Terraform", "Ansible", "GitHub Actions", "Jenkins"
    ],
    "AI / ML & Data": [
        "Machine Learning", "Deep Learning", "NLP", "TensorFlow", "PyTorch",
        "scikit-learn", "Pandas", "NumPy", "Keras", "Hugging Face", "LLM",
        "Computer Vision", "Data Analysis", "Matplotlib", "Seaborn"
    ],
    "Tools & Practices": [
        "Postman", "Agile", "Scrum", "Jira", "Unit Testing", "pytest",
        "Docker Compose", "Swagger", "GitLab", "Bitbucket", "OOP"
    ]
}

# Aliases and alternative spellings mapping to canonical skill names
SKILL_ALIASES: Dict[str, str] = {
    # Programming
    "py": "Python",
    "python3": "Python",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "golang": "Go",
    "c plus plus": "C++",
    "cpp": "C++",
    "c sharp": "C#",
    "csharp": "C#",
    "dotnet": "ASP.NET",
    ".net": "ASP.NET",
    "structured query language": "SQL",

    # Frontend
    "html5": "HTML",
    "css3": "CSS",
    "reactjs": "React",
    "react.js": "React",
    "nextjs": "Next.js",
    "next": "Next.js",
    "angularjs": "Angular",
    "vuejs": "Vue",
    "vue.js": "Vue",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
    "sass/scss": "SASS",
    "scss": "SASS",

    # Backend
    "fast api": "FastAPI",
    "fastapi": "FastAPI",
    "nodejs": "Node.js",
    "node": "Node.js",
    "expressjs": "Express",
    "express.js": "Express",
    "spring": "Spring Boot",
    "springboot": "Spring Boot",
    "restful": "REST API",
    "rest": "REST API",
    "rest apis": "REST API",
    "rest api": "REST API",

    # Database
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "psql": "PostgreSQL",
    "mongo": "MongoDB",
    "elastic search": "Elasticsearch",

    # Cloud & DevOps
    "amazon web services": "AWS",
    "google cloud platform": "GCP",
    "google cloud": "GCP",
    "microsoft azure": "Azure",
    "k8s": "Kubernetes",
    "continuous integration": "CI/CD",
    "continuous deployment": "CI/CD",
    "cicd": "CI/CD",
    "gh actions": "GitHub Actions",

    # AI & ML
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "natural language processing": "NLP",
    "sklearn": "scikit-learn",
    "tf": "TensorFlow",
    "large language models": "LLM",
    "large language model": "LLM",
    "llms": "LLM",

    # Tools
    "object oriented programming": "OOP",
    "unit test": "Unit Testing",
    "unit tests": "Unit Testing",
    "testing": "Unit Testing"
}


def get_all_canonical_skills() -> List[str]:
    """Returns a flat sorted list of all unique canonical skills across all categories."""
    skills = []
    for cat_skills in SKILLS_TAXONOMY.values():
        skills.extend(cat_skills)
    return sorted(list(set(skills)))


def get_skill_category(skill_name: str) -> str:
    """Finds the domain category for a given canonical skill name."""
    for category, skills in SKILLS_TAXONOMY.items():
        if skill_name in skills:
            return category
    return "Other"
