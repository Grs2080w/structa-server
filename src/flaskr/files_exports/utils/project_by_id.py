from flaskr.graphql.auth.auth_token import verifyToken
from flaskr.redis.redis_projects_controls import getProject

"""
This module contains functions to get the project by id and verify if the user is the creator of the project

Functions:

    get_project_by_id_and_user_is_creator: function to get the project by id and verify if the user is the creator of the project
"""


def get_project_by_id_and_user_is_creator(idProject, tokenUser):
    project = getProject(idProject)
    idUser = verifyToken(tokenUser)

    if idUser is None:
        return {"code": "401", "message": "Token Invalid"}

    if project is None:
        return {"code": "404", "message": "Project not found"}

    if project[0]["who_create"]["id"] != idUser:
        return {"code": "403", "message": "You are not the creator of this project"}

    return project[0]
