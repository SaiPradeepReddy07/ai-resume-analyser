# REST API Documentation

The AI Resume Analyzer provides an OpenAPI-compliant RESTful API built on **FastAPI**. Interactive Swagger UI documentation is available at `/docs` and ReDoc at `/redoc`.

---

## Base URL & Headers

- Local Development Base URL: `http://localhost:8000/api`
- Content Type: `application/json` (or `multipart/form-data` for file uploads)
- Authentication: Standard HTTP Bearer Token header for protected endpoints:
  ```http
  Authorization: Bearer <your_jwt_access_token>
  ```

---

## 1. Authentication Endpoints (`/api/auth`)

### 1.1 Register New Account
- **Endpoint**: `POST /api/auth/register`
- **Access**: Public
- **Request Body**:
  ```json
  {
    "name": "Jane Developer",
    "email": "jane@example.com",
    "password": "StrongPassword123!",
    "confirm_password": "StrongPassword123!"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": 1,
    "name": "Jane Developer",
    "email": "jane@example.com",
    "created_at": "2026-10-06T00:00:00Z"
  }
  ```
- **Errors**:
  - `400 Bad Request`: Passwords do not match or email already registered.
  - `422 Unprocessable Entity`: Invalid email format or password shorter than 8 characters.

---

### 1.2 User Login
- **Endpoint**: `POST /api/auth/login`
- **Access**: Public
- **Request Body**:
  ```json
  {
    "email": "jane@example.com",
    "password": "StrongPassword123!"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "name": "Jane Developer",
      "email": "jane@example.com"
    }
  }
  ```
- **Errors**:
  - `401 Unauthorized`: Invalid email or password.

---

### 1.3 Get Current User Profile
- **Endpoint**: `GET /api/auth/me`
- **Access**: Protected (Bearer Token)
- **Response (200 OK)**:
  ```json
  {
    "id": 1,
    "name": "Jane Developer",
    "email": "jane@example.com",
    "created_at": "2026-10-06T00:00:00Z",
    "updated_at": null
  }
  ```

---

## 2. Resume Endpoints (`/api/resumes`)

### 2.1 Upload Resume PDF
- **Endpoint**: `POST /api/resumes/upload`
- **Access**: Protected
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: PDF file binary (max 5MB)
- **Response (201 Created)**:
  ```json
  {
    "id": 1,
    "filename": "Jane_Developer_Resume.pdf",
    "char_count": 3420,
    "detected_skills": ["Python", "FastAPI", "React", "PostgreSQL", "Docker", "Git"],
    "created_at": "2026-10-06T00:05:00Z"
  }
  ```
- **Errors**:
  - `400 Bad Request`: File is not a PDF, is empty, or exceeds 5MB size limit.

---

### 2.2 List User Resumes
- **Endpoint**: `GET /api/resumes`
- **Access**: Protected
- **Response (200 OK)**:
  ```json
  [
    {
      "id": 1,
      "filename": "Jane_Developer_Resume.pdf",
      "char_count": 3420,
      "created_at": "2026-10-06T00:05:00Z"
    }
  ]
  ```

---

### 2.3 Delete Resume
- **Endpoint**: `DELETE /api/resumes/{id}`
- **Access**: Protected
- **Response (204 No Content)**

---

## 3. Job Description Endpoints (`/api/jobs`)

### 3.1 Create Job Description
- **Endpoint**: `POST /api/jobs`
- **Access**: Protected
- **Request Body**:
  ```json
  {
    "title": "Junior Python Developer",
    "company": "Tech Innovations Inc.",
    "description": "We are seeking a Junior Python Developer proficient with Python, FastAPI, PostgreSQL, Git, and Docker. Experience with REST APIs and React is a strong plus."
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "id": 1,
    "title": "Junior Python Developer",
    "company": "Tech Innovations Inc.",
    "created_at": "2026-10-06T00:10:00Z"
  }
  ```

---

## 4. Analysis Endpoints (`/api/analysis`)

### 4.1 Perform Direct Resume & Job Analysis
Analyzes an uploaded PDF directly against a job description in a single cohesive call.
- **Endpoint**: `POST /api/analysis/direct`
- **Access**: Protected
- **Content-Type**: `multipart/form-data`
- **Form Data**:
  - `file`: PDF file
  - `job_title`: String
  - `company`: String (optional)
  - `job_description`: String
- **Response (201 Created)**:
  ```json
  {
    "id": 1,
    "match_score": 82.5,
    "match_tier": "Strong Match",
    "skill_score": 85.0,
    "keyword_score": 80.0,
    "semantic_score": 81.2,
    "job_title": "Junior Python Developer",
    "company": "Tech Innovations Inc.",
    "matching_skills": ["Python", "FastAPI", "PostgreSQL", "Git", "REST API"],
    "missing_skills": [
      {
        "skill": "Docker",
        "category": "Cloud & DevOps",
        "explanation": "Docker appears in the job requirements but was not detected in your resume."
      }
    ],
    "recommendations": [
      {
        "type": "skill_gap",
        "title": "Bridge Technical Skill Gaps",
        "detail": "Consider building a containerized project using Docker if you have basic knowledge, or explore basic Docker container deployment tutorials."
      },
      {
        "type": "quantification",
        "title": "Quantify Engineering Impact",
        "detail": "Enhance your project bullet points with measurable outcomes (e.g., 'Optimized database queries reducing latency by 35%')."
      }
    ],
    "category_breakdown": {
      "Programming": {"resume": 3, "job": 3},
      "Backend": {"resume": 2, "job": 2},
      "Database": {"resume": 1, "job": 1},
      "Cloud & DevOps": {"resume": 0, "job": 1},
      "Tools": {"resume": 2, "job": 2}
    },
    "created_at": "2026-10-06T00:15:00Z"
  }
  ```

---

### 4.2 List Analysis History
- **Endpoint**: `GET /api/analysis`
- **Access**: Protected
- **Query Parameters**:
  - `search` (string, optional): Search by job title or company
  - `sort_by` (string, optional): `date_desc`, `date_asc`, `score_desc`, `score_asc`
  - `min_score` (float, optional): Filter by minimum score
- **Response (200 OK)**: List of analysis summaries.

---

### 4.3 Get Single Analysis Details
- **Endpoint**: `GET /api/analysis/{id}`
- **Access**: Protected
- **Response (200 OK)**: Complete analysis object with breakdown and recommendations.

---

### 4.4 Delete Analysis
- **Endpoint**: `DELETE /api/analysis/{id}`
- **Access**: Protected
- **Response (204 No Content)**

---

## 5. Dashboard Endpoints (`/api/dashboard`)

### 5.1 Get User Dashboard Statistics
- **Endpoint**: `GET /api/dashboard/stats`
- **Access**: Protected
- **Response (200 OK)**:
  ```json
  {
    "total_analyses": 6,
    "average_score": 76.4,
    "highest_score": 91.0,
    "lowest_score": 58.0,
    "most_frequently_missing_skills": [
      {"skill": "Docker", "count": 4},
      {"skill": "Kubernetes", "count": 3},
      {"skill": "AWS", "count": 3}
    ],
    "score_history": [
      {"date": "2026-10-01", "score": 65.0, "job_title": "Python Intern"},
      {"date": "2026-10-06", "score": 82.5, "job_title": "Junior Python Dev"}
    ],
    "recent_analyses": [...]
  }
  ```

---

## 6. Profile Endpoints (`/api/profile`)

### 6.1 Update Profile Name
- **Endpoint**: `PUT /api/profile`
- **Access**: Protected
- **Request Body**:
  ```json
  {
    "name": "Jane Updated Name"
  }
  ```

### 6.2 Change Password
- **Endpoint**: `PUT /api/profile/password`
- **Access**: Protected
- **Request Body**:
  ```json
  {
    "current_password": "OldPassword123!",
    "new_password": "NewSecurePassword456!",
    "confirm_new_password": "NewSecurePassword456!"
  }
  ```
