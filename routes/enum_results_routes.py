from flask import Blueprint, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import json

enum_results_bp = Blueprint('enum_results', __name__)
SCAN_FOLDER = 'uploads/scans'

# Lister les fichiers de scan
@enum_results_bp.route('/api/enum/results', methods=['GET'])
@jwt_required()
def get_enum_results():
    if not os.path.exists(SCAN_FOLDER):
        return jsonify({"error": "Le dossier des scans n'existe pas"}), 404

    results = []
    for filename in sorted(os.listdir(SCAN_FOLDER)):
        if filename.endswith('.json'):
            filepath = os.path.join(SCAN_FOLDER, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    results.append({
                        "filename": filename,
                        "target": data.get("target"),
                        "date": data.get("date"),
                        "total_hosts": data.get("summary", {}).get("total_hosts", 0),
                        "total_open_ports": data.get("summary", {}).get("total_open_ports", 0),
                        "status": data.get("status")
                    })
            except Exception as e:
                results.append({"filename": filename, "error": str(e)})

    return jsonify(results)

# 🟢 Lire un fichier JSON de scan
@enum_results_bp.route('/api/enum/results/<filename>', methods=['GET'])
@jwt_required()
def get_enum_result(filename):
    filepath = os.path.join(SCAN_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 🟢 Supprimer un fichier de scan
@enum_results_bp.route('/api/enum/results/<filename>', methods=['DELETE'])
@jwt_required()
def delete_enum_result(filename):
    filepath = os.path.join(SCAN_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        os.remove(filepath)
        return jsonify({"message": f"{filename} supprimé ✅"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Télécharger un fichier JSON
@enum_results_bp.route('/api/enum/download/<filename>', methods=['GET'])
@jwt_required()
def download_enum_result(filename):
    filepath = os.path.join(SCAN_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404

    return send_from_directory(SCAN_FOLDER, filename, as_attachment=True)
