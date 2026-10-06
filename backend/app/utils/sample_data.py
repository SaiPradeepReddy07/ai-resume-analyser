"""
Sample Data for Testing & Demonstration
Provides pre-configured realistic resume texts and job descriptions,
specifically including a "Junior Python Developer" resume and job posting.
"""

SAMPLE_RESUME_TEXT = """
ALEX MORGAN
Email: alex.morgan@email.com | Phone: (555) 234-5678 | GitHub: github.com/alexmorgan | LinkedIn: linkedin.com/in/alexmorgan

PROFESSIONAL SUMMARY
Motivated Junior Software Engineer with a solid foundation in Python, REST APIs, and database engineering. Passionate about building clean, scalable backend services using FastAPI and PostgreSQL, with practical experience developing interactive React frontends and containerizing applications with Docker.

EDUCATION
B.S. in Computer Science | State University (Graduated May 2025)
Relevant Coursework: Data Structures & Algorithms, Database Systems, Web Development, Object-Oriented Programming, Operating Systems.

TECHNICAL SKILLS
- Programming: Python, JavaScript, SQL, HTML, CSS
- Backend: FastAPI, Flask, REST API
- Databases: PostgreSQL, SQLite, Redis
- Tools & DevOps: Git, GitHub, Linux, Postman, Unit Testing, pytest
- Concepts: Agile, OOP, Microservices basics

PROJECTS
TaskFlow — Collaborative Project Management API
- Architected a RESTful API using FastAPI and PostgreSQL to manage team tasks, assignments, and real-time sprint boards.
- Implemented JWT-based authentication with bcrypt password hashing, protecting sensitive endpoints.
- Integrated Redis caching for frequently accessed project queries, decreasing response time by 40%.
- Wrote automated unit tests with pytest achieving 88% test coverage.

E-Commerce Inventory Tracker
- Built a full-stack inventory management web application utilizing Python, Flask, and SQLite.
- Developed dynamic frontend interfaces using HTML, CSS, JavaScript, and Bootstrap.
- Integrated third-party payment mock APIs and designed relational schema with 6 interrelated tables.
- Version-controlled the entire codebase with Git and GitHub following Git Flow branching conventions.

EXPERIENCE
Software Development Intern | NextGen Solutions (June 2024 – August 2024)
- Collaborated in a 6-person Agile Scrum team to maintain Python backend services.
- Refactored 15+ database queries in PostgreSQL, improving query execution efficiency.
- Documented 20+ API endpoints using Swagger / OpenAPI specs, streamlining QA testing.
- Participated in bi-weekly code reviews and daily standups.
"""

SAMPLE_JOB_TITLE = "Junior Python Developer"
SAMPLE_COMPANY = "CloudScale Tech Solutions"

SAMPLE_JOB_DESCRIPTION = """
About the Role:
CloudScale Tech Solutions is looking for an enthusiastic Junior Python Developer to join our core backend engineering team. In this role, you will help design, develop, and maintain high-performance web applications and REST APIs that power our cloud analytics platform.

Key Responsibilities:
- Develop robust, maintainable RESTful APIs using Python, FastAPI, and Flask.
- Design, optimize, and maintain relational database schemas using PostgreSQL and Redis.
- Collaborate with frontend engineers working in React to integrate backend endpoints.
- Containerize services using Docker and support deployment in AWS cloud environments.
- Write clean, well-tested code using pytest and participate in code reviews.
- Utilize Git and GitHub for version control and CI/CD workflows.
- Participate in Agile/Scrum ceremonies and sprint planning.

Qualifications & Requirements:
- Bachelor's degree in Computer Science, Software Engineering, or equivalent practical experience.
- Strong proficiency in Python and familiarity with modern web frameworks (FastAPI or Django/Flask).
- Practical experience with relational databases (PostgreSQL or MySQL) and writing SQL queries.
- Familiarity with version control using Git and GitHub.
- Understanding of REST API principles and HTTP status codes.
- Basic knowledge of Docker containers and AWS cloud services is a strong plus.
- Exposure to JavaScript and React is desirable.
- Eagerness to learn, collaborate, and grow as part of a supportive engineering team.
"""

SAMPLE_EXPECTED_ANALYSIS = {
    "match_score": 83.5,
    "match_tier": "Strong Match",
    "skill_score": 88.9,
    "keyword_score": 80.5,
    "semantic_score": 78.2,
    "job_title": "Junior Python Developer",
    "company": "CloudScale Tech Solutions",
    "matching_skills": [
        "FastAPI", "Flask", "Git", "GitHub", "HTML", "JavaScript",
        "Linux", "PostgreSQL", "Postman", "pytest", "Python",
        "Redis", "REST API", "SQL", "SQLite", "Unit Testing"
    ],
    "missing_skills": [
        {
            "skill": "AWS",
            "category": "Cloud & DevOps",
            "explanation": "'AWS' (Cloud & DevOps) appears in the job requirements but was not detected in your resume."
        },
        {
            "skill": "Docker",
            "category": "Cloud & DevOps",
            "explanation": "'Docker' (Cloud & DevOps) appears in the job requirements but was not detected in your resume."
        },
        {
            "skill": "React",
            "category": "Frontend",
            "explanation": "'React' (Frontend) appears in the job requirements but was not detected in your resume."
        }
    ]
}
