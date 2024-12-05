from config import get_supabase_client

supabase = get_supabase_client()

# Ajouter un invité
def create_guest(user, event, role):
    response = supabase.table("guest").insert({
        "user": user,
        "event": event,
        "role": role
    }).execute()
    return response.data

# Lire tous les invités
def get_guests():
    response = supabase.table("guest").select("*").execute()
    return response.data

# Mettre à jour un invité
def update_guest(guest_id, update_data):
    response = supabase.table("guest").update(update_data).eq("id", guest_id).execute()
    return response.data

# Supprimer un invité
def delete_guest(guest_id):
    response = supabase.table("guest").delete().eq("id", guest_id).execute()
    return response.data

