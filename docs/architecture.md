# System Architecture & Technical Design

This document details the architectural decisions, pipeline workflows, scoring engine mechanics, and extensibility patterns of the **AI Resume Analyzer**.

---

## 1. System Overview

The system follows a decoupled **Client-Server Architecture**:
1. **Frontend**: A React Single Page Application (SPA) powered by Vite, providing responsive UI, client-side routing, dynamic chart rendering (Recharts), and JWT authorization state.
2. **Backend**: An asynchronous RESTful API built on FastAPI, utilizing Pydantic for schema validation, SQLAlchemy 2.0 for database persistence, and an NLP matching engine.
3. **Database Layer**: Relational storage supporting SQLite (default local development) and PostgreSQL (production).

```
   ┌─────────────────────────────────────────────────────────────┐
   │                     React + Vite Frontend                   │
   │  ┌──────────────┐ ┌───────────────┐ ┌────────────────────┐  │
   │  │ Landing Page │ │ Dashboard &   │ │ Resume Analyzer &  │  │
   │  │ & Auth Views │ │ Score Charts  │ │ Results Views      │  │
   │  └──────┬───────┘ └───────┬───────┘ └─────────┬──────────┘  │
   └─────────┼─────────────────┼───────────────────┼─────────────┘
             │                 │                   │
             └─────────────┐   │   ┌───────────────┘
                           ▼   ▼   ▼
               HTTP / REST + Bearer Token (JSON & Multipart)
                           │   │   │
   ┌───────────────────────┴───┴───┴─────────────────────────────┐
   │                     FastAPI Backend Engine                  │
   │  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐   │
   │  │ Auth & Security│ │ Resume Parsing │ │ NLP & Scoring  │   │
   │  │ (Bcrypt / JWT) │ │ (PyMuPDF)      │ │ Engine         │   │
   │  └────────────────┘ └────────────────┘ └───────┬────────┘   │
   │                                                │            │
   │           ┌────────────────────────────────────┴────────┐   │
   │           │ SQLAlchemy 2.0 ORM Repository Layer         │   │
   │           └────────────────────┬────────────────────────┘   │
   └────────────────────────────────┼────────────────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ SQLite / PostgreSQL  │
                         └──────────────────────┘
```

---

## 2. Directory Structure

```
ai-resume-analyzer/
│
├── frontend/                     # React + Vite Single Page Application
│   ├── public/                   # Static assets, favicon, sample documents
│   ├── src/
│   │   ├── assets/               # Images, SVG logos, brand illustrations
│   │   ├── components/           # Reusable UI components
│   │   │   ├── Navbar.jsx        # Top global navigation bar
│   │   │   ├── Sidebar.jsx       # Dashboard sidebar with active route highlights
│   │   │   ├── StatCard.jsx      # Metrics card with icons and trends
│   │   │   ├── ScoreGauge.jsx    # SVG radial progress score gauge
│   │   │   ├── SkillBadge.jsx    # Matching/missing skill badge component
│   │   │   ├── FileUploader.jsx  # Drag-and-drop PDF upload component
│   │   │   ├── Modal.jsx         # Accessible confirmation dialog
│   │   │   ├── Toast.jsx         # Floating toast alert manager
│   │   │   └── ProtectedRoute.jsx# Auth gate redirecting to /login
│   │   ├── context/
│   │   │   └── AuthContext.jsx   # Global auth state & token persistence
│   │   ├── hooks/
│   │   │   └── useToast.js       # Toast hook for notification dispatch
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx   # Public presentation & features landing
│   │   │   ├── LoginPage.jsx     # User authentication with demo 1-click
│   │   │   ├── RegisterPage.jsx  # New user registration
│   │   │   ├── DashboardPage.jsx # Analytics dashboard & score charts
│   │   │   ├── AnalyzerPage.jsx  # Two-column resume & job matcher
│   │   │   ├── AnalysisResultsPage.jsx # Comprehensive results & breakdown
│   │   │   ├── HistoryPage.jsx   # Searchable & filterable history table
│   │   │   ├── ProfilePage.jsx   # User details & password change
│   │   │   └── NotFoundPage.jsx  # 404 page
│   │   ├── services/
│   │   │   ├── api.js            # Axios client with interceptors
│   │   │   └── analysisService.js# API calling abstractions
│   │   ├── utils/
│   │   │   ├── scoreHelpers.js   # Scoring tiers and color utilities
│   │   │   └── formatters.js     # Date and percentage formatters
│   │   ├── App.jsx               # Route definitions
│   │   ├── main.jsx              # Application bootstrap
│   │   └── index.css             # Tailwind base and design utilities
│   ├── package.json
│   └── vite.config.js
│
├── backend/                      # FastAPI Python Service
│   ├── app/
│   │   ├── api/                  # REST API Endpoints
│   │   │   ├── auth.py           # Register, login, me
│   │   │   ├── resumes.py        # Resume upload and management
│   │   │   ├── jobs.py           # Job description management
│   │   │   ├── analysis.py       # Direct and multi-stage analysis
│   │   │   ├── dashboard.py      # Aggregated metrics and chart data
│   │   │   ├── profile.py        # Profile edit and password update
│   │   │   └── deps.py           # Dependency injection (current user, DB)
│   │   ├── core/
│   │   │   ├── config.py         # App configuration & environment settings
│   │   │   ├── database.py       # SQLAlchemy engine & session maker
│   │   │   └── security.py       # Bcrypt password hashing & JWT handling
│   │   ├── models/               # SQLAlchemy ORM Models
│   │   │   ├── user.py           # Users table definition
│   │   │   ├── resume.py         # Resumes table definition
│   │   │   ├── job_description.py# Job descriptions table definition
│   │   │   └── analysis.py       # Analyses table definition
│   │   ├── schemas/              # Pydantic Schemas (DTOs)
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job_description.py
│   │   │   ├── analysis.py
│   │   │   ├── dashboard.py
│   │   │   └── token.py
│   │   ├── services/             # Core Business & NLP Services
│   │   │   ├── pdf_extractor.py  # PyMuPDF binary parsing & text extraction
│   │   │   ├── text_cleaner.py   # Normalization, regex sanitization
│   │   │   ├── skill_extractor.py# Taxonomy lookup & skill identification
│   │   │   ├── resume_analyzer.py# Multi-metric scoring coordinator
│   │   │   └── recommender.py    # Actionable resume advice generator
│   │   ├── utils/
│   │   │   ├── skills_taxonomy.py# Extended 7-category skills dictionary
│   │   │   └── sample_data.py    # Default demo resumes and job descriptions
│   │   ├── database.py           # Database convenience export
│   │   └── main.py               # FastAPI entry point & CORS configuration
│   ├── tests/                    # Backend Pytest Test Suite
│   │   ├── conftest.py           # Test DB fixtures and client setup
│   │   ├── test_auth.py          # Auth route unit & integration tests
│   │   ├── test_pdf_extractor.py # PDF parsing edge cases
│   │   ├── test_skill_extractor.py# Skill identification precision tests
│   │   ├── test_resume_analyzer.py# Scoring logic & bounds verification
│   │   └── test_api_endpoints.py # Full workflow integration tests
│   ├── requirements.txt
│   └── .env.example
│
├── docs/                         # Technical Documentation
│   ├── architecture.md           # This document
│   ├── api.md                    # REST API specifications
│   └── database.md               # Database schema & ERD
│
├── README.md                     # GitHub portfolio documentation
├── LICENSE                       # MIT License
└── .gitignore                    # Git ignore specifications
```

---

## 3. Analysis & Matching Algorithm

Rather than generating an arbitrary similarity number, the analyzer combines three distinct mathematical dimensions:

### 3.1 Mathematical Formulation

$$\text{Final Score} = 0.50 \cdot S_{\text{skill}} + 0.25 \cdot S_{\text{keyword}} + 0.25 \cdot S_{\text{semantic}}$$

#### 1. Skill Match Score ($S_{\text{skill}}$) — 50% Weight
Measures the direct recall of job requirements found in the applicant's resume:
$$S_{\text{skill}} = \left( \frac{| \text{Skills}_{\text{resume}} \cap \text{Skills}_{\text{job}} |}{\max(1, | \text{Skills}_{\text{job}} |)} \right) \times 100$$
If the job posting specifies 10 technical skills and the resume contains 8 of them, $S_{\text{skill}} = 80\%$.

#### 2. Keyword TF-IDF Cosine Similarity ($S_{\text{keyword}}$) — 25% Weight
Evaluates how strongly technical keywords, technologies, and methodologies align using Term Frequency-Inverse Document Frequency (TF-IDF) over unigrams and bigrams:
$$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \frac{\vec{u} \cdot \vec{v}}{\|\vec{u}\|_2 \|\vec{v}\|_2}$$
$$S_{\text{keyword}} = \text{Cosine Similarity}(\text{TFIDF}_{\text{resume\_keywords}}, \text{TFIDF}_{\text{job\_keywords}}) \times 100$$

#### 3. Semantic / Full Document Similarity ($S_{\text{semantic}}$) — 25% Weight
Measures the overall contextual resonance between the resume text and the job description, capturing background descriptions, domain verbs, and responsibility phrasing.

### 3.2 Score Tiers & Visual Feedback
- `90 – 100`: **Excellent Match** (High probability of passing ATS screens; resume is tightly targeted)
- `75 – 89`: **Strong Match** (Covers vast majority of core skills and responsibilities)
- `60 – 74`: **Good Match** (Competent baseline; missing some secondary or preferred skills)
- `40 – 59`: **Needs Improvement** (Significant skill gaps or disparate terminology)
- `0 – 39`: **Poor Match** (Fundamental mismatch between applicant background and role)

---

## 4. Skills Taxonomy System

Skills are matched through a structured taxonomy across **7 industry standard categories**:
1. **Programming Languages**: Python, Java, JavaScript, TypeScript, C, C++, C#, Go, Rust, Ruby, PHP, SQL
2. **Frontend Technologies**: HTML5, CSS3, React, Next.js, Angular, Vue.js, Tailwind CSS, Redux, SASS
3. **Backend Frameworks**: FastAPI, Django, Flask, Node.js, Express, Spring Boot, ASP.NET, GraphQL
4. **Databases & Caching**: PostgreSQL, MySQL, MongoDB, Redis, SQLite, Oracle, Cassandra
5. **Cloud & DevOps**: AWS, Azure, GCP, Docker, Kubernetes, CI/CD, Git, Linux, Nginx, Terraform
6. **AI / ML & Data**: Machine Learning, Deep Learning, NLP, TensorFlow, PyTorch, scikit-learn, Pandas, NumPy, Keras, Hugging Face
7. **Tools & Methodologies**: REST API, Postman, Agile, Scrum, Jira, Unit Testing, pytest

**Alias Handling**:
Words like `postgres` or `postgresql` resolve to canonical `PostgreSQL`; `reactjs` maps to `React`; `k8s` maps to `Kubernetes`. Word boundaries (`\b`) prevent false positives (e.g., "Go" does not trigger inside "Good" or "Going").

---

## 5. Extensibility: Adding an LLM / OpenAI API

The system is designed with a pluggable service interface. To incorporate an LLM:
1. Create `backend/app/services/llm_advisor.py`.
2. Inject the extracted resume text, job requirements, and missing skills into a structured prompt:
   ```python
   prompt = f"""
   Resume: {resume_text[:2000]}
   Job: {job_description[:2000]}
   Missing Skills: {missing_skills}
   Provide 3 bulleted rewrite suggestions tailored to this candidate.
   """
   ```
3. Return LLM-enhanced suggestions alongside the deterministic mathematical score.
