import nmap

def scan_nmap(target):
    print(f"Launching real Nmap scan on {target}")
    nm = nmap.PortScanner()
    nm.scan(hosts=target, arguments='-T4 -F')  # rapide scan

    results = []
    for host in nm.all_hosts():
        host_info = {
            'host': host,
            'hostname': nm[host].hostname(),
            'status': nm[host].state(),
            'protocols': {}
        }
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            ports_info = [
                {
                    'port': port,
                    'state': nm[host][proto][port]['state'],
                    'name': nm[host][proto][port]['name']
                }
                for port in ports
            ]
            host_info['protocols'][proto] = ports_info
        results.append(host_info)

    return results
