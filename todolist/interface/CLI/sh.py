from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService
import os 
from datetime import datetime
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from colorama import init , Style , Fore
init(autoreset=True)

HISTORY_PATH = os.path.expanduser("~/.todolist_cli_history")


HELP = """
Commands:
  help
  exit
  clear
  project create <name> | <description>
  project list
  project delete <project_id>
  project edit <project_id> | [name or ""] | [description or ""]
  task add <project_id> | <title> | <description> | <todo|doing|done> | <deadline(yyyy-mm-dd)>
  task list <project_id>
  task status <task_id> | <todo|doing|done>
  task edit <task_id> | <title> | <description> | <todo|doing|done> | <deadline(yyyy-mm-dd)>
  task delete <task_id>
"""

def _split_pipe(s: str) -> list[str]:
    """
    splitting a string seprated with | ro an array of parameter

    Args:
        s (str): string to work on

    Returns:
        None 
    """
    parameters = [part.strip() for part in s.split("|")]
    
    for index , p in enumerate(parameters):
        if p.startswith("\"") and p.endswith("\""):
            parameters[index] = p[1:-1].strip()

    return parameters

def _parseDeadline(s: str) -> datetime | None | str:
    """
    Parsing deadline in yyyy-mm-dd format

    Args:
        s (str): string to parse
    
    Returns:
        datetime | None | str: depending on the input string 
    """
    if s == "":
        return None
    try : 
        return datetime.strptime    (s , "%Y-%m-%d")
    except ValueError:
        raise ValueError("Deadline must be in format yyyy-mm-dd (e.g. 2025-12-31)")



class CLI:
    """
    A class to represent cli 

    Attributes: 
        projects (ProjectService) : service to provide to projects
        tasks (TaskService) : service to provide to tasks
        session (PromptSession): interactive command line 
    """

    def __init__(self, project_service: ProjectService, task_service: TaskService) -> None:
        """
        Initializing a ClI instance

        Args:
            project_service (ProjectService) : service to provide to projects
            task_service (TaskService) : service to provide to tasks

        Returns:
            None
        """
        self.projects = project_service
        self.tasks = task_service
        self.session = PromptSession(history=FileHistory(HISTORY_PATH))

    def run(self) -> None:
        """Running the command line interface"""

        print( Fore.GREEN + "Cli todolist app. type help for command list. exit to quit.")
        while True:
            try:
                # cmd = input("$ ").strip()
                cmd = self.session.prompt("> ").strip()
            except (EOFError , KeyboardInterrupt):
                print(Fore.GREEN + "\nBye :)\n Have a good time ! ")
                return
            
            if not cmd:
                continue

            if cmd.lower() == "exit":
                print(Fore.GREEN + "Bye :)\n Have a good time ! ")
                return
            
            if cmd.lower() == "help":
                print(Fore.YELLOW  + HELP)
                continue
            
            if cmd.lower() == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                continue
                
            try:
                self._dispatch(cmd)
            
            except ValueError as v:
                print(Fore.RED + f"Error: {v}")
            except TypeError as t:
                print(Fore.RED + f"Error: {t}")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
    
    def _dispatch(self , cmd: str) -> None:
        """
        dispatcher method to call the correct methods on cmd input
        
        Args:
            cmd (str): command typed in the shell
        
        Returns: 
            None
        """

        if cmd.startswith("project create "):
            self._projectCreate(cmd)

        elif cmd.startswith("project list"):
            self._projectList()

        elif cmd.startswith("project delete "):
            self._projectDelete(cmd)

        elif cmd.startswith("project edit "):
            self._projectEdit(cmd)

        elif cmd.startswith("task add "):
            self._taskAdd(cmd)

        elif cmd.startswith("task list "):
            self._taskList(cmd)

        elif cmd.startswith("task status "):
            self._taskStatus(cmd)
        
        elif cmd.startswith("task edit "):
            self._taskEdit(cmd)

        elif cmd.startswith("task delete "):
            self._taskDelete(cmd)

        else:
            print(Fore.RED + f"\"{cmd}\" is not recognized as a command")
    
    def _projectCreate(self , cmd: str) -> None:
        """
        Call to create project

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if name parameter is missing
        
        Returns:
            None
        """
        
        before , sep , after = cmd.partition("project create ")
        name , desc = _split_pipe(after)
        
        if name == "":
            raise ValueError("Project must have a name")

        p = self.projects.createProject(name , desc)
        print(Fore.CYAN  + f"created project {p.name} (id= {p.id})")
    
    def _projectList(self) -> None:
        """Call to list projects"""
        projectList = self.projects.list()
        if not projectList:
            print(Fore.CYAN  + "No project in workspace")
            return
        for p in projectList:
            print(Fore.CYAN  + f"{p.id[:8]} | name: {p.name} | description: {p.desc}")

    def _projectDelete(self , cmd: str) -> None:
        """
        Call to delete project

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if projectId parameter is missing
        
        Returns:
            None
        """

        before , sep , after = cmd.partition("project delete ")
        projectId = after.strip()

        if projectId == "":
            raise ValueError("project id argument is missing")

        self.projects.deleteProject(projectId)
        print(Fore.CYAN  + f"deleted project with id {projectId}")

    def _projectEdit(self , cmd: str) -> None:
        """
        Call to Edit project

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if projectId parameter is missing
        
        Returns:
            None
        """

        before , sep , after = cmd.partition("project edit ")
        projectId , name , desc = _split_pipe(after)
        if projectId == "":
            raise ValueError("project id argument is missing")
        if name == "":
            name = None
        if desc == "":
            desc = None

        p = self.projects.editProject(projectId , name , desc)
        print(Fore.CYAN  + f"Updated project {p.id}")

    def _taskAdd(self , cmd:str ) -> None:
        """
        Call to add task

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if projectId parameter is missing
            ValueError: if task name parameter is missing
        
        Returns:
            None
        """

        before , sep , after = cmd.partition("task add ")
        projectId , name , desc , status , deadline= _split_pipe(after)

        if projectId == "":
            raise ValueError("project id argument is missing")

        if name == "":
            raise ValueError("A task must have a name")
        if status == "":
            status = "todo"
        
        deadlineItem = _parseDeadline(deadline)
        
        t = self.tasks.addTask(projectId , name , desc , status , deadlineItem)
        print(Fore.CYAN  + f"added task {t.name} with id {t.id} to project {projectId}")

    def _taskList(self , cmd:str ) -> None:
        """
        Call to list tasks

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if projectId parameter is missing
        
        Returns:
            None
        """

        before , sep , after = cmd.partition("task list ")
        projectId = after.strip()

        if projectId == "":
            raise ValueError("project id argument is missing")

        tasksList = self.tasks.listTasks(projectId)
         
        if not tasksList:
            print("no tasks")
            return
        
        for t in tasksList:
            print(Fore.CYAN  + f"{t.id} | name: {t.name} | status: {t.status} {f"| deadline: {t.deadline} " if t.deadline else ""} {f"| closed at: {t.at_closed} " if t.at_closed else ""} {f"| description: {t.desc}" if t.desc else ""}")
    
    
    def _taskStatus(self , cmd:str ) -> None:
        """
        Call to change status of a task

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if taskId parameter is missing
        
        Returns:
            None
        """

        before , sep , after = cmd.partition("task status ")
        taskId , newStatus = _split_pipe(after)

        if taskId == "":
            raise ValueError("task id argument is missing")
        

        t = self.tasks.changeTaskStatus(taskId , newStatus)
        print(Fore.CYAN  + f"task {t.id} status changed to {t.status}")

    def _taskEdit(self , cmd:str) -> None:
        """
        Call to edit task

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if taskId parameter is missing
        
        Returns:
            None
        """

        before, sep , after = cmd.partition("task edit ")
        taskId , name , desc , status , deadline= _split_pipe(after)
        
        if taskId == "":
            raise ValueError("task id argument is missing")

        if name == "":
            name = None
        if desc == "":
            desc = None
        if status == "":
            status = None
        
        deadlineItem = _parseDeadline(deadline)
        if deadlineItem is None:
            print(f"{deadline} is not a valid format of date here. deadline defaulted to None. please use yyyy-mm-dd format")
        
        t = self.tasks.editTask(taskId , name , desc , status , deadlineItem) 
        print(Fore.CYAN  + f"task {t.id} updated")
    
    def _taskDelete(self , cmd:str ) -> None:
        """
        Call to delete task

        Args:
            cmd (str): command typed in the shell
        
        Raises:
            ValueError: if taskId parameter is missing
        
        Returns:
            None
        """

        before , sep , after = cmd.partition("task delete ")
        taskId = after.strip()

        if taskId == "":
            raise ValueError("task id argument is missing")

        result = self.tasks.deleteTask(taskId)
        if(result):
            print(Fore.CYAN  + f"deleted task with id {taskId}")