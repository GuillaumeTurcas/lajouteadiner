from flask import Flask
from flask_cors import CORS

# Importation des contrôleurs
from controllers.user_controller import user_bp
from controllers.event_controller import event_bp
from controllers.guest_controller import guest_bp
from controllers.item_controller import item_bp
from controllers.assign_controller import assign_bp

from security_config.secret_data import secret_key

app = Flask(__name__)
app.secret_key = secret_key

CORS(app)  # Pour autoriser les requêtes Cross-Origin

# Enregistrement des Blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(event_bp, url_prefix="/api")
app.register_blueprint(guest_bp, url_prefix="/api")
app.register_blueprint(item_bp, url_prefix="/api")
app.register_blueprint(assign_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
