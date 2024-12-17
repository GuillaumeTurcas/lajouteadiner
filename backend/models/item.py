import os
from config import get_supabase_client
from models.user import *
from models.event import *

# Initialisation du client Supabase
supabase = get_supabase_client()

# CRUD pour la table "item"

# Ajouter un item
def create_item(name, quantity, description, event):
    """
    Crée un nouvel item dans la table "item".

    :param name: Nom de l'item
    :param quantity: Quantité de l'item
    :param description: Description de l'item
    :param event: ID de l'événement associé
    :return: Données de l'item créé ou None en cas d'erreur
    """
    try:
        response = supabase.table("item").insert({
            "name": name,
            "quantity": quantity,
            "description": description,
            "event": event
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error creating item: {e}")
        return None

# Récupérer tous les items
def get_items():
    """
    Récupère tous les items de la table "item".

    :return: Liste des items ou None en cas d'erreur
    """
    try:
        response = supabase.table("item").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving items: {e}")
        return None

# Récupérer un item par son ID
def get_item(item_id):
    """
    Récupère les détails d'un item spécifique par son ID.

    :param item_id: ID de l'item
    :return: Données de l'item ou None en cas d'erreur
    """
    try:
        response = supabase.table("item").select("*").eq("id", item_id).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving item: {e}")
        return None

# Mettre à jour un item
def update_item(item_id, update_data):
    """
    Met à jour les données d'un item.

    :param item_id: ID de l'item à mettre à jour
    :param update_data: Dictionnaire des champs à mettre à jour
    :return: Données mises à jour ou None en cas d'erreur
    """
    try:
        if "quantity" in update_data:
            init_quantity = supabase.table("item").select("*").eq("id", item_id).execute().data[0]["quantity"]
            if verif_quantity(item_id, init_quantity - update_data["quantity"]):
                print("Quantity too low")
                return None
        response = supabase.table("item").update(update_data).eq("id", item_id).execute()
        return response.data
    except Exception as e:
        print(f"Error updating item: {e}")
        return None

# Supprimer un item
def delete_item(item_id):
    """
    Supprime un item et toutes ses relations associées dans d'autres tables.

    :param item_id: ID de l'item à supprimer
    :return: Données supprimées ou None en cas d'erreur
    """
    try:
        # Supprimer l'item
        response = supabase.table("item").delete().eq("id", item_id).execute()
        return response.data
    except Exception as e:
        print(f"Error deleting item: {e}")
        return None

# Récupérer tous les items d'un événement
def get_items_event(event_id):
    """
    Récupère tous les items associés à un événement spécifique.

    :param event_id: ID de l'événement
    :return: Liste des items de l'événement ou None en cas d'erreur
    """
    try:
        response = supabase.table("item").select("*").eq("event", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error retrieving items for event: {e}")
        return None
