from config import get_supabase_client

supabase = get_supabase_client()

# Créer une assignation
def create_assign(user, item, quantity):
    try:
        if verif_quantity(item, int(quantity)):
            print("Too much quantity")
            return None
        response = supabase.table("assign").insert({
            "user": user,
            "item": item,
            "quantity": quantity
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire toutes les assignations
def get_assigns():
    try:
        response = supabase.table("assign").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Mettre à jour une assignation
def update_assign(assign_id, update_data):
    try:
        if update_data["quantity"]:
            verif_assign_update = supabase.table("assign") \
                .select("*").eq("id", assign_id).execute().data[0]["quantity"]
            if verif_assign(item, update["quantity"] - verif_assign_update):
                print("Too much quantity")
                return None
        response = supabase.table("assign").update(update_data).eq("id", assign_id).execute()
        return response.data
    except Exception as e:
        print(f"Error update in : {e}")
        return None

# Supprimer une assignation
def delete_assign(assign_id):
    try:
        response = supabase.table("assign").delete().eq("id", assign_id).execute()
        return response.data
    except Exception as e:
        print(f"Error delete in : {e}")
        return None

# Obtenir tous les items d'un user pour un event
def get_assign_user(event_id, user_id):
    try:
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
    except Exception as e:
        print(f"Error get in : {e}")
        return None

def verif_quantity(item_id, quantity_assign):
    try:
        quantity = supabase.table("item") \
            .select("*").eq("id", item_id).execute().data[0]["quantity"]
        verif_assign = supabase.table("assign") \
            .select("*").eq("item", item_id).execute().data
        for assign in verif_assign:
            quantity_assign += assign["quantity"]
        return quantity_assign > quantity
    except Exception as e:
        print(f"Error get in : {e}")
        return None