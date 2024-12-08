from config import get_supabase_client

from models.user import *
from models.event import *

supabase = get_supabase_client()

# Ajouter un item
def create_item(name, quantity, description, event):
    response = supabase.table("item").insert({
        "name": name,
        "quantity": quantity,
        "description": description,
        "event": event
    }).execute()
    return response.data

# Lire tous les items
def get_items():
    response = supabase.table("item").select("*").execute()
    return response.data

# Mettre à jour un item
def update_item(item_id, update_data):
    response = supabase.table("item").update(update_data).eq("id", item_id).execute()
    return response.data

# Supprimer un item
def delete_item(item_id):
    response = supabase.table("item").delete().eq("id", item_id).execute()
    return response.data

# Lire tous les items d'un event
def get_items_event(event_id):
    response = supabase.table("item").select("*").eq("event", event_id).execute()
    data = response.data
    return data
