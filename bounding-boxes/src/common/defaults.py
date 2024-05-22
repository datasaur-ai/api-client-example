def defaults(obj: dict | None, key: str, default):
    return obj[key] if obj and key in obj else default
