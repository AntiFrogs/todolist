from todolist.core.Models.models import Task

class TasksRepo:

    def __init__(self ):
        self._tasks: dict[str , Task] = {}
        self._project_tasks: dict[str , set[str]] = {}

    def add(self , newTask: Task) -> Task:
        self._tasks[newTask.id] = newTask

        if newTask.for_project not in self._project_tasks.keys():
            self._project_tasks[newTask.for_project] = set()
        self._project_tasks[newTask.for_project].add(newTask.id)
    
    def get(self , taskId : str) -> Task | None:
        return self._tasks[taskId]
    
    def put(self , newTask: Task) -> Task:
        if newTask.id not in self._tasks:
            raise ValueError("Key not found")
        self._tasks[newTask.id] = newTask
        return newTask

    def delete(self , taskId: str) -> bool:
        result = self._tasks.pop(taskId , None)
        if not result:
            return False
        
        if result.for_project in self._project_tasks:
            self._project_tasks[result.for_project].discard(taskId)
            if not self._project_tasks[result.for_project]:
                self._project_tasks.pop(result.for_project , None)
        
        return True
    
    def delete_project(self , projectId: str) -> bool:
        task_ids = self._project_tasks.pop(projectId , set())
        for task_id in task_ids:
            self._tasks.pop(task_id , None)

        return True
    
    def list_by_project(self , projectId: str) -> list[Task]:
        task_ids = self._project_tasks.get(projectId , set())
        return [self._tasks[task_id] for task_id in task_ids]




