from graphql import GraphQLError
from jwt import exceptions

from criptography.jwt_controls import token_decode

"""
Exceptions to handle errors in JWT

This module contains exceptions to handle errors with JWT

Functions:
    e_exception: function to handle exceptions in JWT
"""


def e_exception(
    token: str,
) -> dict:
    try:
        token_decode(token)

    except exceptions.DecodeError as e:
        print("error -> ", e)
        raise GraphQLError(
            "Token Invalid, please try again",
            extensions={"code": "TOKEN_INVALID", "status": 401},
        )
    except exceptions.ExpiredSignatureError as e:
        print("error -> ", e)
        raise GraphQLError(
            "Token Expired, please try again",
            extensions={"code": "TOKEN_EXPIRED", "status": 401},
        )
