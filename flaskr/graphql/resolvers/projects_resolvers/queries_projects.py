import json

from flaskr.graphql.auth.auth_token import auth
from flaskr.redis.redis_projects_controls import returnAllProjects, searchProject

"""
This module contains all the querys to interact with the projects in the redis database

Functions:

    listProjects_resolver: function to return all the projects in the database
    getProjects_resolver: function to return one project by id
    projectsCount_resolver: function to return the count of all projects in the database
"""


def listProjects_resolver(obj, info):
    auth(info)
    return returnAllProjects()


def getProjects_resolver(obj, info, id):
    auth(info)
    res = searchProject(id)
    return json.loads(res[0])


def projectsCount_resolver(obj, info):
    auth(info)
    return returnAllProjects().__len__()
