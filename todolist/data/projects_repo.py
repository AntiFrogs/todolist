from todolist.core.Models.models import Project

class ProjectsRepo:
    """
    A class used to represent the projects in memory of the program

    Attributes:
        _project (dict[str , Projects]): protected attribure to store the projects in a dictionary with ids as the keys
    """
    
    def __init__(self):
        """
        Initializing a Project repo instance
        """
        self._projects: dict[str , Project] = {}
    
    def add(self , newProject: Project) -> Project:
        """
        Adding a new Project to the existing project repo

        Args:
            newProject (Project) : new Project to add 

        Returns:
            Project: the Project added gets returned 
        """
        self._projects[newProject.id] = newProject
        return newProject

    def get(self , projectId: str ) -> Project | None:
        """
        Getting a Project from the Project Repo

        Args:
            projectId (str): id of the project that we want to get

        Returns:
            Project: project with id projectId 
        """
        return self._projects.get(projectId)
    
    def delete(self , projectId) -> bool:
        """
        Deleting a Project from the Project Repo

        Args:
            projectId (str): id of the project that we want to delete
        
        Returns:
            bool: a boolean value indicating the success of the operation
        """
        return self._projects.pop(projectId , None) != None
    
    def put(self , newProject: Project ) -> Project:
        """
        Updating a Project from Project Repo

        Args:
            newProject (Project): new project to replace the existing one with the same id

        Raises:
            ValueError: if project is not already in the list
            
        Returns:
            Project: updated project
        """
        if newProject.id not in self._projects.keys():
            raise ValueError("Key not found")
        self._projects[newProject.id] = newProject
        return newProject
    
    def list(self) -> list[Project]:
        """
        Listing the Projects

        Returns:
            list[Projects]: list of all projects 
        """
        return list(self._projects.values())
    
    def length(self) -> int:
        """
        getting the number of total projects

        Returns:
            int: the number of projects
        """
        return len(self._projects)