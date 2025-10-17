
STATUS_TAGS = ["todo" , "doing" , "done"]


def validateTextLength(text: str , max_word_length: int , context: str) -> None:
    words = text.strip().split(" ")
    if len(words) > max_word_length:
        raise ValueError(f"{context} is too long (max {max_word_length} words allowed)")
    
def validateStatus(status: str) -> None:
    if status not in STATUS_TAGS:
        raise ValueError("Invalid status , please use status from this list: " , STATUS_TAGS)
    
def validateProjectName(name: str , projects: list , excludeId: str | None = None ):
    for p in projects:
        if excludeId:
            if p.name == name and p.id != excludeId:
                raise ValueError("Project name must be unique")
        else:    
            if p.name == name:
                raise ValueError("Project name must be unique")
            
def validateProjectNumber(currentProjectsNumber: int , max_project_number: int):
    if currentProjectsNumber == max_project_number: 
        raise ValueError("Max number of projects reached")

def validateTaskNumber(currentTasksNumber: int , max_task_numer: int):
    if currentTasksNumber == max_task_numer: 
        raise ValueError("Max number of tasks reached")