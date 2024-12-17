from config import get_supabase_client
from datetime import datetime

# Initialisation du client Supabase
supabase = get_supabase_client()

# Créer un événement
def create_event(event, date, place, organizer):
    """
    Crée un nouvel événement dans la table "event" et ajoute l'organisateur comme guest.

    :param event: Nom de l'événement
    :param date: Date de l'événement
    :param place: Lieu de l'événement
    :param organizer: ID de l'organisateur
    :return: Données de l'événement créé ou None en cas d'erreur
    """
    try:
        response = supabase.table("event").insert({
            "event": event,
            "date": date,
            "place": place,
            "organizer": organizer
        }).execute()
        supabase.table("guest").insert({
            "user": response.data[0]["organizer"],
            "event": response.data[0]["id"],
            "accept": True
        }).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error creating event: {e}")
        return None

# Lire tous les événements
def get_events():
    """
    Récupère tous les événements.

    :return: Liste des événements ou None en cas d'erreur
    """
    try:
        response = supabase.table("event").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving events: {e}")
        return None

# Lire un événement par son ID
def get_event(event_id):
    """
    Récupère les détails d'un événement spécifique par son ID.

    :param event_id: ID de l'événement
    :return: Données de l'événement ou None en cas d'erreur
    """
    try:
        response = supabase.table("event").select("*").eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving event: {e}")
        return None

# Mettre à jour un événement
def update_event(event_id, update_data):
    """
    Met à jour les données d'un événement et gère le changement d'organisateur si nécessaire.

    :param event_id: ID de l'événement
    :param update_data: Dictionnaire des champs à mettre à jour
    :return: Données mises à jour ou None en cas d'erreur
    """
    try:
        verif_organizer = supabase.table("event").select("*").eq("id", event_id).execute().data[0]["organizer"]
        guest_event = supabase.table("guest").select("*").eq("event", event_id).execute().data

        add_organizer_in_guest_list = False
        if "organizer" in update_data and update_data["organizer"] != verif_organizer:
            add_organizer_in_guest_list = all(guest["user"] != update_data["organizer"] for guest in guest_event)

        if add_organizer_in_guest_list:
            supabase.table("guest").insert({
                "user": update_data["organizer"],
                "event": event_id,
                "accept": True
            }).execute()

        response = supabase.table("event").update(update_data).eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error updating event: {e}")
        return None

# Supprimer un événement
def delete_event(event_id):
    """
    Supprime un événement.

    :param event_id: ID de l'événement à supprimer
    :return: Données supprimées ou None en cas d'erreur
    """
    try:
        response = supabase.table("event").delete().eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error deleting event: {e}")
        return None

# Lire tous les invités d'un événement
def get_guests_event(event_id):
    """
    Récupère tous les invités d'un événement spécifique.

    :param event_id: ID de l'événement
    :return: Liste des invités ou None en cas d'erreur
    """
    try:
        response = supabase.table("guest").select("*").eq("event", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving event users: {e}")
        return None

# Lire tous les événements à venir
def get_upcoming_events():
    """
    Récupère tous les événements à venir.

    :return: Liste des événements à venir ou None en cas d'erreur
    """
    try:
        today = datetime.utcnow().isoformat()
        response = supabase.table("event").select("*").gt("date", today).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving upcoming events: {e}")
        return None

# Lire tous les événements à venir pour un utilisateur
def get_upcoming_events_user(user_id):
    """
    Récupère tous les événements à venir pour un utilisateur spécifique.

    :param user_id: ID de l'utilisateur
    :return: Liste des événements ou None en cas d'erreur
    """
    try:
        today = datetime.utcnow().isoformat()
        response = supabase.table("event").select("*, guest!inner(user)").eq("guest.user", user_id).gt("date", today).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving upcoming events for user: {e}")
        return None

# Lire tous les événements pour un utilisateur
def get_events_user(user_id):
    """
    Récupère tous les événements liés à un utilisateur spécifique.

    :param user_id: ID de l'utilisateur
    :return: Liste des événements ou None en cas d'erreur
    """
    try:
        response = supabase.table("event").select("*, guest!inner(user)").eq("guest.user", user_id).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving events for user: {e}")
        return None
