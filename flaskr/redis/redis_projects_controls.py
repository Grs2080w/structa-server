import json

from graphql import GraphQLError
from redis.commands.json.path import Path
from redis.commands.search.query import Query

from flaskr.redis.redis_users_controls import searchDataUser
from flaskr.redis.schema.schemas import indexProjects as index
from flaskr.redis.schema.schemas import r

"""
This module contains all the function to interact with the project in the redis database
"""


def alterProject(idProject: str, obj: dict[str, any]):
    r.json().set(f"project:{idProject}", Path.root_path(), json.dumps(obj))


def returnAllProjects():
    resFromQuery = index.search(Query("*"))
    project_list = [json.loads(doc.json) for doc in resFromQuery.docs]
    return project_list


# return all datas about a project or a specific data about a project
def searchProject(id, *args):
    try:
        resFromQuery = r.json().get(f"project:{id}", *args)
        if not resFromQuery:
            raise TypeError()
        return resFromQuery, 200

    except TypeError:
        raise GraphQLError(
            f"Project with id: {id} not found",
            extensions={"code": "PROJECT_NOT_FOUND", "status": 404},
        )


def getProject(id, *args):
    try:
        resFromQuery = r.json().get(f"project:{id}", *args)
        if not resFromQuery:
            raise TypeError()
        return json.loads(resFromQuery), 200

    except TypeError:
        return None


def addNewProject(obj):
    r.json().set(f"project:{obj['id']}", Path.root_path(), json.dumps(obj))


def deleteExistentProject(id):
    r.delete(f"project:{id}")


def userAlreadyCreateProject(user_id, nameProject):
    user = json.loads(searchDataUser(user_id)[0])
    projectsUser: list = user["projects"]

    for project in projectsUser:
        print("project", project)
        projectSearch = json.loads(searchProject(project)[0])
        nameOfProject = projectSearch["name"]
        if (
            nameOfProject == nameProject
            and projectSearch["who_create"]["id"] == user_id
        ):
            raise GraphQLError(
                "You already created a project with this name",
                extensions={"code": "PROJECT_ALREADY_EXISTS", "status": 400},
            )

    return True


def updateHistoryProject(idProject, string):
    project = json.loads(searchProject(idProject)[0])

    if not project.get("history"):
        project["history"] = []

    history = project["history"]
    history.append(string)
    project.update({"history": history})

    r.json().set(f"project:{idProject}", Path.root_path(), json.dumps(project))
