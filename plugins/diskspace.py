def run():
    import shutil

    total, used, free = shutil.disk_usage("/")
    return {
        "total_GB": round(total / (1024**3), 2),
        "used_GB": round(used / (1024**3), 2),
        "free_GB": round(free / (1024**3), 2)
    }
