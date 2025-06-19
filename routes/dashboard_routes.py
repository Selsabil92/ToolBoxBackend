from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import os
import glob
import json
from datetime import datetime

print("✅ dashboard_routes.py chargé")

dashboard_bp = Blueprint('dashboard', __name__)

# 🔹 Route pour les totaux (stats)
@dashboard_bp.route('/api/dashboard/summary', methods=['GET'])
@jwt_required()
def dashboard_summary():
    try:
        scan_folder = 'uploads/scans'
        vuln_folder = 'uploads/vuln'
        exploit_folder = 'uploads/exploits'

        os.makedirs(scan_folder, exist_ok=True)
        os.makedirs(vuln_folder, exist_ok=True)
        os.makedirs(exploit_folder, exist_ok=True)

        scans = glob.glob(os.path.join(scan_folder, '*.json'))
        vulns = glob.glob(os.path.join(vuln_folder, '*.json'))
        exploits = glob.glob(os.path.join(exploit_folder, '*.json'))
        reports = glob.glob(os.path.join(scan_folder, '*.*'))  # .json, .html, .pdf, .txt...

        return jsonify({
            "success": True,
            "data": {
                "scans": len(scans),
                "vulnerabilities": len(vulns),
                "exploits": len(exploits),
                "reports": len(reports)
            }
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# 🔹 Route pour l'activité récente
@dashboard_bp.route('/api/dashboard/recent-activity', methods=['GET'])
@jwt_required()
def recent_activity():
    try:
        activities = []

        scan_folder = 'uploads/scans'
        vuln_folder = 'uploads/vuln'
        report_folder = 'uploads/scans'

        # 🔍 Derniers scans
        if os.path.exists(scan_folder):
            for filename in sorted(os.listdir(scan_folder), key=lambda f: os.path.getmtime(os.path.join(scan_folder, f)), reverse=True):
                if filename.endswith('.json'):
                    with open(os.path.join(scan_folder, filename)) as f:
                        data = json.load(f)
                    activities.append({
                        "id": f"scan-{filename}",
                        "type": "scan",
                        "target": data.get("target", "Inconnu"),
                        "status": data.get("status", "completed"),
                        "tool": data.get("tool", "nmap"),
                        "time": os.path.getmtime(os.path.join(scan_folder, filename))
                    })
                    if len(activities) >= 3:
                        break

        # 🔍 Dernières vulnérabilités
        if os.path.exists(vuln_folder):
            for filename in sorted(os.listdir(vuln_folder), key=lambda f: os.path.getmtime(os.path.join(vuln_folder, f)), reverse=True):
                if filename.endswith('.json'):
                    with open(os.path.join(vuln_folder, filename)) as f:
                        data = json.load(f)
                    activities.append({
                        "id": f"vuln-{filename}",
                        "type": "vulnerability",
                        "target": data.get("target", "Inconnu"),
                        "status": data.get("severity", "medium"),
                        "title": data.get("title", "Faille détectée"),
                        "time": os.path.getmtime(os.path.join(vuln_folder, filename))
                    })
                    if len([a for a in activities if a['type'] == 'vulnerability']) >= 2:
                        break

        # 🔍 Derniers rapports (fichiers JSON enregistrés)
        if os.path.exists(report_folder):
            for filename in sorted(os.listdir(report_folder), key=lambda f: os.path.getmtime(os.path.join(report_folder, f)), reverse=True):
                if filename.endswith('.json'):
                    activities.append({
                        "id": f"report-{filename}",
                        "type": "report",
                        "target": filename,
                        "status": "completed",
                        "time": os.path.getmtime(os.path.join(report_folder, filename))
                    })
                    if len([a for a in activities if a['type'] == 'report']) >= 2:
                        break

        # 🕒 Tri des activités du plus récent au plus ancien
        activities.sort(key=lambda x: x["time"], reverse=True)

        # 🧠 Formater les dates en ISO 8601 pour le frontend
        for act in activities:
            act["time"] = datetime.fromtimestamp(act["time"]).isoformat()

        return jsonify({"success": True, "data": activities})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
