from config import get_supabase_client
from datetime import datetime

supabase = get_supabase_client()

# Créer un événement
def create_event(event, date, place, organizer):
    try:
        response = supabase.table("event").insert({
            "event": event,
            "date": date,
            "place": place,
            "organizer": organizer
        }).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error create in : {e}")
        return None

# Lire tous les événements
def get_events():
    try:
        response = supabase.table("event").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire un évènement
def get_event(event_id):
    try:
        response = supabase.table("event").select("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Mettre à jour un événement
def update_event(event_id, update_data):
    try:
        response = supabase.table("event").update(update_data).eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error update in : {e}")
        return None

# Supprimer un événement
def delete_event(event_id):
    try:
        response = supabase.table("event").delete().eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error delete in : {e}")
        return None

# Lire tous les évènement à venir
def get_upcoming_events():
    try:
        today = datetime.utcnow().isoformat()  
        response = supabase.table("event") \
            .select("*") \
            .gt("date", today) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire tous les events à venir pour un utilisateur
def get_user_upcoming_events(user_id):
    try:
        today = datetime.utcnow().isoformat() 
        response = supabase.table("event") \
            .select("*, guest!inner(user_id)") \
            .eq("guest.user_id", user_id) \
            .gt("date", today) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire tous les events à venir pour un utilisateur
def get_user_events(user_id):
    try:
        response = supabase.table("event") \
            .select("*, guest!inner(user_id)") \
            .eq("guest.user_id", user_id) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

