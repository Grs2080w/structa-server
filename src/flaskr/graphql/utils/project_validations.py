from graphql import GraphQLError

from flaskr.graphql.utils.errors.ERROR import ERRORS

"""
This module contains all the functions to validate the inputs in the project resolvers
"""


def verify_userAlreadyColaborator(id: str, project: dict):
    if id in [colaborator["id"] for colaborator in project["colaborators"]]:
        raise GraphQLError(
            ERRORS["USER_ALREADY_COLABORATOR"]["message"],
            extensions=ERRORS["USER_ALREADY_COLABORATOR"]["extensions"],
        )


def verify_userNotColaborator(id: str, project: dict):
    if id not in [colaborator["id"] for colaborator in project["colaborators"]]:
        raise GraphQLError(
            ERRORS["USER_NOT_COLABORATOR"]["message"],
            extensions=ERRORS["USER_NOT_COLABORATOR"]["extensions"],
        )


def validate_project_name(name: str):
    if name == "" or len(name) > 100:
        raise GraphQLError(
            "The project not be empty and must have less than 100 characters",
            extensions={"code": "INVALID_PROJECT_NAME"},
        )


def validate_project_description(description: str):
    if description == "":
        raise GraphQLError(
            "The project description not be empty",
            extensions={"code": "INVALID_PROJECT_DESCRIPTION"},
        )
