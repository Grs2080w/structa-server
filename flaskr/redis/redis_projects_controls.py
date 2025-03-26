import json

from graphql import GraphQLError
from redis.commands.json.path import Path
from redis.commands.search.query import Query

from flaskr.redis.redis_users_controls import searchDataUser
from flaskr.redis.schema.schemas import indexProjects as index
from flaskr.redis.schema.schemas import r


def alterProject(idProject: str, obj: dict[str, any]):
    r.json().set(f"project:{idProject}", Path.root_path(), json.dumps(obj))


def returnAllProjects():
    """
    Return all Project from Redis database.

    Returns:
        list: A list of dictionaries containing all Project data.
    """
    resFromQuery = index.search(Query("*"))
    project_list = [json.loads(doc.json) for doc in resFromQuery.docs]
    return project_list


# return all datas about a project or a specific data about a project
def searchProject(id, *args):
    """
    Search a Project by id and return all datas about this Project or a specific data about this Project.

    Args:
        id (str): The ID of the project to be searched.
        *args (str): Path to the specific data to be searched.

    Returns:
        tuple: A tuple with the project data and the status code.

    Raises:
        GraphQLError: If the Project with the specified ID is not found.
    """
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


def addNewProject(obj):
    """
    Add a new Project to the Redis database.

    Args:
        obj (dict): The project to be added, represented as a dict containing the project's
            id, name, password, first_login, avatar_url, project_closed_count,
            project_open_count, projects_aborted_count, and projects.

    Returns:
        None
    """
    r.json().set(f"project:{obj['id']}", Path.root_path(), json.dumps(obj))


def deleteExistentProject(id):
    """
    Delete an existing Project by ID.

    Args:
        id (str): The ID of the project to be deleted.

    Raises:
        GraphQLError: If the project with the specified ID is not found.
    """

    r.delete(f"project:{id}")



## Essa função precisa tá aq?
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
