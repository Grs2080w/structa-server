from graphql import GraphQLError
from jwt import exceptions

from criptography.jwt_controls import token_decode


def auth(info) -> dict:
    """
    Verify if the Authorization token is valid.

    Args:
        info (Info): Info about the request.

    Returns:
        dict: The decoded token.

    Raises:
        GraphQLError: If the Authorization token is invalid or missing.
    """
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
