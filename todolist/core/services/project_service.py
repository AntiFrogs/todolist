from todolist.core.Models.models import Project
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.config.setting import Setting


class ProjectService:
    
    def __init__(self , projects_repo: ProjectsRepo , tasks_repo: TasksRepo , setting: Setting):
        self.projects = projects_repo
        self.tasks = tasks_repo
        self.setting = setting
    
    def createProject(self , name: str , desc: str = "") -> Project:
        newProject = Project(name , desc)
        self.projects.add(newProject)
        return newProject
    
    def editProject(self , projectId:str , newName: str | None = None , newDesc: str | None = None ) -> Project:
        projectToEdit = self.projects.get(projectId)

        if not projectToEdit:
            raise ValueError("Project not found")

        projectToEdit.edit(newName=newName , newDesc=newDesc)
        return self.projects.put(projectToEdit)
    
    def deleteProject(self , projectId: str) -> bool:
        projectToRemove = self.projects.get(projectId)

        if not projectToRemove: 
            raise ValueError("Project not found")
        
        result = self.projects.delete(projectId)
        if result:
            self.tasks.delete_project(projectId)
        
        return result
    
    def list(self) -> list[Project]:
        return self.projects.list()
    