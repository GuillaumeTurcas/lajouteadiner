from config import get_supabase_client

supabase = get_supabase_client()

# CRUD pour la table "user"
def create_user(name, surname, login, password, admin):
    response = supabase.table("user").insert({
        "name": name,
        "surname": surname,
        "login": login,
        "password": password,
        "admin": admin
    }).execute()
    return response.data

def get_users():
    response = supabase.table("user").select("*").execute()
    return response.data

def update_user(user_id, update_data):
    response = supabase.table("user").update(update_data).eq("id", user_id).execute()
    return response.data

def delete_user(user_id):
    response = supabase.table("user").delete().eq("id", user_id).execute()
    return response.data

