# models and schema redis

import redis
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from config.settings import config

r = redis.Redis(
    host=config["REDIS_HOST"],
    port=config["REDIS_PORT"],
    decode_responses=True,
    username=config["REDIS_USERNAME"],
    password=config["REDIS_PASSWORD"],
)


schemaUser = (
    TextField("id"),
    TextField("name"),
    TextField("username"),
    TextField("password"),
    TextField("first_login"),
    NumericField("project_closed_count"),
    NumericField("project_open_count"),
    NumericField("projects_aborted_count"),
    TextField("avatar_url"),
    TextField("projects"),
    TextField("notifications"),
    TextField("otp"),
    TextField("email"),
    TextField("codeOTP"),
)

schemaProject = (
    TextField("id"),
    TextField("name"),
    TextField("description"),
    TextField("created"),
    TextField("status"),
    TextField("tasks.id"),
    TextField("tasks.name"),
    TextField("tasks.description"),
    TextField("tasks.created"),
    TextField("tasks.who_create"),
    TextField("tasks.status"),
    TextField("tasks.type"),
    TextField("colaborators.id"),
    TextField("colaborators.username"),
    TextField("colaborators.avatar"),
    TextField("history"),
)


def cleanRedis(param=False):
    if param:
        print("clean redis")
        r.flushall()
        index = r.ft("idx:users")
        index.create_index(
            schemaUser,
            definition=IndexDefinition(prefix=["user:"], index_type=IndexType.JSON),
        )
        indexProjects = r.ft("idx:projects")
        indexProjects.create_index(
            schemaProject,
            definition=IndexDefinition(prefix=["project:"], index_type=IndexType.JSON),
        )


cleanRedis(False)


index = r.ft("idx:users")
indexProjects = r.ft("idx:projects")
