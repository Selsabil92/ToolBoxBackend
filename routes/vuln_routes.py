# routes/vuln_routes.py
from flask import Blueprint, request, jsonify
from services.vuln_service import scan_vulnerabilities
from services.exploit_generator import generate_exploits_from_vulns
import os
import json
from datetime import datetime

vuln_bp = Blueprint('vuln', __name__)

@vuln_bp.route('/api/vuln/scan', methods=['POST'])
def launch_vuln_scan():
    data = request.get_json()
    target = data.get("target")

    if not target:
        return jsonify({"error": "Target manquant"}), 400

    # Lancer le scan avec détails
    result = scan_vulnerabilities(target, verbose=True)

    # Sauvegarder le rapport
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace('.', '_')
    filename = f"vuln_result_{safe_target}_{now}.json"
    folder = "uploads/vulns"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)

    try:
        with open(path, "w") as f:
            json.dump(result, f, indent=2)
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la sauvegarde : {str(e)}"}), 500

    # ⚙ Générer les exploits en fonction des CVEs trouvées
    try:
        generate_exploits_from_vulns(
            vuln_folder="uploads/vulns",
            output_folder="uploads/exploits",
            mapping_file="data/cve_mapping.json"
        )
    except Exception as e:
        return jsonify({"error": f"Erreur génération exploits : {str(e)}"}), 500

    # Retourne immédiatement le fichier JSON complet
    return jsonify({
        "message": "Scan terminé ✅",
        "results": result,
        "filename": filename,
        "exploit_sync": "done"
    })
