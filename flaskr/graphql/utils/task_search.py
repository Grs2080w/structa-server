def searchTask(project: dict, idTask: str):
    for task in project["tasks"]:
        if task["id"] == idTask:
            return task
