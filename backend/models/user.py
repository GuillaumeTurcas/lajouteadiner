from config import get_supabase_client
from security_config.hash_password import hash_password
from security_config.secret_data import default_password

import os

supabase = get_supabase_client()

# CRUD pour la table "user"

# Créer un user

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

# Lire tous les users

def get_users():
    try:
        print('ici')
        response = supabase.table("user").select(
            "id", "name", "surname").execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire un user

def get_user(user_id):
    try:
        response = supabase.table("user").select(
            "id", "name", "surname", "admin", "token") \
            .eq("id", user_id).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Modifier un user

def update_user(user_id, update_data):
    try:
        response = supabase.table("user").update(
            update_data).eq("id", user_id).execute()
    except Exception as e:
        print(f"Error update in : {e}")
        return None
    return response.data

# Supprimer un user

def delete_user(user_id):
    try:
        event_delete = supabase.table("event").select("*")\
            .eq("organizer", user_id).execute()
        if event_delete.data:
            [supabase.table("event") \
             .delete().eq("id", event["id"]).execute() \
             for event in event_delete.data]
        guest_delete = supabase.table("event").select("*")\
            .eq("user", user_id).execute()
        if guest_delete.data:
            [supabase.table("guest") \
             .delete().eq("id", guest["id"]).execute() \
             for guest in guest_delete.data]
        assign_delete = supabase.table("assign").select("*")\
            .eq("user", user_id).execute()
        if assigne_delete.data:
            [supabase.table("assign") \
             .delete().eq("id", assign["id"]).execute() \
             for assign in assign_delete.data]
        response = supabase.table("user") \
            .delete().eq("id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error delete in : {e}")
        return None
    return response.data

##### Login user #####

# Login

def login_user(login, password):
    try:
        response = supabase.table("user").select(
            "*").eq("login", login).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(password, bytes.fromhex(user["salt"])):
                return get_user(user["id"])
            print(f"Mot de passe incorrect pour {user["login"]}")
        return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

# Change password


def change_password(user_id, old_password, new_password):
    try:
        response = supabase.table("user").select(
            "*").eq("id", user_id).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(old_password, bytes.fromhex(user["salt"])):
                hashed_password = hash_password(
                    new_password, bytes.fromhex(user["salt"]))
                supabase.table("user").update(
                    {"password": hashed_password}).eq("id", user_id).execute()
                return True
        return False
    except Exception as e:
        print(f"Error changing password: {e}")
        return False


def reset_password(user_id):
    try:
        user = supabase.table("user").select(
            "*").eq("id", user_id).execute().data[0]
        new_password = hash_password(
            str(default_password), bytes.fromhex(user["salt"]))
        supabase.table("user").update(
            {"password": new_password}).eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"Error changing password: {e}")
        return False
