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
    response = supabase.table("user").select("id", "name", "surname").execute()
    return response.data

def get_user(user_id):
    response = supabase.table("user").select("id", "name", "surname", "admin").eq("id", user_id).execute()
    return response.data[0]

def update_user(user_id, update_data):
    response = supabase.table("user").update(update_data).eq("id", user_id).execute()
    return response.data

def delete_user(user_id):
    response = supabase.table("user").delete().eq("id", user_id).execute()
    return response.data

def login_user(email, password):
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            user = response.data[0]
            if check_password(password, user["password"]):
                return user  # Return user details without password
        return None  # Invalid credentials
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

def change_password(user_id, old_password, new_password):
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            user = response.data[0]
            if check_password(old_password, user['password']):
                hashed_password = hash_password(new_password)
                supabase.table("users").update({"password": hashed_password}).eq("id", user_id).execute()
                return True
        return False
    except Exception as e:
        print(f"Error changing password: {e}")
        return False

