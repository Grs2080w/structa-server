import json

from flaskr.graphql.auth.auth_token import auth
from flaskr.redis.redis_users_controls import returnAllUsers, searchDataUser

"""
This module contains all the querys to interact with the users in the redis database

Functions:

    listUsers_resolver: function to return all the users in the database
    getUser_resolver: function to return one user by id
    usersCount_resolver: function to return the count of all users in the database
"""


def listUsers_resolver(obj, info):
    auth(info)
    return returnAllUsers()


def getUser_resolver(obj, info, id):
    auth(info)
    res = json.loads(searchDataUser(id)[0])
    return res


def usersCount_resolver(obj, info):
    auth(info)
    return returnAllUsers().__len__()
