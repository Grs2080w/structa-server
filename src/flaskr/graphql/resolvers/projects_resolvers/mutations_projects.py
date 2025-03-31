import json
from datetime import date
from uuid import uuid4

from flaskr.graphql.auth.auth_token import auth
from flaskr.graphql.utils.project_permissions import verify_iAmTheCreator
from flaskr.graphql.utils.project_validations import (
    validate_project_description,
    validate_project_name,
    verify_userAlreadyColaborator,
)
from flaskr.redis.redis_projects_controls import (
    addNewProject,
    alterProject,
    deleteExistentProject,
    searchProject,
    updateHistoryProject,
    userAlreadyCreateProject,
)
from flaskr.redis.redis_users_controls import (
    addNotification,
    alterUser,
    alterUserwithAbortedProject,
    alterUserwithClosedProject,
    alterUserwithNewProject,
    searchDataUser,
)

"""
This module contains mutation resolvers for project-related operations in a GraphQL API.

Functions:
- createProject: Creates a new project and stores it in the Redis database.
- deleteProject: Deletes an existing project and removes all collaborators.
- addColaboratorProject: Adds a collaborator to a project.
- removeColaboratorProject: Removes a collaborator from a project.
- closeStatusProject: Closes a project by changing its status to "closed".

The functions rely on user authentication and various utility functions to validate inputs and update
the Redis database.
"""


def createProject(obj, info, nameProject, descriptionProject):
    idUser, usernameUser = auth(info).values()
    newProject = {
        "id": uuid4().__str__(),
        "name": nameProject,
        "description": descriptionProject,
        "created": date.today().__str__(),
        "who_create": {"id": idUser, "username": usernameUser},
        "status": "active",
        "tasks": [],
        "colaborators": [{"id": idUser, "username": usernameUser}],
    }

    validate_project_name(nameProject)
    validate_project_description(descriptionProject)

    # update the project on redis
    if userAlreadyCreateProject(idUser, nameProject):
        alterUserwithNewProject(idUser, newProject)
        addNewProject(newProject)

    # update the history of the project
    updateHistoryProject(
        newProject["id"],
        f"Project {newProject['name']} created by {usernameUser} in {newProject['created']}",
    )

    return json.loads(json.dumps(newProject))


def deleteProject(obj, info, idProject):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    verify_iAmTheCreator(project, id)

    for colaborator in project["colaborators"]:
        removeColaboratorProject(obj, info, idProject, colaborator["id"])

    # alter the status of the project in user boss
    alterUserwithAbortedProject(id)

    # delete the project on redis
    deleteExistentProject(idProject)

    # send notification to the colaborators
    addNotification(
        id,
        f"The project {project['name']} was deleted by {username}",
    )

    return {"status": "Project Deleted"}


def addColaboratorProject(obj, info, idProject, idColaborator):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    colaboratorToAdd = json.loads(searchDataUser(idColaborator)[0])

    verify_iAmTheCreator(project, id)
    verify_userAlreadyColaborator(idColaborator, project)

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

    # send notification to the colaborator
    addNotification(
        idColaborator, f"You were added to the project {project['name']} by {username}"
    )

    # update the history of the project
    updateHistoryProject(
        idProject,
        f"Colaborator {colaboratorToAdd['username']} added to project",
    )

    return {"status": "Colaborator Added"}


def removeColaboratorProject(obj, info, idProject, idColaborator):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])
    colaboratorToRemove = json.loads(searchDataUser(idColaborator)[0])

    verify_iAmTheCreator(project, id)

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

    # send notification to the colaborator
    addNotification(
        idColaborator,
        f"You were removed from the project {project['name']} by {username}",
    )

    # update the history of the project
    updateHistoryProject(
        idProject,
        f"Colaborator {colaboratorToRemove['username']} removed from project",
    )

    return {"status": "Colaborator Removed"}


def closeStatusProject(obj, info, idProject):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    verify_iAmTheCreator(project, id)

    project.update({"status": "closed"})

    # update the project on redis
    alterProject(idProject, project)

    # update the user on redis
    alterUserwithClosedProject(id)

    # update the history of the project
    updateHistoryProject(idProject, f"Project status changed to closed by {username}")

    return {"status": "Project Closed"}
