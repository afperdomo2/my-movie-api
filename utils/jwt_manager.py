from jwt import decode, encode


def create_token(data: dict) -> str:
    token: str = encode(payload=data, key="misecret123", algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    decoded: dict = decode(token, key="misecret123", algorithms=["HS256"])
    return decoded
