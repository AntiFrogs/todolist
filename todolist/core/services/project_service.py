from todolist.core.Models.models import Project
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.config.setting import Setting
from todolist.core.validation.validation import validateTextLength , validateProjectName , validateProjectNumber


class ProjectService:
    """
    A class used to represent the services provided for projects

    Attributes:
        projects (ProjectRepo): a project repository to work with 
        tasks (TaskRepo): a task repository to work with 
        setting (Setting): rules and constraints for the service
    """
    
    def __init__(self , projects_repo: ProjectsRepo , tasks_repo: TasksRepo , setting: Setting):
        """
        Initializing a project service

        Args:
            projects_repo (ProjectsRepo) : Project repository to work with
            tasks_repo (TasksRepo) : Task repository to work with
        """
        self.projects = projects_repo
        self.tasks = tasks_repo
        self.setting = setting
    
    def createProject(self , name: str , desc: str = "") -> Project:
        """
        Creating a project

        Args:
            name (str): title to be given to the newly made project
            desc (str , optional): description to be given to the newly made project. defaults to ""
        
        Returns:
            Project: created project  

        """
        validateTextLength(name , self.setting.MAX_NAME_WORD_LENGTH , "Project name")
        validateTextLength(desc , self.setting.MAX_DESC_WORD_LENGTH , "Project description")
        validateProjectName(name , self.projects.list()) 
        validateProjectNumber(self.projects.length() , self.setting.MAX_NUMBER_OF_PROJECTS)

        newProject = Project(name , desc)
        self.projects.add(newProject)
        return newProject
    
    def editProject(self , projectId:str , newName: str | None = None , newDesc: str | None = None ) -> Project:
        """
        Updating a project
    
        Args:
            projectId (str) : id of the project we want to have changes upon
            newName (str | None , optional): new title to be given to the project. defaults to None
            newDesc (str | None , optional): new description to be given to the project. defaults to None
        
        Raises:
            ValueError: if project is not found
        
        Returns:
            Project: updated project 
        """
        if newName:
            validateTextLength(newName , self.setting.MAX_NAME_WORD_LENGTH , "Project name")
            validateProjectName(newName , self.projects.list() , projectId) 
        if newDesc:
            validateTextLength(newDesc , self.setting.MAX_DESC_WORD_LENGTH , "Project description")

        projectToEdit = self.projects.get(projectId)

        if not projectToEdit:
            raise ValueError("Project not found")

        projectToEdit.edit(newName=newName , newDesc=newDesc)
        return self.projects.put(projectToEdit)
    
    def deleteProject(self , projectId: str) -> bool:
        """
        Deleting a project

        Args:
            projectId (str): id of the project to be deleted
        
        Raises:
            ValueError: if project is not found
            
        Returns:
            bool: A bollean indicating the success of the operation 
        """
        projectToRemove = self.projects.get(projectId)

        if not projectToRemove: 
            raise ValueError("Project not found")
        
        result = self.projects.delete(projectId)
        if result:
            self.tasks.delete_project(projectId)
        
        return result
    
    def list(self) -> list[Project]:
        """
        Listing the projects

        Returns:
            list[Projects] : list of the projects 
        """
        return self.projects.list()
    
    def getProject(self, projectId: str) -> Project:
        """
        Get a single project by its id.

        Args:
            projectId (str): id of the project we want

        Raises:
            ValueError: if project is not found

        Returns:
            Project: the found project
        """
        project = self.projects.get(projectId)
        if not project:
            raise ValueError("Project not found")
        return project

    