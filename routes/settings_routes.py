from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import os
import json

settings_bp = Blueprint('settings', __name__)
SETTINGS_FILE = 'config/settings.json'  # à ajuster selon ton arborescence

# Charger les paramètres actuels
@settings_bp.route('/api/settings', methods=['GET'])
@jwt_required()
def get_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return jsonify(json.load(f))
    else:
        return jsonify({}), 200

# Enregistrer les paramètres
@settings_bp.route('/api/settings', methods=['POST'])
@jwt_required()
def save_settings():
    data = request.get_json()
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    return jsonify({"message": "Settings saved"}), 200
