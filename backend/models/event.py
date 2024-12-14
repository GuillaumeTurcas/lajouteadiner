from config import get_supabase_client
from datetime import datetime

supabase = get_supabase_client()

# Créer un événement


def create_event(event, date, place, organizer):
    try:
        response = supabase.table("event").insert({
            "event": event,
            "date": date,
            "place": place,
            "organizer": organizer
        }).execute()
        supabase.table("guest"). \
            insert({"user": response.data[0]["organizer"],
                    "event": response.data[0]["id"],
                    "role": "organizer"}).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error create in : {e}")
        return None

# Lire tous les événements


def get_events():
    try:
        response = supabase.table("event").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire un évènement


def get_event(event_id):
    try:
        response = supabase.table("event").select(
            "*").eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Mettre à jour un événement

def update_event(event_id, update_data):
    try:
        verif_organizer = supabase.table("event").select("*").eq(
            "id", event_id).execute().data[0]["organizer"]
        guest_event = supabase.table("event") \
            .select("*, guest!inner(user)") \
            .eq("guest.user", user_id) \
            .execute()
        add_organizer_in_guest_list = False
        if update_data:
            if update_data["organizer"] != verif_organizer :
                add_organizer_in_guest_list = True
                for guest in guest_event:
                    if guest["user"] == update_data["organizer"]:
                        add_organizer_in_guest_list = False
        change_organizer = supabase.table("guest").insert({
                "user": update_data["organizer"],
                "event": event_id,
                "accept": True
            }).execute() if add_organizer_in_guest_list else False
        response = supabase.table("event").update(
            update_data).eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error update in : {e}")
        return None

# Supprimer un événement

def delete_event(event_id):
    try:
        guest_delete = supabase.table("guest") \
            .select("*").eq("event", event_id).execute().data
        if guest_delete:
            [supabase.table("guest")
                .delete().eq("id", int(guest["id"])).execute() \
                for guest in guest_delete]
        item_delete = supabase.table("item") \
            .select("*").eq("event", event_id).execute().data
        if item_delete:
            [supabase.table("item")
                .delete().eq("id", int(item["id"])) \
                for item in item_delete]
        response = supabase.table("event") \
            .delete().eq("id", event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error delete in : {e}")
        return None

# Lire tous les guests d'un évènement à venir


def get_users_event(event_id):
    try:
        response = supabase.table("guest") \
            .select("user") \
            .eq("event", event_id) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None


# Lire tous les évènement à venir
def get_upcoming_events():
    try:
        today = datetime.utcnow().isoformat()
        response = supabase.table("event") \
            .select("*") \
            .gt("date", today) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire tous les events à venir pour un utilisateur


def get_upcoming_events_user(user_id):
    try:
        today = datetime.utcnow().isoformat()
        response = supabase.table("event") \
            .select("*, guest!inner(user)") \
            .eq("guest.user", user_id) \
            .gt("date", today) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire tous les events  pour un utilisateur


def get_events_user(user_id):
    try:
        response = supabase.table("event") \
            .select("*, guest!inner(user)") \
            .eq("guest.user", user_id) \
            .execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None
