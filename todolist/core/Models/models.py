from __future__ import annotations

from uuid import uuid4
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from todolist.db import Base

from typing import Optional , List

class Project(Base):
    """
    A class used to represent a project instance

    Attributes:
        id (str): unique universal id made with uuid4 (only the first 8 characters)
        name (str): unique title of the project 
        desc (str): the description of the project  
    
    """

    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(8) , primary_key=True)
    name: Mapped[str] = mapped_column(String(100) , unique=True, nullable=False,)
    desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    tasks: Mapped[List[Task]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # constructor 
    def __init__(self , name: str , desc: str = ""):
        """
        initializing a Project instance

        Args:
            name (str) : title to initialize the project with
            desc (str , optional) : description to initialize the project with. defaults to ""
         
        """
        self.id = str(uuid4())[:8]
        self.name = name
        self.desc = desc
    
    # Methods to control the representation of the class object
    def __str__(self):
        return f"Project(id: {self.id[:8]} , name: {self.name}, description: {self.desc})"
    def __repr__(self):
        return f"Project(id: {self.id[:8]} , name: {self.name}, description: {self.desc})"

    def edit(self , * , newName: str | None = None , newDesc: str | None = None) -> None:
        """
        Updating project attributes

        Args:
            newName (str | None) : new title to give the Project. defaults to None
            newDesc (str | None) : new description to give the Project. defaults to None

        Returns:
            None 
        """
        if newName:
            self.name = newName
        if newDesc:
            self.desc = newDesc

class Task(Base):
    """
    A class used to represent a task instance

    Attributes:
        id (str): unique universal id made with uuid4 (only the first 8 characters)
        name (str): A title of the task 
        desc (str): The description of the task  
        status ({todo , doing , done}): The status of the task. defaults to todo  
        deadline (datetime | None): The deadline of the task. if not specified , defaults to None    
    
    """
    __tablename__ = "tasks"


    id:Mapped[str] = mapped_column(String(8), primary_key=True)

    for_project: Mapped[str] = mapped_column( String(8), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    name: Mapped[str] = mapped_column( String(100), nullable=False )
    
    desc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    status: Mapped[str] = mapped_column(String(16), default="todo", nullable=False )
    
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True )

    project: Mapped["Project"] = relationship(
        back_populates="tasks",
        primaryjoin="Task.for_project == Project.id",
    )

    # constructor 
    def __init__(self , for_project: str , name:str , desc:str = "", status:str = "todo" , deadline: datetime | None = None):
        """
        initializing a Task instance

        Args:
            for_project (str) : in which project the task resides. given by id of the project 
            name (str) : title to initialize the task with 
            desc (str , optional) : description to initialize the task with. defaults to ""
            status ({todo , doing , done} , optional) : status to initialize the task with. defaults to todo
            deadline (datetime | None) : initial deadline of the task. defaults to None
        """
        self.id = str(uuid4())[:8]
        self.name = name
        self.desc = desc
        self.status = status
        self.for_project = for_project
        self.deadline = deadline
    
    # Methods to control the representation of the class object
    def __str__(self):
         return f"Task(id: {self.id[:8]},name: {self.name}, description: {self.desc},status: {self.status}, for project: {self.for_project[:8]})"
    def __repr__ (self):
         return f"Task(id: {self.id[:8]},name: {self.name}, description: {self.desc},status: {self.status}, for project: {self.for_project[:8]})"

    def edit(self , * , newName: str | None = None , newDesc: str | None = None , newStatus: str | None = None , newDeadline: datetime | None = None) -> None :
        """
        Updating task attributes

        Args:
            newName (str | None) : new title to give the Task. defaults to None
            newDesc (str | None) : new description to give the Task. defaults to None
            newStatus (str | None) : new status to give the Task. defaults to None
            newDeadline (datetime | None ): new Deadline to give the Task. defaults to None

        Returns:
            None 
        """
        
        if newName:
            self.name = newName
        if newDesc:
            self.desc = newDesc
        if newStatus:
            self.status = newStatus
        if newDeadline:
            self.deadline = newDeadline

    def changeStatus(self , newStatus: str) -> None:
        """
        changing task status

        Args: 
            newStatus (str) : new status to give the task

        Returns:
            None  
        """
        newStatus = newStatus.strip()
        if newStatus not in ["todo" , "doing" , "done"]:
            return
        
        self.status = newStatus