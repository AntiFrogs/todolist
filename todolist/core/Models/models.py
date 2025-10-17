from uuid import uuid4

class Project:
    id: str 
    name: str
    desc: str

    def __init__(self , name: str , desc: str = ""):
        self.id = str(uuid4())[:8]
        self.name = name
        self.desc = desc
    
    def __str__(self):
        return f"Project(id: {self.id[:8]} , name: {self.name}, description: {self.desc})"
    def __repr__(self):
        return f"Project(id: {self.id[:8]} , name: {self.name}, description: {self.desc})"

    def edit(self , * , newName: str | None = None , newDesc: str | None = None) -> None:
        if newName:
            self.name = newName
        if newDesc:
            self.desc = newDesc

class Task:
    id: str
    for_project: int
    name: str
    desc: str
    status: str = "todo"

    def __init__(self , for_project: int , name:str , desc:str = "", status:str = "todo"):
        self.id = str(uuid4())[:8]
        self.name = name
        self.desc = desc
        self.status = status
        self.for_project = for_project
    
    def __str__(self):
         return f"Task(id: {self.id[:8]},name: {self.name}, description: {self.desc},status: {self.status}, for project: {self.for_project[:8]})"
    def __repr__ (self):
         return f"Task(id: {self.id[:8]},name: {self.name}, description: {self.desc},status: {self.status}, for project: {self.for_project[:8]})"

    def edit(self , * , newName: str | None = None , newDesc: str | None = None) -> None :
        if newName:
            self.name = newName
        if newDesc:
            self.desc = newDesc

    def changeStatus(self , newStatus: str) -> None:
        newStatus = newStatus.strip()
        if newStatus not in ["todo" , "doing" , "done"]:
            return
        
        self.status = newStatus