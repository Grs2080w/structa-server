# Here are all functions that interact directly with redis db

import json

from graphql import GraphQLError
from redis.commands.json.path import Path
from redis.commands.search.query import Query

from flaskr.redis.db_schemas import index, r


def returnAllUsers():
    """
    Return all users from Redis database.

    Returns:
        list: A list of dictionaries containing all user data.
    """
    resFromQuery = index.search(Query("*"))
    user_list = [json.loads(doc.json) for doc in resFromQuery.docs]
    return user_list


# return all datas about a user or a specific data about a user
def searchDataUser(id, *args):
    """
    Search a user by id and return all datas about this user or a specific data about this user.

    Args:
        id (str): The ID of the user to be searched.
        *args (str): Path to the specific data to be searched.

    Returns:
        tuple: A tuple with the user data and the status code.

    Raises:
        GraphQLError: If the user with the specified ID is not found.
    """
    try:
        resFromQuery = r.json().get(f"user:{id}", *args)
        if not resFromQuery:
            raise TypeError()
        return resFromQuery, 200

    except TypeError:
        print("Argumentos inválidos para .get(). Verifique *args.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    raise GraphQLError(
        f"User with id: {id} not found",
        extensions={"code": "USER_NOT_FOUND", "status": 404},
    )


def addNewUser(obj):
    """
    Add a new user to the Redis database.

    Args:
        obj (dict): The user to be added, represented as a dict containing the user's
            id, name, password, first_login, avatar_url, project_closed_count,
            project_open_count, projects_aborted_count, and projects.

    Returns:
        None
    """
    r.json().set(f"user:{obj['id']}", Path.root_path(), json.dumps(obj))


def deleteExistentUser(id):
    """
    Delete an existing user by ID.

    Args:
        id (str): The ID of the user to be deleted.

    Raises:
        GraphQLError: If the user with the specified ID is not found.
    """

    r.delete(f"user:{id}")


def findUserByParam(param, value):
    """
    Find user by param

    Args:
        param (str): key to be searched
        value (str): value to be matched with key

    Returns:
        boolean: True if someone user is found
    """
    res = index.search("*").docs
    for doc in res:
        user = json.loads(doc.json)

        if user[param] == value:
            return True


def loginUser(name, password):
    """
    Search a user by name and password

    Args:
        name (str): name of user
        password (str): password of user

    Returns:
        json: a json with user id and name

    Raises:
        GraphQLError: if user not found
    """
    res = index.search("*").docs
    for doc in res:
        user = json.loads(doc.json)

        if user["name"] == name and user["password"] == password:
            return json.dumps({"id": user["id"], "name": user["name"]})

    raise GraphQLError(
        "User or password incorrect",
        extensions={"code": "USER_NOT_FOUND", "status": 404},
    )
