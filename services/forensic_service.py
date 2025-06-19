import subprocess
import hashlib
import os

def analyze_file(file_path):
    result = {
        "filename": os.path.basename(file_path),
        "type": "",
        "hashes": {},
        "analysis": {}
    }

    # 🔍 Détection du type de fichier
    file_type = subprocess.getoutput(f"file {file_path}")
    result["type"] = file_type

    # 🔐 Hashs (intégrité / détection malware)
    with open(file_path, 'rb') as f:
        content = f.read()
        result["hashes"]["md5"] = hashlib.md5(content).hexdigest()
        result["hashes"]["sha1"] = hashlib.sha1(content).hexdigest()
        result["hashes"]["sha256"] = hashlib.sha256(content).hexdigest()

    # 🧵 Analyse des strings (contenu lisible)
    result["analysis"]["strings"] = subprocess.getoutput(f"strings {file_path}")[:1000]

    # ⚙️ Analyse ELF (Linux) ou PE (Windows)
    if "ELF" in file_type:
        result["analysis"]["readelf"] = subprocess.getoutput(f"readelf -h {file_path}")
    elif "PE32" in file_type:
        result["analysis"]["peinfo"] = subprocess.getoutput(f"objdump -x {file_path}")

    # 🌐 Analyse réseau (fichiers .pcap)
    if file_path.endswith(".pcap") or "tcpdump capture file" in file_type:
        tshark_check = subprocess.getoutput("which tshark")
        if tshark_check:
            result["analysis"]["tshark_summary"] = subprocess.getoutput(f"tshark -r {file_path} -q -z io,phs")
        else:
            result["analysis"]["tshark_summary"] = "⚠️ tshark non installé"

    # 📜 Analyse simple de logs
    if file_path.endswith(".log") or file_path.endswith(".txt"):
        try:
            with open(file_path, "r", errors="ignore") as f:
                lines = f.readlines()
                suspicious = [l.strip() for l in lines if "error" in l.lower() or "fail" in l.lower()]
                result["analysis"]["log_keywords"] = suspicious[:50]
        except Exception as e:
            result["analysis"]["log_keywords"] = f"Erreur lecture log : {str(e)}"

    return result
