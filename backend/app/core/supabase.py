from supabase import Client, create_client
from app.core.config import settings

supabase: Client | None = None
if settings.SUPABASE_URL and settings.SUPABASE_ANON_KEY:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)

supabase_admin: Client | None = None
if settings.SUPABASE_URL and settings.SUPABASE_SERVICE_ROLE_KEY:
    supabase_admin = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

__all__ = ["supabase", "supabase_admin"]
