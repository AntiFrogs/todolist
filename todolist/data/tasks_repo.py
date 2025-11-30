from typing import Callable

from sqlalchemy import select, delete, func
from sqlalchemy.orm import Session

from todolist.db import get_session
from todolist.core.Models.models import Task

SessionFactory = Callable[[], Session]

class TasksRepo:
    """
    A class used to represent the tasks in memory of the program

    Attributes:
        _tasks (dict[str , Tasks]): protected attribure to store the tasks in a dictionary with ids as the keys
        _project_tasks (dict[str , set[str]]): protected attribure to store task ids of a project for every project with at least one task
    """

    def __init__(self , session_factory: SessionFactory = get_session):
        """
        Initializing a Task repo instance
        """
        self._session_factory = session_factory

    def add(self , newTask: Task) -> Task:
        """
        Adding a new Task to the existing task repo and to the task list of the related project

        Args:
            newTask (Task) : new Task to add 

        Returns:
            Task: the Task added gets returned 
        """
        with self._session_factory() as session:
            session.add(newTask)
            session.commit()
            session.refresh(newTask)
            return newTask
        
    
    def get(self , taskId : str) -> Task | None:
        """
        Getting a Taks from the Project Repo

        Args:
            taskId (str): id of the task that we want to get

        Returns:
            Task: project with id taskId 
        """
        with self._session_factory() as session:
            stmt = select(Task).where(Task.id == taskId)
            result = session.execute(stmt).scalar_one_or_none()
            return result
    
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
        with self._session_factory() as session:
            merged = session.merge(newTask)
            session.commit()
            session.refresh(merged)
            return merged

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
        with self._session_factory() as session:
            stmt = delete(Task).where(Task.id == taskId)
            result = session.execute(stmt)
            session.commit()
            return result.rowcount > 0
    
    def delete_project(self , projectId: str) -> bool:
        """
        Cascade delete of the tasks when the parent project is deleted

        Args:
            projectId (str) : id of the project deleted
        
        Returns:
            bool: A boolean indicating the success of the operation 
        """
        with self._session_factory() as session:
            stmt = delete(Task).where(Task.for_project == projectId)
            session.execute(stmt)
            session.commit()
    
    def list_by_project(self , projectId: str) -> list[Task]:
        """
        Listing the tasks of a project

        Args:
            projectId (str): id of the project to show it's task children 

        Returns:
            list[Task]: list of all tasks of the the project with id = projectId 
        """
        with self._session_factory() as session:
            stmt = select(Task).where(Task.for_project == projectId)
            result = session.execute(stmt).scalars().all()
            return result

    def length(self) -> int:
        """
        getting the number of total tasks

        Returns:
            int: the number of tasks
        """
        with self._session_factory() as session:
            stmt = select(func.count(Task.id))
            result = session.execute(stmt).scalar_one()
            return int(result or 0)


