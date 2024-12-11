
# La Joute à Dîner

**La Joute à Dîner** est un projet conçu pour gérer les soirées. Ce système propose des fonctionnalités robustes pour gérer les invités et ce qu'ils doivent apporter.

## Fonctionnalités

- **Gestion des utilisateurs** 
- **Connexion avec Supabase** pour la gestion des données.
- **API REST** construite avec Flask.
- **Documentation Swagger** accessible depuis /doc.
- Gestion sécurisée des données avec un fichier de configuration personnalisé.

## Prérequis

Avant de commencer, vous aurez besoin de :

- Python 3.8 ou supérieur installé sur votre machine.
- Une instance Supabase avec ses clés d'accès.

## Installation

Suivez ces étapes pour configurer le projet sur votre machine locale :

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/GuillaumeTurcas/lajouteadiner.git
   cd lajouteadiner
   ```

2. Installez l'environnement virtuel Python :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Configurez les clés et secrets nécessaires en créant le fichier suivant :
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

## Utilisation

Pour lancer le projet localement, utilisez la commande suivante :
```bash
cd backend
flask run
```

Accédez à l'interface ou aux API via `http://localhost:5000`.

## Dépendances

Les principales bibliothèques utilisées dans ce projet sont :

- Flask : un micro-framework pour créer des API web.
- Flask-CORS : pour gérer les requêtes cross-origin.
- Supabase : pour la gestion des bases de données.
- Requests : pour effectuer des requêtes HTTP.

Toutes les dépendances nécessaires sont listées dans le fichier `requirements.txt`.

## Structure du projet

- `backend/` : Contient les fichiers principaux de l'API.
- `lib/`, `include/` : Environnement Python.
- `pyvenv.cfg` : Fichier de configuration de l'environnement.

## Contribution

Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request avec vos modifications.