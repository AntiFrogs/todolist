from todolist.core.models import Project

class ProjectsRepo:
    
    def __init__(self):
        self._projects: dict[str , Project] = {}
    
    def add(self , newProject: Project) -> Project:
        self._projects[newProject.id] = newProject
        return newProject

    def get(self , projectId: str ) -> Project | None: 
        return self._projects.get(projectId)
    
    def delete(self , projectId) -> bool:
        return self._projects.pop(projectId , None) != None
    
    def put(self , newProject: Project ) -> Project:
        if newProject.id not in self._projects.keys():
            raise ValueError("Key not found")
        self._projects[newProject.id] = newProject
        return newProject
    
    def list(self) -> list[Project]:
        return list(self._projects.values())