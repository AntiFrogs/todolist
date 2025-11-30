from typing import Callable

from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from todolist.db import get_session

from todolist.core.Models.models import Project


SessionFactory = Callable[[], Session]


class ProjectsRepo:
    """
    A class used to represent the projects in memory of the program

    Attributes:
        _project (dict[str , Projects]): protected attribure to store the projects in a dictionary with ids as the keys
    """
    
    def __init__(self , session_factory: SessionFactory = get_session ):
        """
        Initializing a Project repo instance
        """
        self._session_factory = session_factory
    
    def add(self , newProject: Project) -> Project:
        """
        Adding a new Project to the existing project repo

        Args:
            newProject (Project) : new Project to add 

        Returns:
            Project: the Project added gets returned 
        """

        with self._session_factory() as session:
            session.add(newProject)
            session.commit()
            session.refresh(newProject)
            return newProject

    def get(self , projectId: str ) -> Project | None:
        """
        Getting a Project from the Project Repo

        Args:
            projectId (str): id of the project that we want to get

        Returns:
            Project: project with id projectId 
        """
        with self._session_factory() as session:
            query = select(Project).where(Project.id == projectId)
            result = session.execute(query).scalar_one_or_none()
            return result

    def delete(self , projectId) -> bool:
        """
        Deleting a Project from the Project Repo

        Args:
            projectId (str): id of the project that we want to delete
        
        Returns:
            bool: a boolean value indicating the success of the operation
        """
        with self._session_factory() as session:
            query = delete(Project).where(Project.id == projectId)
            result = session.execute(query)
            session.commit()
            return result.rowcount > 0
    
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
        with self._session_factory() as session:
            merged = session.merge(newProject)
            session.commit()
            session.refresh(merged)
            return merged
    
    def list(self) -> list[Project]:
        """
        Listing the Projects

        Returns:
            list[Projects]: list of all projects 
        """
        with self._session_factory() as session:
            stmt = select(Project)
            result = session.execute(stmt).scalars().all()
            return result
    
    def length(self) -> int:
        """
        getting the number of total projects

        Returns:
            int: the number of projects
        """
        with self._session_factory() as session:
            stmt = select(func.count(Project.id))
            result = session.execute(stmt).scalar_one()
            return int(result or 0)