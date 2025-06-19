# routes/notification_routes.py
from flask import Blueprint, jsonify

# Crée le blueprint 'notifications'
notifications = Blueprint('notifications', __name__)

@notifications.route('/send_notification', methods=['POST'])
def send_notification():
    # Logique pour envoyer une notification (exemple de logique à personnaliser)
    return jsonify({"message": "Notification envoyée avec succès!"})
