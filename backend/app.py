from flask import Flask, request
from flask_restx import Api
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta

# Importation des contrôleurs
from controllers.user_controller import user_ns
from controllers.event_controller import event_ns
from controllers.guest_controller import guest_ns
from controllers.item_controller import item_ns
from controllers.assign_controller import assign_ns

# Importation de la Secret Key 
from security_config.secret_data import secret_key

# Initialisation de l'application Flask
app = Flask(__name__)
app.secret_key = secret_key

# Configuration de JWT
app.config['JWT_SECRET_KEY'] = secret_key  # Utilisation de la même clé secrète
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]  # Utiliser des cookies pour stocker les tokens
app.config["JWT_COOKIE_SECURE"] = True  # True en production (pour HTTPS uniquement)
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
app.config["JWT_COOKIE_CSRF_PROTECT"] = False
# Initialisation de JWT
jwt = JWTManager(app)

# Initialisation de l'API Flask-RESTx
api = Api(app, version='1.0', 
          title='lajoutadiner API',
          doc='/doc',
          base_url='/api',
          description='API du projet lajoutadiner sur modèle MVC.')

# Enregistrement des Blueprints
api.add_namespace(user_ns)
api.add_namespace(event_ns)
api.add_namespace(guest_ns)
api.add_namespace(item_ns)
api.add_namespace(assign_ns)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')