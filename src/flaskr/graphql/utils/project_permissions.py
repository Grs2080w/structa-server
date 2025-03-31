from graphql import GraphQLError

# Centralized error definitions
ERRORS = {
    "UNAUTHORIZED": {
        "message": "You don't have permission to do this action",
        "extensions": {"code": "UNAUTHORIZED", "status": 401},
    },
}


def verify_iAmTheCreator(project, idUser):
    if project["who_create"]["id"] != idUser:
        raise GraphQLError(
            ERRORS["UNAUTHORIZED"]["message"],
            extensions=ERRORS["UNAUTHORIZED"]["extensions"],
        )
