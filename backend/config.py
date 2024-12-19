from supabase import create_client, Client
from security_config import SUPABASE_URL, SUPABASE_KEY

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

limit_session = 24