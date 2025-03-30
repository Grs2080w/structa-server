import json
from datetime import date
from uuid import uuid4

import bcrypt
from graphql import GraphQLError

from criptography.jwt_controls import token_encode
from flaskr.graphql.auth.auth_token import auth, authTokenOTP
from flaskr.graphql.utils.user_validations import validate_email
from flaskr.redis.redis_users_controls import (
    addNewUser,
    alterUser,
    cleanNotifications,
    deleteExistentUser,
    findUserByParam,
    loginUser,
    loginUserwithOtp,
    searchDataUser,
    tokenAfterOtp,
)

"""
This module contains mutation resolvers for user-related operations in a GraphQL API.

Functions:
- createUser: Creates a new user and stores it in the Redis database.
- deleteUser: Deletes an existing user.
- changeEmailUser: Changes the email of an existing user.
- changeAvatarUrlUser: Changes the avatar_url of an existing user.
- turnOTPUser: Toggles the One Time Password (OTP) for an existing user.
- verifyOtp: Verifies the OTP of an existing user.
- userLogin: Logs in an existing user, returns a JWT with user data.
- cleanNotificationsUser: Cleans all notifications of an existing user.

The functions rely on user authentication and various utility functions to validate
inputs and update the Redis database.
"""


def createUser(obj, info, name, username, password):
    password_byte = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_byte, bcrypt.gensalt())

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
        "notifications": ["Welcome to the platform!"],
        "email": "",
        "otp": False,
    }

    if findUserByParam("username", username):
        raise GraphQLError(
            f"Username {username} already exists, try again",
            extensions={"code": "USERNAME_ALREADY_EXISTS", "status": 400},
        )

    addNewUser(newUser)
    return json.loads(json.dumps(newUser))


def deleteUser(obj, info):
    idUser, username = auth(info).values()
    user = searchDataUser(idUser)
    deleteExistentUser(idUser)
    return json.loads(user[0])


def changeAvatarUrlUser(obj, info, avatarUrl):
    idUser, username = auth(info).values()
    user = json.loads(searchDataUser(idUser)[0])
    user.update({"avatar_url": avatarUrl})
    alterUser(idUser, user)
    return {"status": "avatar_url updated"}


def cleanNotificationsUser(obj, info):
    id, username = auth(info).values()

    if cleanNotifications(id):
        return {"status": "Notifications Cleaned"}


def changeEmailUser(obj, info, email):
    idUser, username = auth(info).values()
    user = json.loads(searchDataUser(idUser)[0])

    if not validate_email(email):
        raise GraphQLError(
            "Insert a valid email",
            extensions={"code": "INVALID_EMAIL", "status": 400},
        )

    if not user.get("email"):
        user["email"] = ""

    user.update({"email": email})
    alterUser(idUser, user)
    return {"status": "email updated"}


def turnOTPUser(obj, info):
    idUser, username = auth(info).values()
    user = json.loads(searchDataUser(idUser)[0])

    if not user.get("otp"):
        user["otp"] = False

    if user["otp"]:
        user.update({"otp": False})
    else:
        user.update({"otp": True})

    alterUser(idUser, user)
    return {"status": "otp updated"}


def userLogin(obj, info, username, password):
    payload = json.loads(loginUser(username, password))

    user = json.loads(searchDataUser(payload["id"])[0])

    if not user["otp"]:
        return {"data": token_encode(payload)}

    payloadOTP = json.loads(loginUserwithOtp(payload["id"]))
    return {"data": token_encode(payloadOTP)}


def verifyOtp(obj, info, otp):
    id = authTokenOTP(info)["id"]

    user = json.loads(searchDataUser(id)[0])

    if user["code_otp"] == otp:
        print("username", user["username"])
        print("password", user["password"])
        payload = json.loads(tokenAfterOtp(id))
        return {"data": token_encode(payload)}

    raise GraphQLError(
        "Invalid OTP",
        extensions={"code": "INVALID_OTP", "status": 400},
    )
