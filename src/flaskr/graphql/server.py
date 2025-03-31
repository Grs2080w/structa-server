# Ariadne Utils
from ariadne import (
    ObjectType,
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)

# Server
from ariadne.explorer import ExplorerGraphiQL
from flask import Blueprint, jsonify, request

# Mutations Projects
from flaskr.graphql.resolvers.projects_resolvers.mutations_projects import (
    addColaboratorProject,
    closeStatusProject,
    createProject,
    deleteProject,
    removeColaboratorProject,
)

# Queries Projects
from flaskr.graphql.resolvers.projects_resolvers.queries_projects import (
    getProjects_resolver,
    listProjects_resolver,
    projectsCount_resolver,
)

# Mutations Tasks
from flaskr.graphql.resolvers.tasks_resolvers.mutations_tasks import (
    addAssigneeToTask,
    addTasktoProject,
    alterRatingTask,
    alterStatusTask,
    deleteTaskfromProject,
)

# Mutations Users
from flaskr.graphql.resolvers.users_resolvers.mutations_user import (
    changeAvatarUrlUser,
    changeEmailUser,
    cleanNotificationsUser,
    createUser,
    deleteUser,
    turnOTPUser,
    userLogin,
    verifyOtp,
)

# Queries Users
from flaskr.graphql.resolvers.users_resolvers.queries_user import (
    getUser_resolver,
    listUsers_resolver,
    usersCount_resolver,
)

"""
This module contains the GraphQL server for the API

It defines the schema, the resolvers and the routes for the GraphQL API.

The API is defined in the `graphql` blueprint, and it has the following routes:

* `GET /graphql`: the GraphQL API
* `GET /graphql?query=<query>`: execute a GraphQL query and return the result
* `POST /graphql`: execute a GraphQL mutation and return the result

The API uses the `ariadne` library to define the schema and the resolvers.
The resolvers are defined in the `resolvers` folder.

The API uses the `flask` library to create the routes and the server.
"""

# blueprint
graphql_Blueprint = Blueprint("graphql", __name__, url_prefix="/graphql")


# types
query = ObjectType("Query")
mutation = ObjectType("Mutation")


# Queries Projects
query.set_field("projects", listProjects_resolver)
query.set_field("project", getProjects_resolver)
query.set_field("projectsCount", projectsCount_resolver)

# Queries Users
query.set_field("users", listUsers_resolver)
query.set_field("user", getUser_resolver)
query.set_field("userCount", usersCount_resolver)

# Mutations Users
mutation.set_field("createUser", createUser)
mutation.set_field("deleteUser", deleteUser)
mutation.set_field("login", userLogin)
mutation.set_field("clearNotifications", cleanNotificationsUser)
mutation.set_field("updateAvatar", changeAvatarUrlUser)
mutation.set_field("changeEmailUser", changeEmailUser)
mutation.set_field("turnOTPUser", turnOTPUser)
mutation.set_field("verifyOtp", verifyOtp)

# Mutations Projects
mutation.set_field("createProject", createProject)
mutation.set_field("deleteProject", deleteProject)
mutation.set_field("addCollaborator", addColaboratorProject)
mutation.set_field("removeCollaborator", removeColaboratorProject)
mutation.set_field("closeProject", closeStatusProject)

# Mutations Tasks
mutation.set_field("addTask", addTasktoProject)
mutation.set_field("deleteTask", deleteTaskfromProject)
mutation.set_field("assignTask", addAssigneeToTask)
mutation.set_field("updateTaskStatus", alterStatusTask)
mutation.set_field("updateTaskRating", alterRatingTask)


# schema
type_defs = load_schema_from_path("src/flaskr/graphql/schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)

explorer_html = ExplorerGraphiQL().html(None)


# routes
@graphql_Blueprint.route("/", methods=["GET"])
def graphql_playground():
    return explorer_html, 200


@graphql_Blueprint.route("/", methods=["POST"])
def graphql_server():
    # auth_header = request.headers.get("Authorization")

    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request, debug=True)

    status_code = 200 if success else 400
    return jsonify(result), status_code
