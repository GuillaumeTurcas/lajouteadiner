from supabase import create_client, Client

# Configuration de Supabase
SUPABASE_URL = "magnifiqueURL"  
SUPABASE_KEY = "magnifiqueKEY"

def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

