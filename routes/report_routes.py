from flask import Blueprint, jsonify, render_template, send_file, request
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from io import BytesIO
from weasyprint import HTML

report_bp = Blueprint('report', __name__)
REPORT_FOLDER = 'uploads/scans'
VULN_FOLDER = 'uploads/vulns'

def get_full_path(filename):
    for folder in [REPORT_FOLDER, VULN_FOLDER]:
        full_path = os.path.join(folder, filename)
        if os.path.exists(full_path):
            return full_path
    return None

def detect_scan_type(filename, fallback="N/A"):
    fname = filename.lower()
    if "vuln" in fname:
        return "vuln-analysis"
    elif "nikto" in fname:
        return "nikto"
    elif "zap" in fname:
        return "zap"
    elif "nmap" in fname:
        return "nmap"
    else:
        return fallback

@report_bp.route('/api/reports/download/<filename>', methods=['GET'])
@jwt_required()
def download_report_file(filename):
    file_path = get_full_path(filename)
    if not file_path:
        return jsonify({"error": "Fichier introuvable"}), 404
    return send_file(file_path, as_attachment=True, download_name=filename)

@report_bp.route('/api/report/generate/<scan_type>/<filename>', methods=['GET'])
@jwt_required()
def generate_report(scan_type, filename):
    filepath = get_full_path(filename)
    if not filepath:
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        detected_type = detect_scan_type(filename, scan_type)

        return render_template('report_template.html', data=data, scan_type=detected_type, filename=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/api/report/download/html/<scan_type>/<filename>', methods=['GET'])
@jwt_required()
def download_html(scan_type, filename):
    filepath = get_full_path(filename)
    if not filepath:
        return jsonify({"error": "Fichier introuvable"}), 404

    with open(filepath, 'r') as f:
        data = json.load(f)

    detected_type = detect_scan_type(filename, scan_type)

    rendered = render_template("report_template.html", data=data, scan_type=detected_type, filename=filename)
    buffer = BytesIO()
    buffer.write(rendered.encode("utf-8"))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=filename.replace(".json", ".html"), mimetype="text/html")

@report_bp.route('/api/report/download/pdf/<scan_type>/<filename>', methods=['GET'])
@jwt_required()
def download_pdf(scan_type, filename):
    filepath = get_full_path(filename)
    if not filepath:
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        detected_type = detect_scan_type(filename, scan_type)

        rendered = render_template("report_template.html", data=data, scan_type=detected_type, filename=filename)
        pdf_io = BytesIO()
        HTML(string=rendered).write_pdf(pdf_io)
        pdf_io.seek(0)

        return send_file(pdf_io, as_attachment=True, download_name=filename.replace(".json", ".pdf"), mimetype="application/pdf")

    except Exception as e:
        print("❌ ERREUR PDF:", str(e))
        return jsonify({"error": f"Erreur génération PDF : {str(e)}"}), 500

@report_bp.route('/api/report/download/txt/<scan_type>/<filename>', methods=['GET'])
@jwt_required()
def download_txt(scan_type, filename):
    filepath = get_full_path(filename)
    if not filepath:
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        buffer = BytesIO()
        content = f"=== Rapport TXT : {filename} ===\n"
        for key, value in data.items():
            content += f"\n{key.upper()}:\n"
            if isinstance(value, dict):
                for k, v in value.items():
                    content += f"  - {k}: {v}\n"
            elif isinstance(value, list):
                for i, item in enumerate(value, 1):
                    content += f"  [{i}] {item}\n"
            else:
                content += f"  {value}\n"

        buffer.write(content.encode('utf-8'))
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=filename.replace(".json", ".txt"), mimetype="text/plain")

    except Exception as e:
        return jsonify({"error": f"Erreur TXT : {str(e)}"}), 500

@report_bp.route('/api/reports/list', methods=['GET'])
@jwt_required()
def list_reports():
    try:
        files = []
        for folder in [REPORT_FOLDER, VULN_FOLDER]:
            if not os.path.exists(folder):
                continue

            for filename in os.listdir(folder):
                if not filename.endswith('.json'):
                    continue

                filepath = os.path.join(folder, filename)
                created_at = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                scan_type = detect_scan_type(filename, fallback="nmap")
                target = "Inconnu"

                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        target = data.get("target", "Inconnu")
                        scan_type = data.get("type", scan_type)
                except:
                    pass

                files.append({
                    "filename": filename,
                    "created_at": created_at,
                    "target": target,
                    "type": scan_type,
                    "status": "disponible"
                })

        files.sort(key=lambda x: x["created_at"], reverse=True)
        return jsonify({"success": True, "data": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@report_bp.route('/api/reports/delete/<filename>', methods=['DELETE'])
@jwt_required()
def delete_report(filename):
    filepath = get_full_path(filename)
    if not filepath:
        return jsonify({"error": "Fichier introuvable"}), 404

    try:
        os.remove(filepath)
        return jsonify({"success": True, "message": f"{filename} supprimé avec succès"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
