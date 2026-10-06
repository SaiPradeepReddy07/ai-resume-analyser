# Database Design & Schema Documentation

The AI Resume Analyzer uses **SQLAlchemy 2.0** ORM to manage relational schema and transactions. The application supports **PostgreSQL** in production environments and **SQLite** for zero-configuration local development.

---

## 1. Entity-Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ RESUMES : uploads
    USERS ||--o{ JOB_DESCRIPTIONS : creates
    USERS ||--o{ ANALYSES : performs
    RESUMES ||--o{ ANALYSES : evaluated_in
    JOB_DESCRIPTIONS ||--o{ ANALYSES : matched_against

    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        datetime created_at
        datetime updated_at
    }

    RESUMES {
        int id PK
        int user_id FK
        string filename
        text extracted_text
        datetime created_at
    }

    JOB_DESCRIPTIONS {
        int id PK
        int user_id FK
        string title
        string company
        text description
        datetime created_at
    }

    ANALYSES {
        int id PK
        int user_id FK
        int resume_id FK
        int job_description_id FK
        float match_score
        float skill_score
        float keyword_score
        float semantic_score
        json matching_skills
        json missing_skills
        json recommendations
        json category_breakdown
        datetime created_at
    }
```

---

## 2. Table Specifications

### 2.1 `users` Table
Stores user registration credentials and profile information. Passwords are hash-digested using bcrypt and never stored in plain text.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY, AUTOINCREMENT` | Unique identifier for each user |
| `name` | `VARCHAR(100)` | `NOT NULL` | Full display name of the user |
| `email` | `VARCHAR(255)` | `NOT NULL, UNIQUE, INDEXED` | User email address used for login |
| `password_hash` | `VARCHAR(255)` | `NOT NULL` | Bcrypt salted and hashed password |
| `created_at` | `DATETIME` | `NOT NULL, DEFAULT NOW()` | Account creation timestamp |
| `updated_at` | `DATETIME` | `NULLABLE` | Last profile update timestamp |

**Indexes & Constraints**:
- `ix_users_email`: Unique B-Tree index on `email` to guarantee unique logins and $O(1)$ authentication lookup.

---

### 2.2 `resumes` Table
Stores parsed resume text and metadata uploaded by the user.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY, AUTOINCREMENT` | Unique identifier for the resume entry |
| `user_id` | `INTEGER` | `NOT NULL, FOREIGN KEY(users.id)` | ID of the user who uploaded the resume |
| `filename` | `VARCHAR(255)` | `NOT NULL` | Original uploaded PDF filename |
| `extracted_text` | `TEXT` | `NOT NULL` | Cleaned text extracted from the PDF via PyMuPDF |
| `created_at` | `DATETIME` | `NOT NULL, DEFAULT NOW()` | Upload timestamp |

**Indexes & Constraints**:
- `ix_resumes_user_id`: Index on `user_id` for fast query of all resumes belonging to a user.
- Cascade rule: When a user is deleted, their associated resumes are automatically removed.

---

### 2.3 `job_descriptions` Table
Stores target job postings and company specifications against which resumes are compared.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY, AUTOINCREMENT` | Unique identifier for the job posting |
| `user_id` | `INTEGER` | `NOT NULL, FOREIGN KEY(users.id)` | ID of the user who entered the job |
| `title` | `VARCHAR(200)` | `NOT NULL` | Position title (e.g., "Full-Stack Engineer") |
| `company` | `VARCHAR(200)` | `DEFAULT ""` | Company or organization name |
| `description` | `TEXT` | `NOT NULL` | Raw text of requirements and responsibilities |
| `created_at` | `DATETIME` | `NOT NULL, DEFAULT NOW()` | Creation timestamp |

**Indexes & Constraints**:
- `ix_job_descriptions_user_id`: Index on `user_id` for fast user retrieval.

---

### 2.4 `analyses` Table
Stores the results of the NLP comparison between a resume and a job description.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | `PRIMARY KEY, AUTOINCREMENT` | Unique identifier for the analysis record |
| `user_id` | `INTEGER` | `NOT NULL, FOREIGN KEY(users.id)` | User who ran the analysis |
| `resume_id` | `INTEGER` | `NOT NULL, FOREIGN KEY(resumes.id)` | Analyzed resume record |
| `job_description_id` | `INTEGER` | `NOT NULL, FOREIGN KEY(job_descriptions.id)` | Matched job description record |
| `match_score` | `FLOAT` | `NOT NULL` | Normalized composite score (0–100%) |
| `skill_score` | `FLOAT` | `NOT NULL` | Skill recall component score (0–100%) |
| `keyword_score` | `FLOAT` | `NOT NULL` | TF-IDF keyword cosine similarity (0–100%) |
| `semantic_score` | `FLOAT` | `NOT NULL` | Document text cosine similarity (0–100%) |
| `matching_skills` | `JSON` | `NOT NULL` | Array of detected matching skills |
| `missing_skills` | `JSON` | `NOT NULL` | Array of missing skill objects with explanations |
| `recommendations` | `JSON` | `NOT NULL` | Array of tailored actionable recommendations |
| `category_breakdown` | `JSON` | `NOT NULL` | Skill counts categorized by domain |
| `created_at` | `DATETIME` | `NOT NULL, DEFAULT NOW()` | Analysis timestamp |

**Indexes & Constraints**:
- `ix_analyses_user_id`: Index on `user_id` for sorting and pagination in dashboard and history views.
- `ix_analyses_created_at`: Index on `created_at` for chronological queries.

---

## 3. SQLite vs PostgreSQL Configuration

The application automatically adapts to the connection string defined in the `DATABASE_URL` environment variable:

### Local Development (SQLite)
```bash
DATABASE_URL="sqlite:///./resume_analyzer.db"
```
- No database server installation required.
- SQLite is handled with `connect_args={"check_same_thread": False}` in FastAPI's multi-threaded worker pool.
- JSON fields are transparently serialized as strings or native SQLite JSON.

### Production Environment (PostgreSQL)
```bash
DATABASE_URL="postgresql://user:password@host:5432/resume_analyzer_db"
```
- Uses connection pooling (`pool_size=10`, `max_overflow=20`, `pool_pre_ping=True`) to handle concurrent traffic.
- Native `JSONB` or `JSON` data types for structured indexing and high-throughput query performance.
