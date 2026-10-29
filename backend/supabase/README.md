# Supabase setup

This directory contains the SQL schema for the application database.

1. Open your Supabase project.
2. Go to SQL Editor.
3. Paste the contents of `schema.sql` and run it.
4. Then set these environment variables in your local backend `.env` file.

```env
SUPABASE_URL="https://<project-ref>.supabase.co"
SUPABASE_ANON_KEY="<anon-key>"
SUPABASE_SERVICE_ROLE_KEY="<service-role-key>"
SUPABASE_DATABASE_URL="postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres"
```

For the frontend, add the same URL and anon key to a `frontend/.env` file using `frontend/.env.example`.
