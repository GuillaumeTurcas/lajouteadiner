import os
from config import get_supabase_client
from security_config.hash_password import hash_password
from security_config.secret_data import default_password

# Initialisation du client Supabase
supabase = get_supabase_client()

# CRUD pour la table "user"

# Créer un utilisateur
def create_user(name, surname, login, password, admin):
    """
    Crée un nouvel utilisateur dans la table "user".

    :param name: Prénom de l'utilisateur
    :param surname: Nom de famille de l'utilisateur
    :param login: Login de l'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param admin: Statut d'administrateur
    :return: Données de l'utilisateur créé ou None en cas d'erreur
    """
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
        print(f"Error creating user: {e}")
        return None

# Récupérer tous les utilisateurs
def get_users():
    """
    Récupère tous les utilisateurs avec leurs identifiants, prénoms et noms.

    :return: Liste des utilisateurs ou None en cas d'erreur
    """
    try:
        response = supabase.table("user").select("id", "name", "surname").execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return None

# Récupérer un utilisateur par son ID
def get_user(user_id):
    """
    Récupère les détails d'un utilisateur spécifique par son ID.

    :param user_id: ID de l'utilisateur
    :return: Données de l'utilisateur ou None en cas d'erreur
    """
    try:
        response = supabase.table("user").select("id", "name", "surname", "admin", "token").eq("id", user_id).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error retrieving user: {e}")
        return None

# Mettre à jour un utilisateur
def update_user(user_id, update_data):
    """
    Met à jour les données d'un utilisateur.

    :param user_id: ID de l'utilisateur à mettre à jour
    :param update_data: Dictionnaire des champs à mettre à jour
    :return: Données mises à jour ou None en cas d'erreur
    """
    try:
        if "password" in update_data:
            del update_data["password"]
        response = supabase.table("user").update(update_data).eq("id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error updating user: {e}")
        return None

# Supprimer un utilisateur
def delete_user(user_id):
    """
    Supprime un utilisateur et toutes ses relations dans d'autres tables (events, guests, etc.).

    :param user_id: ID de l'utilisateur à supprimer
    :return: Données supprimées ou None en cas d'erreur
    """
    try:
        # Supprimer l'utilisateur
        response = supabase.table("user").delete().eq("id", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error deleting user: {e}")
        return None

# Authentification et gestion des mots de passe

# Authentifier un utilisateur
def login_user(login, password):
    """
    Authentifie un utilisateur avec son login et son mot de passe.

    :param login: Login de l'utilisateur
    :param password: Mot de passe de l'utilisateur
    :return: Données de l'utilisateur authentifié ou None en cas d'erreur
    """
    try:
        response = supabase.table("user").select("*").eq("login", login).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(password, bytes.fromhex(user["salt"])):
                return get_user(user["id"])
            print(f"Mot de passe incorrect pour {user['login']}")
        return None
    except Exception as e:
        print(f"Error logging in: {e}")
        return None

# Modifier le mot de passe d'un utilisateur
def change_password(user_id, old_password, new_password):
    """
    Change le mot de passe d'un utilisateur après vérification de l'ancien mot de passe.

    :param user_id: ID de l'utilisateur
    :param old_password: Ancien mot de passe
    :param new_password: Nouveau mot de passe
    :return: True si le mot de passe a été changé, sinon False
    """
    try:
        response = supabase.table("user").select("*").eq("id", user_id).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(old_password, bytes.fromhex(user["salt"])):
                hashed_password = hash_password(new_password, bytes.fromhex(user["salt"]))
                supabase.table("user").update({"password": hashed_password}).eq("id", user_id).execute()
                return True
        return False
    except Exception as e:
        print(f"Error changing password: {e}")
        return False

# Réinitialiser le mot de passe d'un utilisateur
def reset_password(user_id):
    """
    Réinitialise le mot de passe d'un utilisateur au mot de passe par défaut.

    :param user_id: ID de l'utilisateur
    :return: True si le mot de passe a été réinitialisé, sinon False
    """
    try:
        user = supabase.table("user").select("*").eq("id", user_id).execute().data[0]
        new_password = hash_password(str(default_password), bytes.fromhex(user["salt"]))
        supabase.table("user").update({"password": new_password}).eq("id", user_id).execute()
        return True
    except Exception as e:
        print(f"Error resetting password: {e}")
        return False
