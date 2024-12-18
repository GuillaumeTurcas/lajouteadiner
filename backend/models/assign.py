from config import get_supabase_client
from models.event import *

# Initialisation du client Supabase
supabase = get_supabase_client()

# Créer une assignation
def create_assign(guest, item, quantity):
    """
    Crée une assignation entre un invité et un item avec une quantité spécifiée.

    :param guest: ID de l'invité
    :param item: ID de l'item
    :param quantity: Quantité assignée
    :return: Données de l'assignation créée ou message d'erreur en cas d'erreur
    """
    try:
        if verif_quantity(item, int(quantity)):
            return {"error": "Too much quanity"}
        guest_data = supabase.table("guest").select("*").eq("id", guest).execute().data[0]
        item_data = supabase.table("item").select("*").eq("id", item).execute().data[0]
        if guest_data["event"] == item_data["event"]:
            response = supabase.table("assign").insert({
                "guest": guest,
                "item": item,
                "quantity": quantity
            }).execute()
            return response.data
        else:
            return {"error": "Impossible quantity"}
    except Exception as e:
        return {"error": f"Error creating assign: {e}"}

# Lire toutes les assignations
def get_assigns():
    """
    Récupère toutes les assignations.

    :return: Liste des assignations ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("assign").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": f"Error retrieving assigns: {e}"}

# Lire une assignation par son ID
def get_assign(assign_id):
    """
    Récupère une assignation spécifique par son ID.

    :param assign_id: ID de l'assignation
    :return: Données de l'assignation ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("assign").select("*").eq("id", assign_id).execute().data[0]
        return response
    except Exception as e:
        return {"error": f"Error retrieving assign: {e}"}

# Mettre à jour une assignation
def update_assign(assign_id, update_data):
    """
    Met à jour une assignation avec les nouvelles données fournies.

    :param assign_id: ID de l'assignation
    :param update_data: Dictionnaire des champs à mettre à jour
    :return: Données mises à jour ou message d'erreur en cas d'erreur
    """
    try:
        # Récupérer les données existantes de l'assignation
        assign = supabase.table("assign").select("*").eq("id", assign_id).execute().data[0]
        item_id = assign["item"]
        event_id = supabase.table("item").select("event").eq("id", item_id).execute().data[0]["event"]

        # Si un changement de "guest" est requis
        if "guest" in update_data:
            guest_event = get_guests_event(event_id)
            guest_in_event = False
            for guest in guest_event:
                if update_data["guest"] == guest["id"]:
                    guest_in_event = True
            if guest_in_event == False:
                return {"error": "Guest is not part of the event"}

        # Vérifier la quantité si elle est cohérente
        if "quantity" in update_data:
            current_quantity = assign["quantity"]
            new_quantity = update_data["quantity"]
            if verif_quantity(item_id, new_quantity - current_quantity):
                return {"error": "Too much quanity"}

        # Effectuer la mise à jour
        response = supabase.table("assign").update(update_data).eq("id", assign_id).execute()
        return response.data
    except Exception as e:
        return {"error": f"Error updating assign: {e}"}

# Supprimer une assignation
def delete_assign(assign_id):
    """
    Supprime une assignation spécifique.

    :param assign_id: ID de l'assignation à supprimer
    :return: Données supprimées ou None en cas d'erreur
    """
    try:
        response = supabase.table("assign").delete().eq("id", assign_id).execute()
        return response.data
    except Exception as e:
        return {"error": f"Error deleting assign: {e}"}

# Vérifier la quantité d'un item pour une assignation
def verif_quantity(item_id, quantity_assign):
    """
    Vérifie si la quantité totale assignée dépasse la quantité disponible pour un item.

    :param item_id: ID de l'item
    :param quantity_assign: Quantité à vérifier
    :return: True si la quantité dépasse, sinon False
    """
    try:
        quantity = supabase.table("item").select("*").eq("id", item_id).execute().data[0]["quantity"]
        verif_assign = supabase.table("assign").select("*").eq("item", item_id).execute().data
        for assign in verif_assign:
            quantity_assign += assign["quantity"]
        return quantity_assign > quantity
    except Exception as e:
        return {"error": f"Error verifying quantity: {e}"}
