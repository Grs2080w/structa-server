import json
from datetime import date
from uuid import uuid4

from flaskr.graphql.auth.auth_token import auth
from flaskr.graphql.utils.project_permissions import verify_iAmTheCreator
from flaskr.graphql.utils.project_validations import verify_userNotColaborator
from flaskr.graphql.utils.task_search import searchTask
from flaskr.graphql.utils.task_validations import (
    validate_task_description,
    validate_task_name,
    validate_task_rating,
    validate_task_tag,
    verify_task_justTheAssignee,
    verify_task_notInProject,
    verify_task_someoneAssigned,
    verify_task_userNotCreator,
)
from flaskr.redis.redis_projects_controls import (
    alterProject,
    searchProject,
    updateHistoryProject,
)
from flaskr.redis.redis_users_controls import (
    addNotification,
)

"""
This module contains mutation resolvers for tasks-related operations in a GraphQL API.

Functions:
- addTasktoProject: Adds a task to a project and stores it in the Redis database.
- deleteTaskfromProject: Deletes an existing task from a project.
- alterRatingTask: Changes the rating of a task.
- alterStatusTask: Changes the status of a task.
- addAssigneeToTask: Assigns a user to a task.
"""


def addTasktoProject(
    obj,
    info,
    idProject,
    name,
    description,
    typeOfTask="normal",
    tag="",
    priority="low",
):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    if typeOfTask == "especial":
        verify_iAmTheCreator(project, id)

    verify_userNotColaborator(id, project)
    validate_task_tag(tag)
    validate_task_name(name)
    validate_task_description(description)

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
        "tag": tag,
        "priority": priority,
        "completed_date": "",
    }

    # update the project on redis
    listTasksFrom_Project = project["tasks"]
    listTasksFrom_Project.append(taskToAdd)
    project.update({"tasks": listTasksFrom_Project})

    alterProject(idProject, project)

    # update the history of the project
    updateHistoryProject(
        idProject,
        f"Task {name} added to project by {username}",
    )

    return taskToAdd


def deleteTaskfromProject(obj, info, idProject, idTask):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    taskToDelete = searchTask(project, idTask)

    verify_userNotColaborator(id, project)
    verify_task_notInProject(idTask, project)
    verify_task_userNotCreator(id, taskToDelete)

    # update the project on redis
    listTasksFrom_Project = project["tasks"]
    listTasksFrom_Project.remove(taskToDelete)
    project.update({"tasks": listTasksFrom_Project})

    alterProject(idProject, project)

    # update the history of the project
    updateHistoryProject(
        idProject,
        f"Task {taskToDelete['name']} removed from project by {username}",
    )

    return {"status": "Task Deleted"}


def addAssigneeToTask(obj, info, idProject, idTask, idAssignee):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    taskToUpdate = searchTask(project, idTask)

    verify_userNotColaborator(id, project)
    verify_userNotColaborator(idAssignee, project)
    verify_task_notInProject(idTask, project)
    verify_task_someoneAssigned(taskToUpdate)

    taskToUpdate.update({"assignee": idAssignee})

    # update the project on redis
    alterProject(idProject, project)

    # send notification to the assignee
    addNotification(
        idAssignee,
        f"You were assigned to the task {taskToUpdate['name']} in the project {project['name']} by {username}",
    )

    # update the history of the project
    updateHistoryProject(
        idProject,
        f"Task {taskToUpdate['name']} assigned to {username}",
    )

    return {"status": "Assignee Added"}


def alterStatusTask(obj, info, idProject, idTask, status):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])

    taskToUpdate = searchTask(project, idTask)

    verify_userNotColaborator(id, project)
    verify_task_notInProject(idTask, project)
    verify_task_justTheAssignee(id, taskToUpdate)

    taskToUpdate.update({"status": status})

    if status == "done":
        # change rating to 100
        taskToUpdate.update({"rating": 100})

        # update closed_data
        if not taskToUpdate.get("completed_date"):
            taskToUpdate["completed_date"] = ""
        taskToUpdate.update({"completed_date": date.today().__str__()})

    # update the project on redis
    alterProject(idProject, project)

    # update the history of the project
    updateHistoryProject(
        idProject,
        f"Task {taskToUpdate['name']} status changed to {status} by {username}",
    )

    return {"status": "Status Changed"}


def alterRatingTask(obj, info, idProject: str, idTask: str, rating: int):
    id, username = auth(info).values()
    project = json.loads(searchProject(idProject)[0])
    taskToUpdate = searchTask(project, idTask)

    verify_userNotColaborator(id, project)
    verify_task_justTheAssignee(id, taskToUpdate)
    verify_task_notInProject(idTask, project)
    validate_task_rating(rating)

    taskToUpdate.update({"rating": rating})

    if rating == 100:
        taskToUpdate.update({"completed_date": date.today().__str__()})
        taskToUpdate.update({"status": "done"})

    # update the project on redis
    alterProject(idProject, project)

    # update the history of the project
    updateHistoryProject(
        idProject,
        f"Task {taskToUpdate['name']} rating changed to {rating} by {username}",
    )

    return {"status": "Rating Changed"}
