# models and schema redis

import json

import redis
from redis.commands.json.path import Path
from redis.commands.search.field import NumericField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from config.settings import config
from flaskr.redis.listProjects import list_projects
from flaskr.redis.listUsers import list_users

r = redis.Redis(
    host=config["REDIS_HOST"],
    port=config["REDIS_PORT"],
    decode_responses=True,
    username=config["REDIS_USERNAME"],
    password=config["REDIS_PASSWORD"],
)

try:
    r.flushall()
except Exception:
    pass


schemaUser = (
    TextField("id"),
    TextField("name"),
    TextField("password"),
    TextField("first_login"),
    NumericField("project_closed_count"),
    NumericField("project_open_count"),
    NumericField("projects_aborted_count"),
    TextField("avatar_url"),
    TextField("projects.id"),
    TextField("projects.name"),
    TextField("projects.description"),
    TextField("projects.created"),
    TextField("projects.status"),
    TextField("projects.tasks.id"),
    TextField("projects.tasks.name"),
    TextField("projects.tasks.description"),
    TextField("projects.tasks.created"),
    TextField("projects.tasks.who_create"),
    TextField("projects.tasks.status"),
    TextField("projects.tasks.type"),
    TextField("projects.colaborators.id"),
    TextField("projects.colaborators.name"),
    TextField("projects.colaborators.avatar"),
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
    TextField("colaborators.name"),
    TextField("colaborators.avatar"),
)

print("Populate the db for dev users")

index = r.ft("idx:user")
index.create_index(
    schemaUser,
    definition=IndexDefinition(prefix=["user:"], index_type=IndexType.JSON),
)

indexProjects = r.ft("idx:projects")
indexProjects.create_index(
    schemaProject,
    definition=IndexDefinition(prefix=["projects:"], index_type=IndexType.JSON),
)

# populate the db for dev
for user in list_users:
    r.json().set(f"user:{user['id']}", Path.root_path(), json.dumps(user))

for project in list_projects:
    r.json().set(f"projects:{project['id']}", Path.root_path(), json.dumps(project))
