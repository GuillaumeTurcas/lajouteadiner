from config import get_supabase_client

supabase = get_supabase_client()

# Créer une assignation
def create_assign(user, item, quantity):
    response = supabase.table("assign").insert({
        "user": user,
        "item": item,
        "quantity": quantity
    }).execute()
    return response.data

# Lire toutes les assignations
def get_assigns():
    response = supabase.table("assign").select("*").execute()
    return response.data

# Mettre à jour une assignation
def update_assign(assign_id, update_data):
    response = supabase.table("assign").update(update_data).eq("id", assign_id).execute()
    return response.data

# Supprimer une assignation
def delete_assign(assign_id):
    response = supabase.table("assign").delete().eq("id", assign_id).execute()
    return response.data

# Obtenir tous les items d'un user pour un event
def get_assign_user(event_id, user_id):
    item_ids = [item["id"] for item in supabase.table("item") \
            .select("*") \
            .eq("event", event_id) \
            .execute().data]
    return (
        [] if not item_ids else 
        supabase.table("assign")
        .select("*")
        .in_("item", item_ids)
        .eq("user", user_id)
        .execute()
        .data
    )
