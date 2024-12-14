from config import get_supabase_client

supabase = get_supabase_client()

# Ajouter un invité
def create_guest(user, event):
    try:
        verif_guest = supabase.table("guest") \
            .select("*").execute().data
        if verif_guest:
            for guest in verif_guest:
                if guest["user"] == user and guest["event"] == event:
                    print("guest already exist")
                    return None
        response = supabase.table("guest").insert({
            "user": user,
            "event": event,
            "accept": False
        }).execute()
        return response.data
    except Exception as e:
        print(f"Error create in : {e}")
        return None

# Lire tous les invités
def get_guests():
    try:
        response = supabase.table("guest").select("*").execute()
        print(response.data)
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None

# Lire un invité
def get_guest(guest_id):
    try:
        response = supabase.table("guest") \
            .select("*").eq("id", guest_id).execute()
        return response.data[0]
    except Exception as e:
        print(f"Error get in : {e}")
        return None

def accept_guest(guest_id):
    try:
        change_accept = supabase.table("guest").select("*").eq("id", guest_id) \
            .execute().data[0]
        change_accept["accept"] = False if change_accept["accept"] else True
        response = supabase.table("guest") \
            .update(change_accept).eq("id", guest_id).execute()
        return response.data
    except Exception as e:
        print(f"Error update in : {e}")

# Supprimer un invité
def delete_guest(guest_id):
    try:
        response = supabase.table("guest").delete().eq("id", guest_id).execute()
        return response.data
    except Exception as e:
        print(f"Error delete in : {e}")
        return None

# Avoir tous les guest d'un event
def get_guests_by_event(event_id):
    try:
        response = supabase.table('guest').select('*').eq('eventId', event_id).execute()
        return response.data
    except Exception as e:
        print(f"Error get in : {e}")
        return None
