from uuid import uuid4

class Project:
    id: str = str(uuid4())
    name: str
    desc: str

    def __init__(self , name: str , desc: str = ""):
        self.name = name
        self.desc = desc

    def edit(self , newName: str = "" , newDesc = "") -> None:
        if newName.strip():
            self.name = newName
        if newDesc.strip():
            self.desc = newDesc

class Task:
    id: str = str(uuid4())
    for_project: int
    name: str
    desc: str
    status: str = "todo"

    def __init__(self , for_project: int , name:str , desc:str = "", status:str = "todo"):
        self.name = name
        self.desc = desc
        self.status = status
        self.for_project = for_project

    def edit(self , newName: str = "" , newDesc: str = "") -> None :
        if newName.strip():
            self.name = newName
        if newDesc.strip():
            self.desc = newDesc

    def changeStatus(self , newStatus: str) -> None:
        newStatus = newStatus.strip()
        if newStatus not in ["todo" , "doing" , "done"]:
            return
        
        self.status = newStatus