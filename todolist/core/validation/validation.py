
STATUS_TAGS = ["todo" , "doing" , "done"]


def validateTextLength(word: str , max_word_length: int) -> None:
    if len(word) > max_word_length:
        raise ValueError(f"Text is too long")
    
def validateStatus(status: str) -> None:
    if status not in STATUS_TAGS:
        raise ValueError("Invalid status")
    
def validateProjectName(name: str , projects: list):
    for p in projects:
        if p.name == name:
            raise ValueError("Project name must be unique")