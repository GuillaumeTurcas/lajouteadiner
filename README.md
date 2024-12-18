# La Joute à Dîner

**La Joute à Dîner** est un projet conçu pour simplifier l'organisation des soirées entre amis. Ce système permet de gérer les invités, de suivre les contributions attendues et d'assurer une organisation fluide.

---

## 📋 Table des Matières
1. [Fonctionnalités](#fonctionnalites)
2. [Prérequis](#prerequis)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Démarrage](#demarrage)
6. [Structure du projet](#structure-du-projet)
7. [Documentation de l'API](#documentation-de-lapi)
8. [Technologies utilisées](#technologies-utilisees)
9. [Contribuer](#contribuer)
10. [Licence](#licence)

---

## ⚙️ Fonctionnalités

- **Gestion des utilisateurs** : Ajout, modification et suppression des invités.
- **Connexion sécurisée avec Supabase** pour la gestion des données utilisateurs et des soirées.
- **API RESTful** : Construite avec Flask pour une interaction flexible.
- **Documentation Swagger** : L'API est documentée et accessible depuis `/doc`.
- **Personnalisation** : Configuration sécurisée via un fichier `.env`.

---

## 🛠️ Prérequis

Assurez-vous d'avoir les outils suivants installés sur votre machine :

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/) pour la gestion des paquets
- [Supabase](https://supabase.io/) pour les bases de données
- [Git](https://git-scm.com/) pour cloner le projet

---

## 🚀 Installation

Clonez le projet et installez les dépendances :

```bash
# Clonez le dépôt
git clone https://github.com/votreutilisateur/lajouteadiner.git
cd lajouteadiner

# Activez l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate

# Installez les dépendances
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Configurez les clés et secrets nécessaires en créant le fichier suivant :
`backend/security_config/secret_data.py`
avec ce modèle :

```python
SUPABASE_URL = "url"
SUPABASE_KEY = "key"

secret_key = "Secret Key"

default_password = "default".encode("utf-8")
pepper = "pepper"
iterations = 1
```

---

## ▶️ Démarrage

Démarrez l'API Flask localement :

```bash
python backend/app.py
```

L'API sera disponible sur `http://127.0.0.1:5000`.

Accédez à la documentation Swagger via :

```
http://127.0.0.1:5000/doc
```

---

## 📂 Structure du Projet

```plaintext
lajouteadiner/
├── backend/               # Code source de l'API Flask
│   ├── app.py            # Point d'entrée principal
│   ├── routes/           # Définition des routes API
│   ├── models/           # Modèles de données
│   ├── utils/            # Fonctions utilitaires
│   ├── auth.py           # Gestion de l'authentification
│
├── .gitignore            # Fichiers à ignorer par Git
├── requirements.txt      # Liste des dépendances Python
├── README.md             # Documentation principale
└── venv/                 # Environnement virtuel Python
```

---

## 📜 Documentation de l'API

La documentation complète de l'API est disponible sur Swagger, accessible localement après le démarrage du projet :

```plaintext
http://127.0.0.1:5000/doc
```

Exemples de routes :
- `GET /api/users` : Récupère la liste des utilisateurs.
- `POST /api/users` : Ajoute un nouvel utilisateur.
- `DELETE /api/users/{id}` : Supprime un utilisateur.

---

## 🛠️ Technologies Utilisées

- **Backend** : Flask
- **Base de données** : Supabase
- **Langage** : Python
- **Documentation** : Swagger
- **Environnement** : Virtualenv

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Pour proposer des modifications :

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité :
   ```bash
   git checkout -b nouvelle-fonctionnalite
   ```
3. Committez vos changements :
   ```bash
   git commit -m "Ajout d'une nouvelle fonctionnalité"
   ```
4. Poussez vos modifications :
   ```bash
   git push origin nouvelle-fonctionnalite
   ```
5. Créez une Pull Request.

---

## 📄 Licence

Ce projet est sous licence libre.
