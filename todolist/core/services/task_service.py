from todolist.core.Models.models import Task
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.config.setting import Setting
from todolist.core.validation.validation import validateTextLength , validateStatus , validateTaskNumber , validateDeadline
from datetime import datetime , timezone

class TaskService:
    """
    A class used to represent the services provided for taks

    Attributes:
        projects (ProjectRepo): a project repository to work with 
        tasks (TaskRepo): a task repository to work with 
        setting (Setting): rules and constraints for the service
    """
    def __init__(self, projects_repo: ProjectsRepo , tasks_repo: TasksRepo , setting: Setting):
        """
        Initializing a project service

        Args:
            projects_repo (ProjectsRepo) : Project repository to work with
            tasks_repo (TasksRepo) : Task repository to work with
        """
        
        self.projects = projects_repo
        self.tasks = tasks_repo
        self.setting = setting
    
    def addTask(self , projectId: str , name:str , desc: str = "" , status: str = "todo" , deadline: datetime | None = None ) -> Task:
        """
        Adding a task to a project
        
        Args:
            projectId (str): id of the project to add the task to
            name (str) : name of the task set to be added
            desc (str, optional) : description of the task set to be added. defaults to ""
            status ({todo , doing , done}, optional) : status of the task set to be added. defaults to todo
            deadline (datetime | None, optional): deadline of the task set to be added. defaults to None
        
        Raises:
            ValueError: if project is not found

        Returns:
            Task: added task
        """
        
        validateTextLength(name , self.setting.MAX_NAME_WORD_LENGTH , "Task name")
        validateTextLength(desc , self.setting.MAX_DESC_WORD_LENGTH , "Task desc")
        validateTaskNumber(self.tasks.length() , self.setting.MAX_NUMBER_OF_TASKS)
        validateStatus(status)

        if deadline:
            validateDeadline(deadline)

        if not self.projects.get(projectId):
            raise ValueError("Project not found")

        newTask = Task(projectId , name , desc , status , deadline)
        self.tasks.add(newTask)
        return newTask

    def editTask(self , taskId: str , name: str | None = None , desc: str | None = None , status: str | None = None  , deadline: datetime | None = None) -> Task:
        """
        Updating a task 

        Args:
            taskId (str): id of the task set to be updated
            name (str | None, optional) : name of the task set to be updated. defaults to None
            desc (str | None, optional) : description of the task set to be updated. defaults to None
            status ({todo , doing , done} | None , optional) : status of the task set to be updated. defaults to None
            deadline (datetime | None, optional): deadline of the task set to be updated. defaults to None
        
        Raises:
            ValueError: if task is not found

        Returns:
            Task: updated task
        """
        if name:
            validateTextLength(name , self.setting.MAX_NAME_WORD_LENGTH , "Task name")
        if desc:
            validateTextLength(desc , self.setting.MAX_DESC_WORD_LENGTH , "Task desc")
        if status:
            validateStatus(status)
        if deadline:
            validateDeadline(deadline)

        taskToEdit = self.tasks.get(taskId)

        if not taskToEdit:
            raise ValueError("Task not found")
        
        taskToEdit.edit(newName= name , newDesc= desc , newStatus=status , newDeadline= deadline)
        return self.tasks.put(taskToEdit)
    
    def changeTaskStatus(self , taskId: str , newStatus: str) -> Task:
        """
        Changing the status of a task 

        Args:
            taskId (str): id of the task set to have it's status changed
            newStatus ({todo , doing , done}): new status for the task

        Raises:
            ValueError: if task is not found

        Returns:
            Task: updated task
        """
        validateStatus(newStatus)

        taskToChange = self.tasks.get(taskId)
        
        if not taskToChange:
            raise ValueError("Task not found")
        
        taskToChange.changeStatus(newStatus)
        return self.tasks.put(taskToChange)
    
    def deleteTask(self , taskId: str) -> bool:
        """
        Deleting a task

        Args:
            taskId (str): id of the task set to get deleted
        
        Returns:
            bool: A boolean indicating the success of the operation 
        """
        return self.tasks.delete(taskId)
    
    def listTasks(self , projectId: str) -> list[Task]:
        """
        Listing all the tasks of a project

        Args:
            projentId (str) : id of the project to list it's tasks
        
        Returns:
            list[Task]: list of the tasks of project with id == projectId   
        """
        if not self.projects.get(projectId):
            raise ValueError("Project not found")

        return self.tasks.list_by_project(projectId)
    
    def autoCloseOverdueTasks(self) -> int:
        """
        Automatically close all overdue tasks.

        A task is considered overdue if:
          + it has a deadline
          + its deadline is before 'now'
          + its status is not 'done'

        Returns:
            int: number of tasks that were updated
        """
        now = datetime.now(timezone.utc)
        return self.tasks.close_overdue(now)
    
    def getTask(self, taskId: str) -> Task:
        """
        Get a single task by its id.

        Args:
            taskId (str): id of the task we want

        Raises:
            ValueError: if task is not found

        Returns:
            Task: the found task
        """
        task = self.tasks.get(taskId)
        if not task:
            raise ValueError("Task not found")
        return task
