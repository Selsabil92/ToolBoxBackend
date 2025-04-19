
def generate_jwt(data, secret_key):
    # Code pour générer le JWT
    import jwt
    token = jwt.encode(data, secret_key, algorithm="HS256")
    return token
