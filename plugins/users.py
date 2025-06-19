def run():
    import psutil
    users = psutil.users()
    return [u.name for u in users]
