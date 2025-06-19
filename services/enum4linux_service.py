import subprocess
import os
import datetime

UPLOAD_DIR = "uploads/scans"

def run(target_ip):
    try:
        # 📁 Création du dossier s’il n’existe pas
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        # 🕒 Format du nom de fichier
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        safe_ip = target_ip.replace('.', '-')
        filename = f"{timestamp}_enum4linux_{safe_ip}.log"
        filepath = os.path.join(UPLOAD_DIR, filename)

        # ▶️ Exécution de la commande Enum4Linux
        with open(filepath, 'w') as outfile:
            subprocess.run(["enum4linux", "-a", target_ip], stdout=outfile, stderr=subprocess.STDOUT, timeout=30)

        # 🔄 Lecture du résultat pour l'affichage
        with open(filepath, 'r') as f:
            content = f.read()

        return {
            "target": target_ip,
            "tool": "enum4linux",
            "status": "success",
            "file": filename,
            "output": content
        }

    except subprocess.CalledProcessError as e:
        return {"error": f"Erreur Enum4Linux : {e.output.decode()}"}
    except Exception as e:
        return {"error": str(e)}
