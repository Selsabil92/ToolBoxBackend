from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from services.forensic_service import analyze_file
from fpdf import FPDF
import os
import json
from io import BytesIO
from datetime import datetime
import traceback

forensic_bp = Blueprint("forensic", __name__)

UPLOAD_FOLDER = "uploads/forensic/"
SAVE_FOLDER = "saved_reports/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVE_FOLDER, exist_ok=True)

@forensic_bp.route("/api/forensic/analyze", methods=["POST"])
@jwt_required()
def forensic_analyze():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier reçu"}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({"error": "Nom de fichier vide"}), 400

    try:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        result = analyze_file(save_path)
        result["filename"] = filename

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_name = f"{timestamp}_{filename}_rapport.json"
        with open(os.path.join(SAVE_FOLDER, save_name), "w") as f:
            json.dump(result, f, indent=2)

        return jsonify(result), 200

    except Exception as e:
        print("❌ Erreur analyse :")
        print(traceback.format_exc())
        return jsonify({"error": f"Échec de l’analyse : {str(e)}"}), 500


@forensic_bp.route("/api/forensic/export/<format>", methods=["POST", "OPTIONS"])
@jwt_required()
def export_forensic_report(format):
    if request.method == "OPTIONS":
        return jsonify({"message": "Préflight OK"}), 200

    if request.content_type != "application/json":
        return jsonify({"error": "Type de contenu invalide, utilisez application/json"}), 415

    data = request.get_json()
    if not data:
        return jsonify({"error": "Aucune donnée fournie"}), 400

    filename = secure_filename(data.get("filename", "rapport_forensic"))
    content = data.get("result", {})

    try:
        buffer = BytesIO()

        if format == "json":
            buffer.write(json.dumps(content, indent=2).encode("utf-8"))
            mime = "application/json"
            ext = "json"

        elif format == "html":
            html = f"<html><head><meta charset='utf-8'><title>Rapport {filename}</title></head><body>"
            html += f"<h2>Rapport Forensique : {filename}</h2><pre>{json.dumps(content, indent=2)}</pre></body></html>"
            buffer.write(html.encode("utf-8"))
            mime = "text/html"
            ext = "html"

        elif format == "pdf":
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)

            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, f"Rapport Forensique : {filename}", ln=True)

            pdf.ln(5)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Analyse :", ln=True)
            pdf.set_font("Courier", size=10)
            pdf.multi_cell(0, 5, json.dumps(content.get("analysis", {}), indent=2))

            pdf.ln(3)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Hashs :", ln=True)
            pdf.set_font("Courier", size=10)
            pdf.multi_cell(0, 5, json.dumps(content.get("hashes", {}), indent=2))

            pdf.ln(3)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, "Type :", ln=True)
            pdf.set_font("Courier", size=10)
            pdf.multi_cell(0, 5, content.get("type", "Inconnu"))

            pdf_output = BytesIO()
            pdf.output(pdf_output)
            pdf_output.seek(0)
            return send_file(pdf_output, as_attachment=True, download_name=f"{filename}.pdf", mimetype="application/pdf")

        else:
            return jsonify({"error": "Format non supporté"}), 400

        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"{filename}.{ext}", mimetype=mime)

    except Exception as e:
        print("❌ Erreur export :")
        print(traceback.format_exc())
        return jsonify({"error": f"Erreur export : {str(e)}"}), 500
