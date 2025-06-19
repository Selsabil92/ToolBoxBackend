# ids_routes.py

from flask import Blueprint, jsonify
import os

ids_bp = Blueprint('ids', __name__)

LOG_PATH = "/var/log/suricata/fast.log"

@ids_bp.route('/api/ids/alerts', methods=['GET'])
def get_intrusion_alerts():
    if not os.path.exists(LOG_PATH):
        return jsonify({"error": "Fichier de log introuvable"}), 404

    with open(LOG_PATH, 'r') as f:
        lines = f.readlines()[-20:]  # dernières 20 alertes
    return jsonify({"alerts": lines})
