# Routes pour les scans (Nmap, Metasploit, OWASP ZAP)
from flask import Blueprint, request, jsonify
from utils.scanner import run_nmap_scan
from flask_jwt_extended import jwt_required

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/nmap", methods=["POST"])
@jwt_required()
def nmap_scan():
    data = request.get_json()
    target = data.get("target")
    if not target:
        return jsonify({"message": "Target is required"}), 400
    result = run_nmap_scan(target)
    return jsonify({"scan_result": result})
