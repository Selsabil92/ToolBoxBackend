import os
import json
from datetime import datetime
from services.crypto_utils import encrypt_data, decrypt_data  # Sécurité

# 📁 Dossiers requis
REPORT_FOLDER = "reports"
TEMPLATE_FOLDER = "saved_reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)

# 🔐 Génération d’un rapport JSON chiffré dans /reports/
def generate_report(scan_results=None, vulnerabilities=None):
    if not scan_results:
        scan_results = []
    if not vulnerabilities:
        vulnerabilities = []

    for item in scan_results:
        if 'scan_output' in item:
            try:
                item['scan_output'] = encrypt_data(item['scan_output'])
            except Exception as e:
                item['scan_output'] = f"[Erreur de chiffrement] {str(e)}"

    report = {
        "report_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "scan_results": scan_results,
        "vulnerabilities": vulnerabilities,
    }

    filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    path = os.path.join(REPORT_FOLDER, filename)

    try:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)
        return {
            "status": "success",
            "message": f"Report generated successfully: {filename}",
            "report_filename": filename
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# 🧾 Génère un rapport HTML ou TXT lisible à partir de données chiffrées
def generate_and_save_report(scan_data, export_format="html"):
    target_ip = scan_data.get("target_ip", "inconnu").replace(".", "-")
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    filename = f"{timestamp}_resultat_{target_ip}.{export_format}"
    filepath = os.path.join(TEMPLATE_FOLDER, filename)

    scan_type = scan_data.get("scan_type", "N/A")
    scan_output = scan_data.get("scan_output", "Aucun résultat reçu.")

    # 🔓 Tentative de déchiffrement
    try:
        scan_output = decrypt_data(scan_output)
    except Exception:
        pass  # Si déjà en clair ou non chiffré

    if export_format == "txt":
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("=== Rapport TXT ===\n")
            f.write(f"Type de scan : {scan_type}\n")
            f.write(f"Cible : {target_ip}\n\n")
            f.write(scan_output)

    elif export_format == "html":
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"><title>Rapport HTML</title></head>
<body style="font-family:sans-serif;">
  <h1>🔍 Rapport de Scan</h1>
  <p><strong>Type de scan :</strong> {scan_type}</p>
  <p><strong>IP cible :</strong> {target_ip}</p>
  <pre style="background:#111c24; color:#00ffe1; padding:10px;">{scan_output}</pre>
</body>
</html>"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

    else:
        raise ValueError("❌ Format non supporté (attendu : html ou txt)")

    return filepath
