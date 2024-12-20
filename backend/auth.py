from functools import wraps
from flask import jsonify, json
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, get_csrf_token, verify_jwt_in_request
from models.user import *
from models.guest import *
from models.event import *
from models.item import *
from models.assign import *
from datetime import datetime, timedelta
import pytz
import json


# Initialisation de JWT
jwt = JWTManager()

# ----------------------------
# Décorateur : Login requis
# ----------------------------
def login_required(f):
    """
    Décorateur pour s'assurer que l'utilisateur est connecté.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()  # Vérifie que le JWT est valide
            current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT

            if not current_user:
                return jsonify({"is_login": False, "error": "Authentication required"})
            current_user = json.loads(get_jwt_identity())
            # Vérifications supplémentaires sur l'utilisateur
            user_data = get_full_user(current_user["user_id"])
            if not user_data:
                return jsonify({"is_login": False, "error": "User not found"})
            # Vérifier la cohérence des données utilisateur
            if (
                user_data.get("admin") != current_user.get("admin") or
                user_data.get("login") != current_user.get("login")
            ):
                return jsonify({"is_login": False, "error": "Invalid session data"})

            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"is_login": False, "error": f"Error: {e}"})

    return decorated_function


# ----------------------------
# Décorateur : Propriétaire requis
# ----------------------------
def owner_required(f):
    """
    Décorateur pour vérifier si l"utilisateur est le propriétaire.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Vérifie que le JWT est valide
        current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT
        
        if not current_user:
            return jsonify({"is_login": False, "error": "Authentication required"})
        current_user = json.loads(get_jwt_identity())

        user_id = kwargs.get("user_id")
        if "user_id" not in current_user:
            return jsonify({"error": "Authentication required"})
        if current_user["user_id"] != user_id:
            return jsonify(error="Access denied : you are not the owner")
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Admin requis
# ----------------------------
def admin_required(f):
    """
    Décorateur pour vérifier si l"utilisateur est administrateur.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Vérifie que le JWT est valide
        current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT
        if not current_user:
            return jsonify({"is_login": False, "error": "Authentication required"})
        current_user = json.loads(get_jwt_identity())

        if "user_id" not in current_user or "admin" not in current_user or current_user["admin"] < 1:
            return jsonify(error="Accès denied : you are not admin")
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Admin ou propriétaire requis
# ----------------------------
def admin_or_owner_required(f):
    """
    Décorateur pour vérifier si l"utilisateur est admin ou propriétaire.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Vérifie que le JWT est valide
        current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT
        if not current_user:
            return jsonify({"is_login": False, "error": "Authentication required"})
        current_user = json.loads(get_jwt_identity())

        user_id = kwargs.get("user_id")
        is_admin = current_user.get("admin") >= 1
        is_owner = current_user.get("user_id") == user_id
        if not is_admin and not is_owner:
            return jsonify(error="Access denied : you are not admin or the owner")
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Admin ou organisateur requis
# ----------------------------
def admin_or_organizer_required(f):
    """
    Décorateur pour vérifier si l"utilisateur est admin ou organisateur de l"événement.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Vérifie que le JWT est valide
        current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT
        if not current_user:
            return jsonify({"is_login": False, "error": "Authentication required"})
        current_user = json.loads(get_jwt_identity())

        event = retrieve_event(kwargs)
        if not event:
            return jsonify(error="Event not found")
        is_admin = current_user.get("admin") >= 1
        is_organizer = current_user.get("user_id") == event["organizer"]
        
        if not is_admin and not is_organizer:
            return jsonify(error="Access denied : You are not the admin or the organizer of the event")
        return f(*args, **kwargs)
    return decorated_function



# ----------------------------
# Décorateur : Admin ou invités requis
# ----------------------------
def admin_or_guests_required(f):
    """
    Décorateur pour vérifier si l"utilisateur est admin ou invité.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Vérifie que le JWT est valide
        current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT
        if not current_user:
            return jsonify({"is_login": False, "error": "Authentication required"})
        current_user = json.loads(get_jwt_identity())

        event = retrieve_event(kwargs)
        if not event:
            return jsonify(error="Event not found")
        is_organizer = current_user["user_id"] == event["organizer"]
        is_admin = current_user.get("admin") >= 1
        all_guests = get_guests_event(event["id"])
        is_guest = any(current_user["user_id"] == guest["user"] for guest in all_guests)

        if not is_admin and not is_guest and not is_organizer:
            return jsonify(error="Access denied : You are not the admin or a guest of the event")
        return f(*args, **kwargs)
    return decorated_function



# ----------------------------
# Décorateur : Admin ou invité spécifique requis
# ----------------------------
def admin_or_guest_required(f):
    """
    Décorateur pour vérifier si l"utilisateur est admin ou un invité spécifique.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verify_jwt_in_request()  # Vérifie que le JWT est valide
        current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT
        if not current_user:
            return jsonify({"is_login": False, "error": "Authentication required"})
        current_user = json.loads(get_jwt_identity())

        guest = retrieve_guest(kwargs)
        event = retrieve_event(kwargs)
        if not event:
            return {"error": "Event not found"}
        if not guest:
            return {"error": "Guest not found"}

        # Vérifications d"authentification
        if "user" not in current_user or "admin" not in current_user:
            return jsonify(error="Authentication required")
        # Vérification des droits
        is_admin = current_user["admin"] >= 1  
        is_organizer = current_user["user_id"] == event["organizer"]
        is_guest = guest["user"] == current_user["user_id"]

        if not (is_admin or is_guest or is_organizer):
            return jsonify(error="Access denied : You are not the admin or a guest of the event")
        return f(*args, **kwargs)

    return decorated_function


# ----------------------------
# Fonction d"autorisation : Admin ou invité
# ----------------------------
def authorize(data):
    """
    Fonction pour vérifier si un utilisateur est admin ou invité.
    Renvoie True si autorisé, sinon False.
    """
    verify_jwt_in_request()  # Vérifie que le JWT est valide
    current_user = get_jwt_identity()  # Récupérer l'identité de l'utilisateur depuis le JWT
    if not current_user:
        return jsonify({"is_login": False, "error": "Authentication required"})
    current_user = json.loads(get_jwt_identity())

    is_admin = current_user.get("admin") >=1  
    event = retrieve_event_from_data(data)

    if not event:
        return {"error": "Event not found"}
    # Récupérer tous les invités de l"événement
    all_guests = get_guests_event(event["id"])
    is_guest = any(current_user["user_id"] == guest["user"] for guest in all_guests)

    return is_admin or is_guest

# ----------------------------
# Fonctions utilitaires
# ----------------------------
def retrieve_event(kwargs):
    """
    Récupère un invité à partir des paramètres fournis.
    """
    try:
        event = None
        if "event_id" in kwargs:
            event = get_event(kwargs["event_id"])
        if "guest_id" in kwargs:
            guest = get_guest(kwargs["guest_id"])
            event = get_event(guest["event"])
        if "item_id" in kwargs:
            item = get_item(kwargs["item_id"])
            event = get_event(item["event"])
        if "assign_id" in kwargs:
            assign = get_assign(kwargs["assign_id"])
            item = get_item(assign["item"])
            event = get_event(item["event"])
        return None if "error" in event else event
    except:
        return None


def retrieve_guest(kwargs):
    """
    Récupère un invité à partir des paramètres fournis.
    """
    try:
        guest = None
        if "guest_id" in kwargs:
            guest = get_guest(kwargs["guest_id"])
        if "assign_id" in kwargs:
            assign = get_assign(kwargs["assign_id"])
            guest = get_guest(assign["guest"])
        return None if "error" in guest else guest
    except:
        return None


def retrieve_event_from_data(data):
    """
    Récupère un événement à partir des données fournies.
    """
    try:
        event = None
        if "event" in data:
            event = get_event(data["event"])
        if "guest" in data:
            guest = get_guest(data["guest"])
            event = get_event(guest["event"])
        if "item" in data:
            item = get_item(data["item"])
            event = get_event(item["event"])
        if "assign" in data:
            assign = get_assign(data["assign"])
            item = get_item(assign["item"])
            event = get_event(item["event"])
        return None if "error" in event else event
    except:
        return None
