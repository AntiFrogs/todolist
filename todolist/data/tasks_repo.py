from todolist.core.Models.models import Task

class TasksRepo:
    """
    A class used to represent the tasks in memory of the program

    Attributes:
        _tasks (dict[str , Tasks]): protected attribure to store the tasks in a dictionary with ids as the keys
        _project_tasks (dict[str , set[str]]): protected attribure to store task ids of a project for every project with at least one task
    """

    def __init__(self ):
        """
        Initializing a Task repo instance
        """
        self._tasks: dict[str , Task] = {}
        self._project_tasks: dict[str , set[str]] = {}

    def add(self , newTask: Task) -> Task:
        """
        Adding a new Task to the existing task repo and to the task list of the related project

        Args:
            newTask (Task) : new Task to add 

        Returns:
            Task: the Task added gets returned 
        """
        self._tasks[newTask.id] = newTask

        if newTask.for_project not in self._project_tasks.keys():
            self._project_tasks[newTask.for_project] = set()
        self._project_tasks[newTask.for_project].add(newTask.id)
    
    def get(self , taskId : str) -> Task | None:
        """
        Getting a Taks from the Project Repo

        Args:
            taskId (str): id of the task that we want to get

        Returns:
            Task: project with id taskId 
        """
        return self._tasks[taskId]
    
    def put(self , newTask: Task) -> Task:
        """
        Updating a Task from Task Repo

        Args:
            newTask (Task): new task to replace the existing one with the same id

        Raises:
            ValueError: if task is not already in the list
            
        Returns:
            Task: updated task
        """
        if newTask.id not in self._tasks:
            raise ValueError("Key not found")
        self._tasks[newTask.id] = newTask
        return newTask

    def delete(self , taskId: str) -> bool:
        """
        Deleting a Task from the Task  Repo and the related project's tasl list 

        Args:
            taskId (str): id of the task that we want to delete

        Raises:
            ValueError: if the task is not found
        
        Returns:
            bool: a boolean value indicating the success of the operation
        """
        result = self._tasks.pop(taskId , None)
        if not result:
            raise ValueError("Task not found")
        
        if result.for_project in self._project_tasks:
            self._project_tasks[result.for_project].discard(taskId)
            if not self._project_tasks[result.for_project]:
                self._project_tasks.pop(result.for_project , None)
        
        return True
    
    def delete_project(self , projectId: str) -> bool:
        """
        Cascade delete of the tasks when the parent project is deleted

        Args:
            projectId (str) : id of the project deleted
        
        Returns:
            bool: A boolean indicating the success of the operation 
        """
        task_ids = self._project_tasks.pop(projectId , set())
        for task_id in task_ids:
            self._tasks.pop(task_id , None)

        return True
    
    def list_by_project(self , projectId: str) -> list[Task]:
        """
        Listing the tasks of a project

        Args:
            projectId (str): id of the project to show it's task children 

        Returns:
            list[Task]: list of all tasks of the the project with id = projectId 
        """
        task_ids = self._project_tasks.get(projectId , set())
        return [self._tasks[task_id] for task_id in task_ids]

    def length(self) -> int:
        """
        getting the number of total tasks

        Returns:
            int: the number of tasks
        """
        return len(self._tasks)


