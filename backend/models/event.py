from config import get_supabase_client

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

# Mettre à jour un événement
def update_event(event_id, update_data):
    response = supabase.table("event").update(update_data).eq("id", event_id).execute()
    return response.data

# Supprimer un événement
def delete_event(event_id):
    response = supabase.table("event").delete().eq("id", event_id).execute()
    return response.data

