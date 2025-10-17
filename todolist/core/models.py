from uuid import uuid4

class Project:
    id: str = uuid4()
    name: str
    desc: str

    def __init__(self , name: str , desc: str = ""):
        self.name = name
        self.desc = desc



class Task:
    id: str = uuid4()
    for_project: int
    name: str
    desc: str
    status: str = "todo"

    def __init__(self , for_project: int , name:str , desc:str = "", status:str = "todo"):
        self.name = name
        self.desc = desc
        self.status = status
        self.for_project = for_project
    