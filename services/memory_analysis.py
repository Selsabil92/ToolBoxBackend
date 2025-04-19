import subprocess

def run_hydra_scan(target, service, wordlist):
    command = f"hydra -l {target} -P {wordlist} {service}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
