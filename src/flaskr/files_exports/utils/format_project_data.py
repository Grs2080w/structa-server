import datetime
from collections import Counter

"""
This module contains a function to format a project data in different ways

Functions:
    data_format: function to format a project data in different ways

The function `data_format` takes a project data and return a string with the
project data formatted in different ways.
"""


def data_format(project, type):
    tasks = project["tasks"]

    # progress project
    total_rating = sum(task["rating"] for task in tasks)
    num_tarefas = len(tasks)
    project_progress = total_rating / num_tarefas if num_tarefas > 0 else 0

    # number of tasks by status
    tasks_open = len([task for task in tasks if task["status"] == "open"])
    tasks_in_progress = len([task for task in tasks if task["status"] == "in progress"])
    tasks_done = len([task for task in tasks if task["status"] == "done"])

    # number of tasks by priority
    tasks_priority_low = len([task for task in tasks if task["priority"] == "low"])
    tasks_priority_medium = len(
        [task for task in tasks if task["priority"] == "medium"]
    )
    tasks_priority_high = len([task for task in tasks if task["priority"] == "high"])

    time_done = [
        (
            datetime.strptime(task["completed_date"], "%Y-%m-%d")
            - datetime.strptime(task["created"], "%Y-%m-%d")
        ).days
        for task in tasks
        if task["status"] == "done"
    ]

    # average time to done
    time_done = sum(time_done) / len(time_done) if len(time_done) > 0 else 0

    # tasks by assignee
    atribuicoes = [task["assignee"] for task in tasks]
    contador = Counter(atribuicoes)
    tasks_by_assignee = dict(contador)

    # colaborators in string
    colaborators = [colaborador["username"] for colaborador in project["colaborators"]]
    colaborators_str = "  ".join(colaborators)

    # format tasks assigned to markdown table
    def table_tasks_assignee(list):
        markdown = "| id | tasks assigned |\n"
        markdown += "|----|-------|\n"

        for key, value in list.items():
            markdown += f"| {key} | {value} |\n"

        return markdown

    # format colaborators in markdown table
    def table_project_colaborators(list):
        markdown = "| id | username |\n"
        markdown += "|----|-------|\n"

        # Adiciona cada item do dicionário à tabela
        for colaborator in list:
            markdown += f"| {colaborator['id']} | {colaborator['username']} |\n"

        return markdown

    default = [
        ["analitcs", "data"],
        ["project_name", project["name"]],
        ["project_description", project["description"]],
        ["project_created", project["created"]],
        ["project_created_by", project["who_create"]["username"]],
        ["project_status", project["status"]],
        ["project_progress", project_progress],
        ["tasks_total", num_tarefas],
        ["tasks_open", tasks_open],
        ["tasks_in_progress", tasks_in_progress],
        ["tasks_done", tasks_done],
        ["tasks_priority_low", tasks_priority_low],
        ["tasks_priority_medium", tasks_priority_medium],
        ["tasks_priority_high", tasks_priority_high],
        ["time_done", time_done],
        ["tasks_by_assignee", tasks_by_assignee],
        ["colaborators", colaborators_str],
        ["table_tasks_assignee", table_tasks_assignee(tasks_by_assignee)],
        [
            "table_project_colaborators",
            table_project_colaborators(project["colaborators"]),
        ],
    ]

    if type == "csv":
        return default[:-2]

    if type == "pdf":
        return default
