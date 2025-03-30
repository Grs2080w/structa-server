import datetime
import json
import random
from datetime import timezone

import bcrypt
from graphql import GraphQLError
from redis.commands.json.path import Path
from redis.commands.search.query import Query

from flaskr.redis.schema.schemas import index, r
from otp.send_otp import send_code_otp

"""
This module contains all the function to interact with the user in the redis database
"""


def returnAllUsers():
    resFromQuery = index.search(Query("*"))
    user_list = [json.loads(doc.json) for doc in resFromQuery.docs]
    return user_list


def searchDataUser(id, *args):
    try:
        resFromQuery = r.json().get(f"user:{id}", *args)
        if not resFromQuery:
            raise TypeError()
        return resFromQuery, 200

    except TypeError:
        raise GraphQLError(
            f"User with id: {id} not found",
            extensions={"code": "USER_NOT_FOUND", "status": 404},
        )


def addNewUser(obj):
    r.json().set(f"user:{obj['id']}", Path.root_path(), json.dumps(obj))


def deleteExistentUser(id):
    r.delete(f"user:{id}")


def findUserByParam(param, value):
    res = index.search("*").docs
    for doc in res:
        user = json.loads(doc.json)

        if user[param] == value:
            return True


def alterUserwithNewProject(id: str, newProject: dict[str, any]):
    user = json.loads(searchDataUser(id)[0])

    userProjects: list = user["projects"]
    userProjects.append(newProject["id"])

    user.update(
        {"projects": userProjects, "project_open_count": user["project_open_count"] + 1}
    )

    r.json().set(f"user:{id}", Path.root_path(), json.dumps(user))


def alterUserwithAbortedProject(iduser: str):
    user = json.loads(searchDataUser(iduser)[0])

    user.update(
        {
            "projects_aborted_count": user["projects_aborted_count"] + 1,
        }
    )

    alterUser(iduser, user)


def alterUserwithClosedProject(iduser: str):
    user = json.loads(searchDataUser(iduser)[0])

    user.update(
        {
            "project_closed_count": user["project_closed_count"] + 1,
        }
    )

    alterUser(iduser, user)


def alterUser(iduser: str, obj: dict[str, any]):
    r.json().set(f"user:{iduser}", Path.root_path(), json.dumps(obj))


def addNotification(idUser, notification):
    user = json.loads(searchDataUser(idUser)[0])

    if not user.get("notifications"):
        user["notifications"] = []

    notifications = user["notifications"]
    notifications.append(notification)

    user.update({"notifications": notifications})

    r.json().set(f"user:{idUser}", Path.root_path(), json.dumps(user))


def cleanNotifications(idUser):
    user = json.loads(searchDataUser(idUser)[0])

    user.update({"notifications": []})

    r.json().set(f"user:{idUser}", Path.root_path(), json.dumps(user))

    return True


def loginUser(username, passwordReceived):
    response: list = index.search("*").docs

    for doc in response:
        user = json.loads(doc.json)
        passwordUser_byte = user["password"].encode("utf-8")
        passwordReceivedbyUser = passwordReceived.encode("utf-8")

        if user["username"] == username and bcrypt.checkpw(
            passwordReceivedbyUser, passwordUser_byte
        ):
            exp = int(
                (
                    datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=7)
                ).timestamp()
            )

            return json.dumps(
                {
                    "id": user["id"],
                    "username": user["username"],
                    "exp": exp,
                }
            )

    raise GraphQLError(
        "User or password incorrect",
        extensions={"code": "USER_NOT_FOUND", "status": 404},
    )


def loginUserwithOtp(idUser):
    user = json.loads(searchDataUser(idUser)[0])

    # create the code
    codeOTP = "{:06}".format(random.randint(0, 999999))

    # add the code in the user
    addOTP(idUser, codeOTP)

    # send the code by email
    send_code_otp(user["email"], codeOTP)

    exp_temp = int(
        (
            datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(minutes=5)
        ).timestamp()
    )

    return json.dumps(
        {
            "exp": exp_temp,
            "require_otp": True,
            "id": idUser,
        }
    )


def addOTP(idUser, codeOTP):
    user = json.loads(searchDataUser(idUser)[0])

    if not user.get("code_otp"):
        user["code_otp"] = ""

    user.update({"code_otp": codeOTP})

    r.json().set(f"user:{idUser}", Path.root_path(), json.dumps(user))


def tokenAfterOtp(idUser):
    user = json.loads(searchDataUser(idUser)[0])

    exp = int(
        (
            datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=7)
        ).timestamp()
    )

    return json.dumps(
        {
            "id": user["id"],
            "username": user["username"],
            "exp": exp,
        }
    )
