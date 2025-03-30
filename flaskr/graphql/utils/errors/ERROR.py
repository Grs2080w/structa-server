"""
This module contains a dictionary with all the errors that can be raised in the
tasks resolver in the GraphQL API.

The errors are defined as dictionaries with the following structure:
    {
        "message": str,
        "extensions": {
            "code": str,
            "status": int
        }
    }

The message is the text of the error to be sent to the client, and the
extensions is a dictionary with additional information about the error.
"""

ERRORS = {
    "INVALID_NAME": {
        "message": "The name of the task can't be empty",
        "extensions": {"code": "INVALID_NAME", "status": 400},
    },
    "INVALID_DESCRIPTION": {
        "message": "The description of the task can't be empty",
        "extensions": {"code": "INVALID_DESCRIPTION", "status": 400},
    },
    "INVALID_TAG": {
        "message": "The tag of the task can't be empty",
        "extensions": {"code": "INVALID_TAG", "status": 400},
    },
    "INVALID_RATING": {
        "message": "The rating must be between 0 and 100",
        "extensions": {"code": "INVALID_RATING", "status": 400},
    },
    "TASK_NOT_IN_PROJECT": {
        "message": "This task is not in this project",
        "extensions": {"code": "TASK_NOT_IN_PROJECT", "status": 400},
    },
    "UNAUTHORIZED": {
        "message": "You don't have permission to change this task",
        "extensions": {"code": "UNAUTHORIZED", "status": 403},
    },
    "TASK_ALREADY_ASSIGNED": {
        "message": "This task is already assigned to someone",
        "extensions": {"code": "TASK_ALREADY_ASSIGNED", "status": 400},
    },
    "USER_ALREADY_COLABORATOR": {
        "message": "This user is already colaborator in this project",
        "extensions": {"code": "USER_ALREADY_COLABORATOR", "status": 400},
    },
    "USER_NOT_COLABORATOR": {
        "message": "This user is not colaborator in this project",
        "extensions": {"code": "USER_NOT_COLABORATOR", "status": 400},
    },
}
