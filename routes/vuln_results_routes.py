# routes/vuln_results_routes.py
from flask import Blueprint, jsonify, send_from_directory
from flask_jwt_extended import jwt_required
import os
import json
import re

vuln_results_bp = Blueprint('vuln_results', __name__, url_prefix="/api/vuln")
VULN_FOLDER = 'uploads/vulns'

# 🔍 Lister tous les fichiers de résultats
@vuln_results_bp.route('/results', methods=['GET'])
@jwt_required()
def list_vuln_results():
    results = []
    if not os.path.exists(VULN_FOLDER):
        return jsonify({"error": "Le dossier des vulnérabilités n'existe pas."}), 404

    for filename in sorted(os.listdir(VULN_FOLDER), reverse=True):
        if filename.endswith('.json'):
            filepath = os.path.join(VULN_FOLDER, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    results.append({
                        "filename": filename,
                        "target": data.get("target", "Inconnu"),
                        "date": data.get("date", "N/A"),
                        "status": data.get("status", "N/A"),
                        "total_vulns": len(data.get("vulnerabilities", [])),
                        "vulnerabilities": data.get("vulnerabilities", [])
                    })
            except Exception as e:
                results.append({
                    "filename": filename,
                    "error": str(e),
                    "total_vulns": 0,
                    "vulnerabilities": []
                })

    return jsonify(results)

# 📄 Lire un résultat spécifique
@vuln_results_bp.route('/results/<filename>', methods=['GET'])
@jwt_required()
def get_vuln_result(filename):
    filepath = os.path.join(VULN_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ❌ Supprimer un fichier
@vuln_results_bp.route('/results/<filename>', methods=['DELETE'])
@jwt_required()
def delete_vuln_result(filename):
    filepath = os.path.join(VULN_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        os.remove(filepath)
        return jsonify({"message": f"{filename} supprimé ✅"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ⬇ Télécharger un fichier
@vuln_results_bp.route('/download/<filename>', methods=['GET'])
@jwt_required()
def download_vuln_result(filename):
    filepath = os.path.join(VULN_FOLDER, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404

    return send_from_directory(VULN_FOLDER, filename, as_attachment=True)

# 📊 Résumé global par niveau de sévérité
@vuln_results_bp.route('/summary', methods=['GET'])
@jwt_required()
def vuln_summary():
    summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    if not os.path.exists(VULN_FOLDER):
        return jsonify(summary)

    for filename in os.listdir(VULN_FOLDER):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(VULN_FOLDER, filename)) as f:
                    data = json.load(f)
                    for vuln in data.get("vulnerabilities", []):
                        output = vuln.get("output", "").lower()

                        # 💡 Détection basique par mot-clé
                        if "critical" in output:
                            summary["critical"] += 1
                        elif "high" in output:
                            summary["high"] += 1
                        elif "medium" in output:
                            summary["medium"] += 1
                        elif "low" in output:
                            summary["low"] += 1
                        else:
                            # 🧠 BONUS : détection par score CVSS dans output
                            match = re.search(r"\b([0-9]{1,2}\.[0-9])\b", output)
                            if match:
                                score = float(match.group(1))
                                if score >= 9:
                                    summary["critical"] += 1
                                elif score >= 7:
                                    summary["high"] += 1
                                elif score >= 4:
                                    summary["medium"] += 1
                                else:
                                    summary["low"] += 1
            except Exception:
                continue

    return jsonify(summary)
