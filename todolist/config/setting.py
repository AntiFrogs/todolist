from dotenv import load_dotenv
import os


class Setting:
    MAX_NUMBER_OF_PROJECTS: int
    MAX_NUMBER_OF_TASKS: int

    def __init__(self , max_p: int = 0 , max_t: int =  0 , max_nw: int = 0 , max_dw: int = 0):
        self.MAX_NUMBER_OF_PROJECTS = max_p
        self.MAX_NUMBER_OF_TASKS = max_t
        self.MAX_NAME_WORD_LENGTH = max_nw
        self.MAX_DESC_WORD_LENGTH = max_dw

    @classmethod
    def initializeSettings(cls):
        load_dotenv()
        return cls(
            max_p = int(os.getenv("MAX_NUMBER_OF_PROJECTS" , 5)) ,
            max_t = int(os.getenv("MAX_NUMBER_OF_TASKS" , 10 )) ,
            max_nw = int(os.getenv("MAX_NAME_WORD_LENGTH" , 30 )) ,
            max_dw = int(os.getenv("MAX_DESC_WORD_LENGTH" , 150 )) ,
        )

