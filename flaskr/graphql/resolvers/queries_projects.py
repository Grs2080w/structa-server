import json

from flaskr.graphql.auth.auth_token import auth
from flaskr.redis.redis_projects_controls import returnAllProjects, searchProject


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
