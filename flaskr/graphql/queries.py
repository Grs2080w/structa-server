# queries.py

import json

from flaskr.graphql.auth_token import auth
from flaskr.redis.redis_controls import returnAllUsers, searchDataUser


def listUsers_resolver(obj, info):
    auth(info)
    return returnAllUsers()


def getUser_resolver(obj, info, id):
    auth(info)
    res = searchDataUser(id)
    return json.loads(res[0])


def usersCount_resolver(obj, info):
    auth(info)
    return returnAllUsers().__len__()
