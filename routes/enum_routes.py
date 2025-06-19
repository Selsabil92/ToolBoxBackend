# routes/enum_routes.py

from flask import Blueprint, request, jsonify
from services.enum_service import nmap_scan

# Définition du blueprint avec préfixe d'URL propre
enum_bp = Blueprint("enum", __name__, url_prefix="/api/enum")

@enum_bp.route("/scan", methods=["POST"])
def launch_enum():
    data = request.get_json()
    target = data.get("target")
    scan_arguments = data.get("scan_arguments")

    if not target:
        return jsonify({"error": "Cible manquante"}), 400

    result = nmap_scan(target, scan_arguments)
    return jsonify(result)
