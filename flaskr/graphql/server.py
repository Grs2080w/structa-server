from ariadne import (
    ObjectType,
    graphql_sync,
    load_schema_from_path,
    make_executable_schema,
    snake_case_fallback_resolvers,
)
from ariadne.explorer import ExplorerGraphiQL
from flask import Blueprint, jsonify, request

from flaskr.graphql.resolvers.mutations_projects import (
    addAssigneeToTask,
    addColaboratorProject,
    addTasktoProject,
    createProject,
    deleteProject,
    deleteTaskfromProject,
    removeColaboratorProject,
)
from flaskr.graphql.resolvers.mutations_user import createUser, deleteUser, userLogin
from flaskr.graphql.resolvers.queries_projects import (
    getProjects_resolver,
    listProjects_resolver,
    projectsCount_resolver,
)
from flaskr.graphql.resolvers.queries_user import (
    getUser_resolver,
    listUsers_resolver,
    usersCount_resolver,
)

# blueprint
graphql_Blueprint = Blueprint("graphql", __name__, url_prefix="/graphql")


# types
query = ObjectType("Query")
mutation = ObjectType("Mutation")


# queries
query.set_field("listUsers", listUsers_resolver)
query.set_field("getUser", getUser_resolver)
query.set_field("usersCount", usersCount_resolver)

query.set_field("listProjects", listProjects_resolver)
query.set_field("getProject", getProjects_resolver)
query.set_field("projectCount", projectsCount_resolver)


# mutations
mutation.set_field("createUser", createUser)
mutation.set_field("deleteUser", deleteUser)
mutation.set_field("userLogin", userLogin)

mutation.set_field("createProject", createProject)
mutation.set_field("deleteProject", deleteProject)
mutation.set_field("addColaboratorToProject", addColaboratorProject)
mutation.set_field("removeColaboratorToProject", removeColaboratorProject)
mutation.set_field("addTaskToProject", addTasktoProject)
mutation.set_field("deleteTaskToProject", deleteTaskfromProject)
mutation.set_field("addAssigneeToTask", addAssigneeToTask)


# schema
type_defs = load_schema_from_path("flaskr/graphql/schema.graphql")
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
