from jwt import encode


def crete_token(data: dict):
    token: str = encode(payload=data, key="misecret123", algorithm="HS256")
    return token
