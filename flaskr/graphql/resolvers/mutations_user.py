import json
from datetime import date
from uuid import uuid4

import bcrypt
from graphql import GraphQLError

from criptography.jwt_controls import token_encode
from flaskr.graphql.auth.auth_token import auth
from flaskr.redis.redis_users_controls import (
    addNewUser,
    deleteExistentUser,
    findUserByParam,
    loginUser,
    searchDataUser,
)


def createUser(obj, info, name, username, password):
    password_byte = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_byte, bcrypt.gensalt())
    ## when this hash be verified, it's necessary convert to type bytes using encode(utf-8)

    newUser = {
        "id": uuid4().__str__(),
        "name": name,
        "username": username,
        "password": hashed.decode("utf-8"),
        "first_login": date.today().__str__(),
        "avatar_url": "",
        "project_closed_count": 0,
        "project_open_count": 0,
        "projects_aborted_count": 0,
        "projects": [],
    }

    if findUserByParam("username", username):
        raise GraphQLError(
            f"Username {username} already exists, try again",
            extensions={"code": "USERNAME_ALREADY_EXISTS", "status": 400},
        )

    addNewUser(newUser)
    return json.loads(json.dumps(newUser))


def deleteUser(obj, info):
    idUser, usernameUser = auth(info).values()
    user = searchDataUser(idUser)
    deleteExistentUser(idUser)
    return json.loads(user[0])


def userLogin(obj, info, username, password):
    payload = json.loads(loginUser(username, password))
    return {"data": token_encode(payload)}
