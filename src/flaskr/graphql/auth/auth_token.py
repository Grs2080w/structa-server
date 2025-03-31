from graphql import GraphQLError

from criptography.jwt_controls import token_decode
from flaskr.graphql.auth.utils.excepts import e_exception

"""
This module contains functions to verify the token in the headers of the request

Functions:

    auth: function to verify the token, return a dict with the user data if the
        token is valid
    authTokenOTP: function to verify the token, return a dict with the user data if
        the token is valid, but the user must be verified first
"""


def auth(info) -> dict:
    auth: str = info.context.headers.get("Authorization")

    if not auth:
        raise GraphQLError(
            "Token Missing in Headers",
            extensions={"code": "TOKEN_MISSING", "status": 401},
        )

    token = auth[7:]

    e_exception(token)

    token = token_decode(token)

    if token.get("require_otp"):
        raise GraphQLError(
            "This user in not verified, please check your email",
            extensions={"code": "USER_NOT_VERIFIED", "status": 401},
        )

    del token["exp"]
    return token


def authTokenOTP(info) -> dict:
    auth: str = info.context.headers.get("Authorization")

    if not auth:
        raise GraphQLError(
            "Token Missing in Headers",
            extensions={"code": "TOKEN_MISSING", "status": 401},
        )

    token = auth[7:]

    e_exception(token)

    token = token_decode(token)

    del token["exp"]
    del token["require_otp"]
    return token


def verifyToken(token) -> dict:
    try:
        token_decode(token)
    except Exception:
        return None

    token = token_decode(token)

    if not token.get("id"):
        return None

    return token["id"]
