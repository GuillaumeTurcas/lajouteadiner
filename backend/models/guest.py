from config import get_supabase_client

supabase = get_supabase_client()

# Ajouter un invité
def create_guest(user, event, role):
    try:
        response = supabase.table("guest").insert({
            "user": user,
            "event": event,
            "role": role
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error create in : {e}")
        return None

# Lire tous les invités
def get_guests():
    try:
        response = supabase.table("guest").select("*").execute()
        print(response.data)
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire un invité
def get_guest(guest_id):
    try:
        response = supabase.table("guest").select("*").eq("id", guest_id).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Mettre à jour un invité
def update_guest(guest_id, update_data):
    try:
        response = supabase.table("guest").update(update_data).eq("id", guest_id).execute()
        return response.data
    except Exception as e:
        print(f"Error update in : {e}")
        return None

# Supprimer un invité
def delete_guest(guest_id):
    try:
        response = supabase.table("guest").delete().eq("id", guest_id).execute()
        return response.data
    except Exception as e:
        print(f"Error delete in : {e}")
        return None

# Avoir tous les guest d'un event
def get_guests_by_event(event_id):
    try:
        response = supabase.table('guest').select('*').eq('eventId', event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None
