def run():
    import psutil
    top = []

    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            top.append(p.info)
        except:
            pass

    # Tri par CPU décroissant
    return sorted(top, key=lambda x: x['cpu_percent'], reverse=True)[:5]
