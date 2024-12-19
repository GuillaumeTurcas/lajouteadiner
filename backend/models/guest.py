import os
from config import get_supabase_client
from models.user import *
from models.event import *

# Initialisation du client Supabase
supabase = get_supabase_client()

# CRUD pour la table "guest"

def create_guest(user, event):
    """
    Ajoute un nouvel invité à un événement si celui-ci n'existe pas déjà.

    :param user: ID de l'utilisateur invité
    :param event: ID de l'événement
    :return: Données de l'invité créé ou message d'erreur en cas d'erreur
    """
    try:
        verif_guest = supabase.table("guest").select("*").execute().data
        if verif_guest:
            for guest in verif_guest:
                if guest["user"] == user and guest["event"] == event:
                    return {"error": "Guest already exists"}
        response = supabase.table("guest").insert({
            "user": user,
            "event": event,
            "accept": False
        }).execute()
        return response.data
    except Exception as e:
        return {"error": f"Error creating guest: {e}"}


def get_guests():
    """
    Récupère tous les invités.

    :return: Liste des invités ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("guest").select("*").execute()
        return response.data
    except Exception as e:
        return {"error": f"Error retrieving guests: {e}"}


def get_guest(guest_id):
    """
    Récupère les détails d'un invité spécifique par son ID.

    :param guest_id: ID de l'invité
    :return: Données de l'invité ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("guest").select("*").eq("id", guest_id).execute()
        return response.data[0]
    except Exception as e:
        return {"error": f"Error retrieving guest: {e}"}


def accept_guest(guest_id, data):
    """
    Change le statut d'acceptation d'un invité.

    :param guest_id: ID de l'invité
    :return: Données mises à jour de l'invité ou message d'erreur en cas d'erreur
    """
    try:
        response = (
            supabase.table("guest")
            .update({
                "accept": data["accept"]
                })
            .eq("id", guest_id)
            .execute()
        )
        return response.data
    except Exception as e:
        return {"error": f"Error updating guest: {e}"}


def delete_guest(guest_id):
    """
    Supprime un invité.

    :param guest_id: ID de l'invité à supprimer
    :return: Données supprimées ou message d'erreur en cas d'erreur
    """
    try:
        response = supabase.table("guest").delete().eq("id", guest_id).execute()
        return response.data
    except Exception as e:
        return {"error": f"Error deleting guest: {e}"}


def items_for_a_guest(guest_id):
    """
    Récupère tous les items assignés à un invité pour un événement spécifique.

    :param guest_id: ID de l'invité
    :return: Liste des items ou message d'erreur en cas d'erreur
    """
    try:
        assigns = (
            supabase.table("assign")
            .select("*")
            .eq("guest", guest_id)
            .execute()
            .data
        )
        response = [
            supabase.table("item")
            .select("*")
            .eq("id", assign["item"])
            .execute()
            .data[0]
            for assign in assigns
        ]
        return response
    except Exception as e:
        return {"error": f"Error retrieving items for guest: {e}"}
