from config import get_supabase_client

supabase = get_supabase_client()

# Ajouter un objet
def create_item(name, quantity, description, event):
    response = supabase.table("item").insert({
        "name": name,
        "quantity": quantity,
        "description": description,
        "event": event
    }).execute()
    return response.data

# Lire tous les objets
def get_items():
    response = supabase.table("item").select("*").execute()
    return response.data

# Mettre à jour un objet
def update_item(item_id, update_data):
    response = supabase.table("item").update(update_data).eq("id", item_id).execute()
    return response.data

# Supprimer un objet
def delete_item(item_id):
    response = supabase.table("item").delete().eq("id", item_id).execute()
    return response.data

