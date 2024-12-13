from config import get_supabase_client

from models.user import *
from models.event import *

supabase = get_supabase_client()

# Ajouter un item
def create_item(name, quantity, description, event):
    try:
        response = supabase.table("item").insert({
            "name": name,
            "quantity": quantity,
            "description": description,
            "event": event
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error create in : {e}")
        return None

# Lire tous les items

def get_items():
    try:
        response = supabase.table("item").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

def get_items(item_id):
    try:
        response = supabase.table("item").select("*").eq("id", item_id).execute()
        return response.data 
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Mettre à jour un item

def update_item(item_id, update_data):
    try:
        response = supabase.table("item").update(update_data).eq("id", item_id).execute()
        return response.data
    except Exception as e:
        print(f"Error update in : {e}")
        return None
a
# Supprimer un item

def delete_item(item_id):
    try:
        assign_delete = supabase.table("assign").select("*") \
            .eq("item", item_id).execute()
        if assign_delete.data:
            [supabase.table("assigne") \
             .delete().eq("id", assign["id"]).execute() \
             for assign in assign_delete.data]
        response = supabase.table("item") \
            .delete().eq("id", item_id).execute()
        return response.data
    except Exception as e:
        print(f"Error delete in : {e}")
        return None

# Lire tous les items d'un event
def get_items_event(event_id):
    try:
        response = supabase.table("item").select("*").eq("event", event_id).execute()
        data = response.data
        return data
    except Exception as e:
        print(f"Error get in : {e}")
        return None
