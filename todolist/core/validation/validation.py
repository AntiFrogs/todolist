from datetime import datetime

STATUS_TAGS = ["todo" , "doing" , "done"]


def validateTextLength(text: str , max_word_length: int , context: str) -> None:
    """
    validating word length of a text

    Args:
        text (str) : string to be validated
        max_word_length (int) : maximum number of words allowed 
        context (str): context of the text. used for the logging
    
    Raises:
        ValueError: if the text is not valid

    Returns:
        None 
    """
    words = text.strip().split(" ")
    if len(words) > max_word_length:
        raise ValueError(f"{context} is too long (max {max_word_length} words allowed)")
    
def validateStatus(status: str) -> None:
    """
    validating status of a task

    Args:
        status (str) : status to be validated

    Raises:
        ValueError: if the status is not valid

    Returns:
        None 
    """
    if status not in STATUS_TAGS:
        raise ValueError("Invalid status , please use status from this list: " , STATUS_TAGS)
    
def validateProjectName(name: str , projects: list , excludeId: str | None = None ):
    """
    validating project names

    Args:
        name (str) : project name to be validated
        projects (list) : list of all the projects to check
        excludeId (str | None , optional ): the id of a excluded project. used to exlude a project from the validation. defaults to None
    
    Raises:
        ValueError: if the name is not unique

    Returns:
        None 
    """
    for p in projects:
        if excludeId:
            if p.name == name and p.id != excludeId:
                raise ValueError("Project name must be unique")
        else:    
            if p.name == name:
                raise ValueError("Project name must be unique")
            
def validateProjectNumber(currentProjectsNumber: int , max_project_number: int):
    """
    validating the number of projects 

    Args:
        currentProjectsNumber (int) : number of current projects available 
        max_project_number (int) : maximum number of projects allowed
    
    Raises:
        ValueError: if the maximum number of projects is reached

    Returns:
        None 
    """
    if currentProjectsNumber == max_project_number: 
        raise ValueError("Max number of projects reached")

def validateTaskNumber(currentTasksNumber: int , max_task_numer: int):
    """
    validating the number of tasks 

    Args:
        currentTasksNumber (int) : number of current tasks available 
        max_task_numer (int) : maximum number of tasks allowed
    
    Raises:
        ValueError: if the maximum number of tasks is reached

    Returns:
        None 
    """
    if currentTasksNumber == max_task_numer: 
        raise ValueError("Max number of tasks reached")

def validateDeadline(deadline: datetime) -> None:
    """
    validate deadline

    Args:
        deadline (datetime): deadline of the task
    
    Raises:
        ValueError: if the deadline has passed
    
    Returns:
        None
    """
    today = datetime.now()
    if deadline < today:
        raise ValueError("deadline can't be in the past!")