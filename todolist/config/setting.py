from dotenv import load_dotenv
import os


class Setting:
    """
    A class used to represent the .env variables as the program setting

    Attributes:
        MAMAX_NUMBER_OF_PROJECTS (int): the maximum allowed number of projects
        MAX_NUMBER_OF_TASKS (int): the maximum allowed number of tasks
        MAX_NAME_WORD_LENGTH (int): the maximum word length of a name
        MAX_DESC_WORD_LENGTH (int): the maximum word length of a description
    """

    MAX_NUMBER_OF_PROJECTS: int
    MAX_NUMBER_OF_TASKS: int
    MAX_NAME_WORD_LENGTH: int
    MAX_DESC_WORD_LENGTH: int

    def __init__(self , max_p: int = 0 , max_t: int =  0 , max_nw: int = 0 , max_dw: int = 0):
        """
        Initialize a setting instance

        Args:
            max_p (int): the maximum allowed number of projects (defaults to zero)
            max_t (int): the maximum allowed number of tasks (defaults to zero)
            max_nw (int): the maximum word length of a name (defaults to zero)
            max_dw (int): the maximum word length of a description (defaults to zero)
        """
        self.MAX_NUMBER_OF_PROJECTS = max_p
        self.MAX_NUMBER_OF_TASKS = max_t
        self.MAX_NAME_WORD_LENGTH = max_nw
        self.MAX_DESC_WORD_LENGTH = max_dw

    @classmethod
    def initializeSettings(cls):
        """
        make a new class with initialized environment variables

        Args:
            cls ( Setting ): current class object
        """
        load_dotenv()
        return cls(
            max_p = int(os.getenv("MAX_NUMBER_OF_PROJECTS" , 5)) ,
            max_t = int(os.getenv("MAX_NUMBER_OF_TASKS" , 10 )) ,
            max_nw = int(os.getenv("MAX_NAME_WORD_LENGTH" , 30 )) ,
            max_dw = int(os.getenv("MAX_DESC_WORD_LENGTH" , 150 )) ,
        )

