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

## Supabase setup

This project supports both local SQLite development and a real PostgreSQL/Supabase
production database.

1. Create a new Supabase project from the Supabase dashboard.
2. Copy your project URL and keys from:
   - Project Settings → API
   - Project Settings → Database
3. Create a local `.env` file in `backend/` using `backend/.env.example` as a template.
4. Set at least these values:

```env
SUPABASE_URL="https://<project-ref>.supabase.co"
SUPABASE_ANON_KEY="<anon-key>"
SUPABASE_SERVICE_ROLE_KEY="<service-role-key>"
SUPABASE_DATABASE_URL="postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres"
```

If you are using Supabase for the app database, set `SUPABASE_DATABASE_URL` or `DATABASE_URL`.
The app will automatically prefer `SUPABASE_DATABASE_URL` when present.

The Supabase client is exposed as `app.core.supabase.supabase` and the admin client as
`app.core.supabase.supabase_admin` for database or auth operations.

## Deploy to Render

The root `render.yaml` blueprint creates a free Docker-based web service and
managed PostgreSQL database. Docker builds the React frontend and packages it
with the FastAPI backend. The API serves the frontend and its client-side
routes from the same HTTPS origin. Render generates the JWT signing key and
injects the database connection string.

The free web service may sleep when idle. Render's free PostgreSQL database
expires after 30 days, so it is suitable for a demo, not durable production
data. Upgrade the database to a paid plan before using it for data you need to
keep.

1. Push this repository to GitHub.
2. In Render, choose **New** → **Blueprint** and connect the repository.
3. Review the services and database, then apply the blueprint.
4. When the service is live, open its `onrender.com` URL. `/health` checks the
   API, and `/docs` opens the API documentation.

The Render web service and managed database use paid plans. The database is
managed separately from the web service so user accounts and analyses persist
across app restarts and deploys.
