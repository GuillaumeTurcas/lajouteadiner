import os
from config import get_supabase_client
from security_config.hash_password import hash_password
from security_config.secret_data import default_password

# Initialisation du client Supabase
supabase = get_supabase_client()

# CRUD pour la table "user"

def create_user(name, surname, login, password, admin):
    """
    Crée un nouvel utilisateur dans la table "user".

    :param name: Prénom de l'utilisateur
    :param surname: Nom de famille de l'utilisateur
    :param login: Login de l'utilisateur
    :param password: Mot de passe de l'utilisateur
    :param admin: Statut d'administrateur
    :return: Données de l'utilisateur créé ou message d'erreur en cas d'erreur
    """
    salt = os.urandom(32)
    token = os.urandom(32).hex()
    try:
        is_login_exist = supabase.table("user") \
            .select("*") \
            .eq("login", login) \
            .execute().data 
        if is_login_exist:
            return {
                "create_user": False,
                "reason": "login already exist"
            }
        if len(password) < 8 or len(login) < 4:
            return {
                "create_user": False,
                "reason": "not enough character for login or password"
            }

        response = supabase.table("user").insert({
            "name": name,
            "surname": surname,
            "login": login,
            "password": hash_password(password, salt),
            "admin": 0,
            "salt": salt.hex(),
            "token": token
        }).execute()
        return {
            "create_user": True
        }
    except Exception as e:
        return {
            "create_user": False,
            "reason": f"Error creating user: {e}"
            }


def get_users():
    """
    Récupère tous les utilisateurs avec leurs identifiants, prénoms et noms.

    :return: Liste des utilisateurs ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("user").select("id", "name", "surname").execute()
        return response.data
    except Exception as e:
        return {"error": f"Error reading users: {e}"}


def get_user(user_id):
    """
    Récupère les éléments nécessaires d'un utilisateur spécifique par son ID.

    :param user_id: ID de l'utilisateur
    :return: Données de l'utilisateur ou message d'erreur en cas d'erreur
    """
    try:
        response = (
            supabase.table("user")
            .select("id", "name", "surname", "admin", "login")
            .eq("id", user_id)
            .execute()
        )
        return response.data[0]
    except Exception as e:
        return {"error": f"Error reading user: {e}"}


def get_full_user(user_id):
    """
    Récupère les détails d'un utilisateur spécifique par son ID.

    :param user_id: ID de l'utilisateur
    :return: Données de l'utilisateur ou message d'erreur en cas d'erreur
    """
    try:
        response = (
            supabase.table("user")
            .select("id", "name", "surname", "admin", "token", "login")
            .eq("id", user_id)
            .execute()
        )
        return response.data[0]
    except Exception as e:
        return {"error": f"Error reading user: {e}"}


def update_user(user_id, update_data):
    """
    Met à jour les données d'un utilisateur.

    :param user_id: ID de l'utilisateur à mettre à jour
    :param update_data: Dictionnaire des champs à mettre à jour
    :return: Données mises à jour ou message d'erreur en cas d'erreur
    """
    try:
        if "password" in update_data:
            del update_data["password"]
        if "login" in update_data:
            if len(update_data["login"]) < 4:
                return {
                    "update_user": False,
                    "reason": "not enough character for login"
                }
        response = (
            supabase.table("user")
            .update(update_data)
            .eq("id", user_id)
            .execute()
        )
        return response.data
    except Exception as e:
        return {"error": f"Error updating user: {e}"}


def delete_user(user_id):
    """
    Supprime un utilisateur et toutes ses relations dans d'autres tables.

    :param user_id: ID de l'utilisateur à supprimer
    :return: Données supprimées ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("user").delete().eq("id", user_id).execute()
        return response.data
    except Exception as e:
        return {"error": f"Error deleting user: {e}"}


def login_user(login, password):
    """
    Authentifie un utilisateur avec son login et son mot de passe.

    :param login: Login de l'utilisateur
    :param password: Mot de passe de l'utilisateur
    :return: Données de l'utilisateur authentifié ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("user").select("*").eq("login", login).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(
                password, bytes.fromhex(user["salt"])
            ):
                return get_full_user(user["id"])
    except Exception as e:
        return {"error": f"Error logging user: {e}"}


def change_password(user_id, old_password, new_password):
    """
    Change le mot de passe d'un utilisateur après vérification de l'ancien mot de passe.

    :param user_id: ID de l'utilisateur
    :param old_password: Ancien mot de passe
    :param new_password: Nouveau mot de passe
    :return: True si le mot de passe a été changé, sinon False
    """
    try:
        if len(new_password) < 8:
            return {
                "create_user": False,
                "reason": "not enough character for the new password"
                }
        response = supabase.table("user").select("*").eq("id", user_id).execute()
        if response.data:
            user = response.data[0]
            if user["password"] == hash_password(
                old_password, bytes.fromhex(user["salt"])
            ):
                hashed_password = hash_password(
                    new_password, bytes.fromhex(user["salt"])
                )
                supabase.table("user").update(
                    {"password": hashed_password}
                ).eq("id", user_id).execute()
                return True
        return False
    except Exception as e:
        return {"error": f"Error changing password: {e}"}


def reset_password(user_id):
    """
    Réinitialise le mot de passe d'un utilisateur au mot de passe par défaut.

    :param user_id: ID de l'utilisateur
    :return: True si le mot de passe a été réinitialisé, sinon False
    """
    try:
        user = supabase.table("user").select("*").eq("id", user_id).execute().data[0]
        new_password = hash_password(
            str(default_password), bytes.fromhex(user["salt"])
        )
        supabase.table("user").update({"password": new_password}).eq(
            "id", user_id
        ).execute()
        return True
    except Exception as e:
        return {"error": f"Error reset password: {e}"}