# Routes pour l'analyse des résultats et détection de vulnérabilités
from flask import Blueprint, request, jsonify
from services.scan_service import analyze_results
from models import db, ScanResult

results = Blueprint('results', __name__)

@results.route('/api/results/analyze', methods=['POST'])
def analyze_scan():
    data = request.get_json()
    scan_data = data.get("scan_results")

    if not scan_data:
        return jsonify({"error": "Données de scan requises"}), 400

    analysis = analyze_results(scan_data)
    return jsonify(analysis)
