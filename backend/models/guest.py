from config import get_supabase_client
from datetime import datetime

# Initialisation du client Supabase
supabase = get_supabase_client()

# Créer un invité
def create_guest(user, event):
    """
    Ajoute un nouvel invité à un événement si celui-ci n'existe pas déjà.

    :param user: ID de l'utilisateur invité
    :param event: ID de l'événement
    :return: Données de l'invité créé ou None en cas d'erreur
    """
    try:
        verif_guest = supabase.table("guest").select("*").execute().data
        if verif_guest:
            for guest in verif_guest:
                if guest["user"] == user and guest["event"] == event:
                    print("Guest already exists")
                    return None
        response = supabase.table("guest").insert({
            "user": user,
            "event": event,
            "accept": False
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error creating guest: {e}")
        return None

# Lire tous les invités
def get_guests():
    """
    Récupère tous les invités.

    :return: Liste des invités ou None en cas d'erreur
    """
    try:
        response = supabase.table("guest").select("*").execute()
        print(response.data)
        return response.data
    except Exception as e:
        print(f"Error retrieving guests: {e}")
        return None

# Lire un invité par son ID
def get_guest(guest_id):
    """
    Récupère les détails d'un invité spécifique par son ID.

    :param guest_id: ID de l'invité
    :return: Données de l'invité ou None en cas d'erreur
    """
    try:
        response = supabase.table("guest").select("*").eq("id", guest_id).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error retrieving guest: {e}")
        return None

# Accepter ou refuser un invité
def accept_guest(guest_id):
    """
    Change le statut d'acceptation d'un invité.

    :param guest_id: ID de l'invité
    :return: Données mises à jour de l'invité ou None en cas d'erreur
    """
    try:
        change_accept = supabase.table("guest").select("*").eq("id", guest_id).execute().data[0]
        change_accept["accept"] = not change_accept["accept"]
        response = supabase.table("guest").update(change_accept).eq("id", guest_id).execute()
        return response.data
    except Exception as e:
        print(f"Error updating guest: {e}")
        return None

# Supprimer un invité
def delete_guest(guest_id):
    """
    Supprime un invité.

    :param guest_id: ID de l'invité à supprimer
    :return: Données supprimées ou None en cas d'erreur
    """
    try:
        response = supabase.table("guest").delete().eq("id", guest_id).execute()
        return response.data
    except Exception as e:
        print(f"Error deleting guest: {e}")
        return None


# Obtenir tous les items d'un invité pour un événement
def items_for_a_guest(guest_id):
    """
    Récupère tous les items assignés à un invité pour un événement spécifique.

    :param guest_id: ID de l'invité
    :return: Liste des items ou None en cas d'erreur
    """
    try:
        assigns = supabase.table("assign").select("*") \
            .eq("guest", guest_id) \
            .execute().data
        response = [supabase.table("item").select("*") \
            .eq("id", assign["item"]) \
            .execute().data[0] \
            for assign in assigns]
        return response
    except Exception as e:
        print(f"Error retrieving items for guest: {e}")
        return None