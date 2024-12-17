from functools import wraps
from flask import session, jsonify
from models.guest import *
from models.event import *
from models.item import *


# ----------------------------
# Décorateur : Login requis
# ----------------------------
def login_required(f):
    """
    Décorateur pour s'assurer que l'utilisateur est connecté.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"error": "Authentification requise"})
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Propriétaire requis
# ----------------------------
def owner_required(f):
    """
    Décorateur pour vérifier si l'utilisateur est le propriétaire.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = kwargs.get("user_id")
        if "user" not in session:
            return jsonify({"error": "Authentification requise"})
        if session["user"] != user_id:
            return jsonify(error="Accès refusé : vous n'êtes pas propriétaire")
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Admin requis
# ----------------------------
def admin_required(f):
    """
    Décorateur pour vérifier si l'utilisateur est administrateur.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session or "admin" not in session or session["admin"] != 1:
            return jsonify(error="Accès refusé : vous n'êtes pas admin")
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Admin ou propriétaire requis
# ----------------------------
def admin_or_owner_required(f):
    """
    Décorateur pour vérifier si l'utilisateur est admin ou propriétaire.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = kwargs.get("user_id")
        is_admin = session.get("admin") == 1
        is_owner = session.get("user") == user_id
        if not is_admin and not is_owner:
            return jsonify(error="Accès refusé : vous n'êtes ni admin ni propriétaire")
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Admin ou organisateur requis
# ----------------------------
def admin_or_organizer_required(f):
    """
    Décorateur pour vérifier si l'utilisateur est admin ou organisateur de l'événement.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        event = retrieve_event(kwargs)
        if not event:
            return jsonify(error="Impossible de retrouver l'événement")
        is_admin = session.get("admin") == 1
        is_organizer = session.get("user") == event["organizer"]
        if not is_admin and not is_organizer:
            return jsonify(error="Accès refusé : vous n'êtes ni admin ni organisateur")
        return f(*args, **kwargs)
    return decorated_function


# ----------------------------
# Décorateur : Admin ou invités requis
# ----------------------------
def admin_or_guests_required(f):
    """
    Décorateur pour vérifier si l'utilisateur est admin ou invité.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        event = retrieve_event(kwargs)
        if not event:
            return jsonify(error="Impossible de retrouver l'événement")
        is_admin = session.get("admin") == 1
        all_guests = get_guests_event(event["id"])
        is_guest = any(session["user"] == guest["user"] for guest in all_guests)

        if not is_admin and not is_guest:
            return jsonify(error="Accès refusé : vous n'êtes ni admin ni invité")
        return f(*args, **kwargs)
    return decorated_function



# ----------------------------
# Décorateur : Admin ou invité spécifique requis
# ----------------------------
def admin_or_guest_required(f):
    """
    Décorateur pour vérifier si l'utilisateur est admin ou un invité spécifique.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        guest = retrieve_guest(kwargs)

        # Vérifications d'authentification
        if "user" not in session or "admin" not in session:
            return jsonify(error="Authentification requise")
        # Vérification des droits
        is_admin = session["admin"] == 1  # Admin = 1
        is_guest = guest["user"] == session["user"]

        if not (is_admin or is_guest):
            return jsonify(error="Accès refusé : vous n'êtes ni admin ni invité")
        return f(*args, **kwargs)

    return decorated_function


# ----------------------------
# Fonction d'autorisation : Admin ou invité
# ----------------------------
def authorize(data):
    """
    Fonction pour vérifier si un utilisateur est admin ou invité.
    Renvoie True si autorisé, sinon False.
    """
    is_admin = session.get("admin") == 1  # Admin = 1
    event = retrieve_event_from_data(data)

    if not event:
        return {"error": "Impossible de retrouver l'événement"}
    # Récupérer tous les invités de l'événement
    all_guests = get_guests_event(event["id"])
    is_guest = any(session["user"] == guest["user"] for guest in all_guests)

    return is_admin or is_guest

# ----------------------------
# Fonctions utilitaires
# ----------------------------
def retrieve_guest(kwargs):
    """
    Récupère un invité à partir des paramètres fournis.
    """
    if "guest_id" in kwargs:
        return get_guest(kwargs["guest_id"])
    if "assign_id" in kwargs:
        assign = get_assign(kwargs["assign_id"])
        return get_guest(assign["guest_id"])
    raise ValueError("Impossible de retrouver l'invité")


def retrieve_event_from_data(data):
    """
    Récupère un événement à partir des données fournies.
    """
    if "event" in data:
        return get_event(data["event"])
    if "guest" in data:
        guest = get_guest(data["guest"])
        return get_event(guest["event_id"])
    if "item" in data:
        item = get_item(data["item"])
        return get_event(item["event_id"])
    return None
