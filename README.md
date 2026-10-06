# AI Resume Analyzer

AI Resume Analyzer is a full-stack application for comparing a resume with a
job description, reviewing skill gaps, and tracking analyses.

## Run locally

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API and interactive API documentation are available at
`http://127.0.0.1:8000` and `http://127.0.0.1:8000/docs`.

### Frontend

In a second terminal:

```powershell
cd frontend
npm ci
npm run dev
```

Open `http://127.0.0.1:5173`. The Vite development server proxies API requests
to the local backend.

## Deploy to Render

The root `render.yaml` blueprint creates the Docker-based web service and a
managed PostgreSQL database. Docker builds the React frontend and packages it
with the FastAPI backend. The API serves the frontend and its client-side
routes from the same HTTPS origin. Render generates the JWT signing key and
injects the database connection string.

1. Push this repository to GitHub.
2. In Render, choose **New** → **Blueprint** and connect the repository.
3. Review the services and database, then apply the blueprint.
4. When the service is live, open its `onrender.com` URL. `/health` checks the
   API, and `/docs` opens the API documentation.

The Render web service and managed database use paid plans. The database is
managed separately from the web service so user accounts and analyses persist
across app restarts and deploys.
