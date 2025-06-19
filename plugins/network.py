def run():
    import socket
    import psutil

    interfaces = psutil.net_if_addrs()
    info = {}

    for iface, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                info[iface] = addr.address

    return info
