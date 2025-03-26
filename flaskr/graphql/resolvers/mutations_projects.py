import json
from datetime import date
from uuid import uuid4

from graphql import GraphQLError

from flaskr.graphql.auth.auth_token import auth
from flaskr.redis.redis_projects_controls import (
    addNewProject,
    alterProject,
    deleteExistentProject,
    searchProject,
    userAlreadyCreateProject,
)
from flaskr.redis.redis_users_controls import (
    alterUser,
    alterUserwithAbortedProject,
    alterUserwithNewProject,
    searchDataUser,
)


def createProject(obj, info, nameProject):
    idUser, usernameUser = auth(info).values()
    newProject = {
        "id": uuid4().__str__(),
        "name": nameProject,
        "description": "",
        "created": date.today().__str__(),
        "who_create": {"id": idUser, "username": usernameUser},
        "status": "active",
        "tasks": [],
        "colaborators": [{"id": idUser, "username": usernameUser}],
    }

    if userAlreadyCreateProject(idUser, nameProject):
        alterUserwithNewProject(idUser, newProject)
        addNewProject(newProject)

    return json.loads(json.dumps(newProject))


# criar uma pasta utils pra isso aq
def iAmTheBoss(project, idUser):
    if project["who_create"]["id"] != idUser:
        raise GraphQLError(
            "You don't have permission to change this project",
            extensions={"code": "UNAUTHORIZED", "status": 401},
        )


def deleteProject(obj, info, idProject):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])
    print(project)

    iAmTheBoss(project, id)

    for colaborator in project["colaborators"]:
        removeColaboratorProject(obj, info, idProject, colaborator["id"])

    # alter the status of the project in user boss
    alterUserwithAbortedProject(id, idProject)
    # delete the project on redis
    deleteExistentProject(idProject)

    return {"status": "Project Deleted"}


def addColaboratorProject(obj, info, idProject, idColaborator):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])
    iAmTheBoss(project, id)

    colaboratorToAdd = json.loads(searchDataUser(idColaborator)[0])

    # check if the user is already colaborator
    if idColaborator in [colaborator["id"] for colaborator in project["colaborators"]]:
        raise GraphQLError(
            "This user is already colaborator in this project",
            extensions={"code": "USER_ALREADY_COLABORATOR", "status": 400},
        )

    # update the project on redis
    listColaboratorsFrom_Project = project["colaborators"]
    listColaboratorsFrom_Project.append(
        {"id": idColaborator, "username": colaboratorToAdd["username"]}
    )
    project.update({"colaborators": listColaboratorsFrom_Project})

    alterProject(idProject, project)

    # update the user on redis
    projectsOfUser = colaboratorToAdd["projects"]
    projectsOfUser.append(idProject)
    colaboratorToAdd.update({"projects": projectsOfUser})

    alterUser(idColaborator, colaboratorToAdd)

    return {"status": "Colaborator Added"}


def removeColaboratorProject(obj, info, idProject, idColaborator):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])
    iAmTheBoss(project, id)

    colaboratorToRemove = json.loads(searchDataUser(idColaborator)[0])

    # check if the user is already colaborator
    if idColaborator not in [
        colaborator["id"] for colaborator in project["colaborators"]
    ]:
        raise GraphQLError(
            "This user is not colaborator in this project",
            extensions={"code": "USER_NOT_COLABORATOR", "status": 400},
        )

    # update the project on redis
    listColaboratorsFrom_Project = project["colaborators"]
    listColaboratorsFrom_Project.remove(
        {"id": idColaborator, "username": colaboratorToRemove["username"]}
    )
    project.update({"colaborators": listColaboratorsFrom_Project})

    alterProject(idProject, project)

    # update the user on redis
    projectsOfUser = colaboratorToRemove["projects"]
    projectsOfUser.remove(idProject)
    colaboratorToRemove.update({"projects": projectsOfUser})

    alterUser(idColaborator, colaboratorToRemove)

    return {"status": "Colaborator Removed"}


def addTasktoProject(obj, info, idProject, name, description, typeOfTask):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    # check if the user is already colaborator
    if id not in [colaborator["id"] for colaborator in project["colaborators"]]:
        raise GraphQLError(
            "This user is not colaborator in this project",
            extensions={"code": "USER_NOT_COLABORATOR", "status": 400},
        )

    if typeOfTask == "especial":
        iAmTheBoss(project, id)

    taskToAdd = {
        "id": uuid4().__str__(),
        "name": name,
        "description": description,
        "created": date.today().__str__(),
        "who_create": id,
        "status": "open",
        "type": typeOfTask,
        "assignee": "",
        "rating": 0,
    }

    # update the project on redis
    listTasksFrom_Project = project["tasks"]
    listTasksFrom_Project.append(taskToAdd)
    project.update({"tasks": listTasksFrom_Project})

    alterProject(idProject, project)

    return taskToAdd


def deleteTaskfromProject(obj, info, idProject, idTask):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    # check if the user is already colaborator
    if id not in [colaborator["id"] for colaborator in project["colaborators"]]:
        raise GraphQLError(
            "This user is not colaborator in this project",
            extensions={"code": "USER_NOT_COLABORATOR", "status": 400},
        )

    if idTask not in [task["id"] for task in project["tasks"]]:
        raise GraphQLError(
            "This task is not in this project",
            extensions={"code": "TASK_NOT_IN_PROJECT", "status": 400},
        )

    for task in project["tasks"]:
        if task["id"] == idTask:
            taskToDelete = task

    print("taskToDelete", taskToDelete)

    if taskToDelete["who_create"] != id:
        raise GraphQLError(
            "You don't have permission to change this task",
            extensions={"code": "UNAUTHORIZED", "status": 401},
        )

    # update the project on redis
    listTasksFrom_Project = project["tasks"]
    listTasksFrom_Project.remove(taskToDelete)
    project.update({"tasks": listTasksFrom_Project})

    alterProject(idProject, project)

    return {"status": "Task Deleted"}


def addAssigneeToTask(obj, info, idProject, idTask, idAssignee):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    # check if the user is already colaborator
    if id not in [colaborator["id"] for colaborator in project["colaborators"]]:
        raise GraphQLError(
            "This user is not colaborator in this project",
            extensions={"code": "USER_NOT_COLABORATOR", "status": 400},
        )

    if idAssignee not in [colaborator["id"] for colaborator in project["colaborators"]]:
        raise GraphQLError(
            "The assignee proposed is not colaborator in this project",
            extensions={"code": "USER_NOT_COLABORATOR", "status": 400},
        )

    if idTask not in [task["id"] for task in project["tasks"]]:
        raise GraphQLError(
            "This task is not in this project",
            extensions={"code": "TASK_NOT_IN_PROJECT", "status": 400},
        )

    for task in project["tasks"]:
        if task["id"] == idTask:
            taskToUpdate = task

    if taskToUpdate["assignee"] != "" and taskToUpdate["assignee"] is not None:
        raise GraphQLError(
            "This task is already assigned to someone",
            extensions={"code": "TASK_ALREADY_ASSIGNED", "status": 400},
        )

    taskToUpdate.update({"assignee": idAssignee})

    for task in project["tasks"]:
        if task["id"] == idTask:
            task = taskToUpdate

    # update the project on redis
    alterProject(idProject, project)

    return {"status": "Assignee Added"}
