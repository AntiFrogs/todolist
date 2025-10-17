from todolist.core.Models.models import Task
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.config.setting import Setting

class TaskService:

    def __init__(self, projects_repo: ProjectsRepo , tasks_repo: TasksRepo , setting: Setting):
        self.projects = projects_repo
        self.tasks = tasks_repo
        self.setting = setting
    
    def addTask(self , projectId: str , name:str , desc: str) -> Task:
        if not self.projects.get(projectId):
            raise ValueError("Project not found")

        newTask = Task(projectId , name , desc)
        self.tasks.add(newTask)
        return newTask

    def editTask(self , taskId: str , name: str | None = None , desc: str | None = None) -> Task:
        taskToEdit = self.tasks.get(taskId)

        if not taskToEdit:
            raise ValueError("Task not found")
        
        taskToEdit.edit(newName= name , newDesc= desc)
        return self.tasks.put(taskToEdit)
    
    def changeTaskStatus(self , taskId: str , newStatus: str) -> Task:
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