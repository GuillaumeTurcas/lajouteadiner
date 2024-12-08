from config import get_supabase_client
from datetime import datetime

supabase = get_supabase_client()

# Créer un événement
def create_event(event, date, place, organizer):
    response = supabase.table("event").insert({
        "event": event,
        "date": date,
        "place": place,
        "organizer": organizer
    }).execute()
    return response.data

# Lire tous les événements
def get_events():
    response = supabase.table("event").select("*").execute()
    return response.data

def get_event(event_id):
    response = supabase.table("event").select("id", event_id).execute()
    return response.data

# Mettre à jour un événement
def update_event(event_id, update_data):
    response = supabase.table("event").update(update_data).eq("id", event_id).execute()
    return response.data

# Supprimer un événement
def delete_event(event_id):
    response = supabase.table("event").delete().eq("id", event_id).execute()
    return response.data

# Lire tous les évènement à venir
def get_upcoming_events():
    today = datetime.utcnow().isoformat()  
    response = supabase.table("event") \
        .select("*") \
        .gt("date", today) \
        .execute()
    return response.data

# Lire tous les events à venir pour un utilisateur
def get_user_upcoming_events(user_id):
    today = datetime.utcnow().isoformat() 
    response = supabase.table("event") \
        .select("*, guest!inner(user_id)") \
        .eq("guest.user_id", user_id) \
        .gt("date", today) \
        .execute()
    return response.data

# Lire tous les events à venir pour un utilisateur
def get_user_events(user_id):
    response = supabase.table("event") \
        .select("*, guest!inner(user_id)") \
        .eq("guest.user_id", user_id) \
        .execute()
    return response.data