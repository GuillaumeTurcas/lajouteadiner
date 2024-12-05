import requests

BASE_URL = "http://127.0.0.1:5000/api"

def create_user():
    print("=== Ajouter un utilisateur ===")
    name = input("Nom : ")
    surname = input("Prénom : ")
    login = input("Identifiant : ")
    password = input("Mot de passe : ")
    admin = int(input("Admin (1 pour oui, 0 pour non) : "))
    user = {"name": name, "surname": surname, "login": login, "password": password, "admin": admin}
    response = requests.post(f"{BASE_URL}/users", json=user)
    print("Réponse :", response.status_code, response.json())

def list_users():
    print("=== Liste des utilisateurs ===")
    response = requests.get(f"{BASE_URL}/users")
    print("Réponse :", response.status_code, response.json())

def update_user():
    print("=== Modifier un utilisateur ===")
    user_id = input("ID de l'utilisateur à modifier : ")
    name = input("Nouveau nom : ")
    surname = input("Nouveau prénom : ")
    user = {"name": name, "surname": surname}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=user)
    print("Réponse :", response.status_code, response.json())

def delete_user():
    print("=== Supprimer un utilisateur ===")
    user_id = input("ID de l'utilisateur à supprimer : ")
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    print("Réponse :", response.status_code, response.json())

def create_event():
    print("=== Ajouter un événement ===")
    event = input("Nom de l'éènement : ")
    date = input("Date de l'événement (YYYY-MM-DDTHH:MM:SS) : ")
    place = input("Lieu de l'événement : ")
    organizer = int(input("Organisateur (id) : "))
    event = {"event": event, "date": date, "place": place, "organizer": organizer}
    response = requests.post(f"{BASE_URL}/events", json=event)
    print("Réponse :", response.status_code, response.json())

def list_events():
    print("=== Liste des événements ===")
    response = requests.get(f"{BASE_URL}/events")
    print("Réponse :", response.status_code, response.json())

def delete_event():
    print("=== Supprimer un événement ===")
    event_id = input("ID de l'événement à supprimer : ")
    response = requests.delete(f"{BASE_URL}/events/{event_id}")
    print("Réponse :", response.status_code, response.json())

def create_guest():
    print("=== Ajouter un invité ===")
    user = input("ID de l'utilisateur : ")
    event = input("ID de l'événement : ")
    role = input("Rôle de l'invité (ex : participant) : ")
    guest = {"user": user, "event": event, "role": role}
    response = requests.post(f"{BASE_URL}/guests", json=guest)
    print("Réponse :", response.status_code, response.json())

def list_guests():
    print("=== Liste des invités ===")
    response = requests.get(f"{BASE_URL}/guests")
    print("Réponse :", response.status_code, response.json())

def delete_guest():
    print("=== Supprimer un invité ===")
    guest_id = input("ID de l'invité à supprimer : ")
    response = requests.delete(f"{BASE_URL}/guests/{guest_id}")
    print("Réponse :", response.status_code, response.json())

def create_item():
    print("=== Ajouter un objet ===")
    name = input("Nom de l'objet : ")
    quantity = int(input("Quantité : "))
    description = input("Description : ")
    event = input("ID de l'événement associé : ")
    item = {"name": name, "quantity": quantity, "description": description, "event": event}
    response = requests.post(f"{BASE_URL}/items", json=item)
    print("Réponse :", response.status_code, response.json())

def list_items():
    print("=== Liste des objets ===")
    response = requests.get(f"{BASE_URL}/items")
    print("Réponse :", response.status_code, response.json())

def delete_item():
    print("=== Supprimer un objet ===")
    item_id = input("ID de l'objet à supprimer : ")
    response = requests.delete(f"{BASE_URL}/items/{item_id}")
    print("Réponse :", response.status_code, response.json())

def assign_item():
    print("=== Assigner un objet ===")
    user = input("ID de l'utilisateur : ")
    item = input("ID de l'objet : ")
    quantity = int(input("Quantité assignée : "))
    assign = {"user": user, "item": item, "quantity": quantity}
    response = requests.post(f"{BASE_URL}/assigns", json=assign)
    print("Réponse :", response.status_code, response.json())

def list_assigns():
    print("=== Liste des assignations ===")
    response = requests.get(f"{BASE_URL}/assigns")
    print("Réponse :", response.status_code, response.json())

def delete_assign():
    print("=== Supprimer une assignation ===")
    assign_id = input("ID de l'assignation à supprimer : ")
    response = requests.delete(f"{BASE_URL}/assigns/{assign_id}")
    print("Réponse :", response.status_code, response.json())

def main():
    while True:
        print("\n=== Menu ===")
        print("1. Ajouter un utilisateur")
        print("2. Liste des utilisateurs")
        print("3. Modifier un utilisateur")
        print("4. Supprimer un utilisateur")
        print("5. Ajouter un événement")
        print("6. Liste des événements")
        print("7. Supprimer un événement")
        print("8. Ajouter un invité")
        print("9. Liste des invités")
        print("10. Supprimer un invité")
        print("11. Ajouter un objet")
        print("12. Liste des objets")
        print("13. Supprimer un objet")
        print("14. Assigner un objet")
        print("15. Liste des assignations")
        print("16. Supprimer une assignation")
        print("17. Quitter")

        choice = input("Choix : ")

        if choice == "1":
            create_user()
        elif choice == "2":
            list_users()
        elif choice == "3":
            update_user()
        elif choice == "4":
            delete_user()
        elif choice == "5":
            create_event()
        elif choice == "6":
            list_events()
        elif choice == "7":
            delete_event()
        elif choice == "8":
            create_guest()
        elif choice == "9":
            list_guests()
        elif choice == "10":
            delete_guest()
        elif choice == "11":
            create_item()
        elif choice == "12":
            list_items()
        elif choice == "13":
            delete_item()
        elif choice == "14":
            assign_item()
        elif choice == "15":
            list_assigns()
        elif choice == "16":
            delete_assign()
        elif choice == "17":
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Essayez à nouveau.")

if __name__ == "__main__":
    main()

