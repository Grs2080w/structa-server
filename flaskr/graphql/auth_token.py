from graphql import GraphQLError
from jwt import exceptions

from criptography.jwt_controls import token_decode


def auth(info):
    auth: str = info.context.headers.get("Authorization")

    if not auth:
        raise GraphQLError(
            "Token Missing in Headers",
            extensions={"code": "TOKEN_MISSING", "status": 401},
        )

    token = auth[7:]

    try:
        token_decode(token)
        auth = True
    except exceptions.DecodeError:
        raise GraphQLError(
            "Token Invalid, please try again",
            extensions={"code": "TOKEN_INVALID", "status": 401},
        )

    return token_decode(token)
