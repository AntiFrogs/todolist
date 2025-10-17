from todolist.core.Models.models import Task
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.config.setting import Setting
from todolist.core.validation.validation import validateTextLength , validateStatus , validateTaskNumber , validateDeadline
from datetime import datetime

class TaskService:

    def __init__(self, projects_repo: ProjectsRepo , tasks_repo: TasksRepo , setting: Setting):
        self.projects = projects_repo
        self.tasks = tasks_repo
        self.setting = setting
    
    def addTask(self , projectId: str , name:str , desc: str = "" , status: str = "todo" , deadline: datetime | None = None ) -> Task:
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
        validateStatus(newStatus)

        taskToChange = self.tasks.get(taskId)
        
        if not taskToChange:
            raise ValueError("Task not found")
        
        taskToChange.changeStatus(newStatus)
        return self.tasks.put(taskToChange)
    
    def deleteTask(self , taskId: str) -> bool:
        return self.tasks.delete(taskId)
    
    def listTasks(self , projectId: str) -> list[Task]:
        if not self.projects.get(projectId):
            raise ValueError("Project not found")

        return self.tasks.list_by_project(projectId)