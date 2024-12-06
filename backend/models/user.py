from config import get_supabase_client
from security_config.hash_password import hash_password

import os

supabase = get_supabase_client()

# CRUD pour la table "user"
def create_user(name, surname, login, password, admin):
    salt = os.urandom(32)
    token = os.urandom(32).hex()
    try:
        response = supabase.table("user").insert({
            "name": name,
            "surname": surname,
            "login": login,
            "password": hash_password(password, salt),
            "admin": admin,
            "salt": salt.hex(),
            "token": token
        }).execute()
        return response.data

    except Exception as e:
        print(f"Error create in: {e}")
        return None



def get_users():
    response = supabase.table("user").select("id", "name", "surname").execute()
    return response.data

def get_user(user_id):
    response = supabase.table("user").select("id", "name", "surname", "admin", "token").eq("id", user_id).execute()
    return response.data[0]

def update_user(user_id, update_data):
    response = supabase.table("user").update(update_data).eq("id", user_id).execute()
    return response.data

def delete_user(user_id):
    response = supabase.table("user").delete().eq("id", user_id).execute()
    return response.data

def login_user(login, password):
    try:
        response = supabase.table("users").select("*").eq("login", login).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(password, user["salt"])
                return get_user(user["id"])
        return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def change_password(user_id, old_password, new_password):
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(old_password, user["salt"])
                hashed_password = hash_password(new_password, user["salt"])
                supabase.table("users").update({"password": hashed_password}).eq("id", user_id).execute()
                return True
        return False
    except Exception as e:
        print(f"Error changing password: {e}")
        return False
