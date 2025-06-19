import os
import json
from datetime import datetime
import subprocess

UPLOAD_FOLDER = 'uploads/scans'

def run_nikto_scan(target, verbose=False):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    safe_target = target.replace("/", "_").replace(".", "_").replace(":", "_")
    timestamp = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    filename = f"nikto_resultat_{safe_target}.json"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    nikto_data = {
        "target": target,
        "date": str(datetime.now()),
        "status": "success",
        "type": "nikto-scan",
        "findings": [],
        "raw_output": "",
        "saved_as": filepath
    }

    try:
        if verbose:
            print(f"[+] Lancement du scan Nikto sur {target}...")

        # ❗️Commande Nikto sans limite, et on NE TIENT PLUS COMPTE de STDERR
        command = f"nikto -host {target} -Tuning 124 -Format txt -output -"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        stdout = result.stdout
        stderr = result.stderr

        if verbose:
            print("🔧 RAW STDOUT:")
            print(stdout)
            print("🔧 RAW STDERR:")
            print(stderr)

        # ⚠️ On ignore les erreurs dans stderr tant qu'on a un résultat
        nikto_data["raw_output"] = stdout

        findings = []
        for line in stdout.splitlines():
            if line.startswith('+') and ':' in line:
                findings.append({
                    "port": 80,
                    "protocol": "http",
                    "script": line.split(':')[0].replace('+', '').strip(),
                    "output": line.strip()
                })

        nikto_data["findings"] = findings

        if verbose:
            print(f"[✓] {len(findings)} vulnérabilités extraites")
            print(f"[✓] Rapport enregistré : {filepath}")

    except subprocess.TimeoutExpired:
        nikto_data["status"] = "error"
        nikto_data["error_message"] = "Timeout atteint pour Nikto"
        if verbose:
            print("[!] Timeout atteint pour Nikto")
    except Exception as e:
        nikto_data["status"] = "error"
        nikto_data["error_message"] = str(e)
        if verbose:
            print(f"[ERREUR] {e}")

    with open(filepath, "w") as f:
        json.dump(nikto_data, f, indent=4)

    return nikto_data
