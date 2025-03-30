from graphql import GraphQLError

from flaskr.graphql.utils.errors.ERROR import ERRORS

"""
This module contains all the functions to validate the inputs of the tasks and verify

Functions:

    validate_task_name: function to validate the name of the task
    validate_task_description: function to validate the description of the task
    validate_task_tag: function to validate the tag of the task
    validate_task_rating: function to validate the rating of the task

The functions rely on user authentication and various utility functions to validate
inputs and update the Redis database.

"""


def validate_task_name(name: str):
    if name == "":
        raise GraphQLError(
            ERRORS["INVALID_NAME"]["message"],
            extensions=ERRORS["INVALID_NAME"]["extensions"],
        )


def validate_task_description(description: str):
    if description == "":
        raise GraphQLError(
            ERRORS["INVALID_DESCRIPTION"]["message"],
            extensions=ERRORS["INVALID_DESCRIPTION"]["extensions"],
        )


def validate_task_tag(tag: str):
    if tag == "":
        raise GraphQLError(
            ERRORS["INVALID_TAG"]["message"],
            extensions=ERRORS["INVALID_TAG"]["extensions"],
        )


def validate_task_rating(rating: int):
    if rating < 0 or rating > 100:
        raise GraphQLError(
            ERRORS["INVALID_RATING"]["message"],
            extensions=ERRORS["INVALID_RATING"]["extensions"],
        )
    if not isinstance(rating, int):
        raise GraphQLError(
            ERRORS["INVALID_RATING"]["message"],
            extensions=ERRORS["INVALID_RATING"]["extensions"],
        )


def verify_task_notInProject(idTask: str, project: dict):
    if idTask not in [task["id"] for task in project["tasks"]]:
        raise GraphQLError(
            ERRORS["TASK_NOT_IN_PROJECT"]["message"],
            extensions=ERRORS["TASK_NOT_IN_PROJECT"]["extensions"],
        )


def verify_task_userNotCreator(id: str, task: dict):
    if task["who_create"] != id:
        raise GraphQLError(
            ERRORS["UNAUTHORIZED"]["message"],
            extensions=ERRORS["UNAUTHORIZED"]["extensions"],
        )


def verify_task_someoneAssigned(task: dict):
    if task["assignee"] != "":
        raise GraphQLError(
            ERRORS["TASK_ALREADY_ASSIGNED"]["message"],
            extensions=ERRORS["TASK_ALREADY_ASSIGNED"]["extensions"],
        )


def verify_task_justTheAssignee(id: str, task: dict):
    if id != task["assignee"]:
        raise GraphQLError(
            ERRORS["UNAUTHORIZED"]["message"],
            extensions=ERRORS["UNAUTHORIZED"]["extensions"],
        )
