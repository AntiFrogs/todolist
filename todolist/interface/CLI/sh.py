from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService


HELP = """
Commands:
  help
  exit
  project create <name> | <description>
  project list
  project delete <project_id>
  project edit <project_id> | [name or ""] | [description or ""]
  task add <project_id> | <title> | <description>
  task list <project_id>
  task status <task_id> | <todo|doing|done>
  task delete <task_id>
"""

def _split_pipe(s: str) -> list[str]:
    return [part.strip() for part in s.split("|")]



class CLI:

    def __init__(self, project_service: ProjectService, task_service: TaskService) -> None:
        self.projects = project_service
        self.tasks = task_service
    

    def run(self) -> None:
        print("Cli todolist app. type help for command list. exit to quit.")
        while True:
            try:
                cmd = input("$ ").strip()
            except (EOFError , KeyboardInterrupt):
                print("\nBye :)\n Have a good time ! ")
                return
            
            if not cmd:
                continue

            if cmd.lower() == "exit":
                print("Bye :)\n Have a good time ! ")
                return
            
            if cmd.lower() == "help":
                print(HELP)
                continue
                
            try:
                self._dispatch(cmd)
            
            except ValueError as v:
                print(f"Error: {v}")
            except TypeError as t:
                print(f"Error: {t}")
            except Exception as e:
                print(f"Error: {e}")
    
    def _dispatch(self , cmd: str) -> None:
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

        elif cmd.startswith("task delete "):
            self._taskDelete(cmd)

        else:
            print("Command is not valid")
    
    def _projectCreate(self , cmd: str) -> None:
        before , sep , after = cmd.partition("project create ")
        name , desc = _split_pipe(after)
        p = self.projects.createProject(name , desc)
        print(f"created project {p.name} (id= {p.id})")
    
    def _projectList(self) -> None:
        projectList = self.projects.list()
        if not projectList:
            print("No project in workspace")
            return
        for p in projectList:
            print(f"{p.id[:8]} | name: {p.name} | description: {p.desc}")

    def _projectDelete(self , cmd: str) -> None:
        before , sep , after = cmd.partition("project delete ")
        projectId = after.strip()
        removed = self.projects.deleteProject(projectId)
        print(f"deleted project with id {projectId}")

    def _projectEdit(self , cmd: str) -> None:
        before , sep , after = cmd.partition("project edit ")
        projectId , name , desc = _split_pipe(after)
        if name == "":
            name = None
        if desc == "":
            desc = None

        p = self.projects.editProject(projectId , name , desc)
        print(f"Updated project {p.id}")

    def _taskAdd(self , cmd:str ) -> None:
        before , sep , after = cmd.partition("task add ")
        projectId , name , desc = _split_pipe(after)
        t = self.tasks.addTask(projectId , name , desc)
        print(f"added task {t.name} with id {t.id} to project {projectId}")

    def _taskList(self , cmd:str ) -> None:
        before , sep , after = cmd.partition("task list ")
        projectId = after.strip()
        tasksList = self.tasks.listTasks(projectId)
         
        if not tasksList:
            print("no tasks")
            return
        
        for t in tasksList:
            print(f"{t.id[:8]} | name: {t.name} | status: {t.status} | description: {t.desc}")
    
    
    def _taskStatus(self , cmd:str ) -> None:
        before , sep , after = cmd.partition("task status ")
        taskId , newStatus = _split_pipe(after)
        t = self.tasks.changeTaskStatus(taskId , newStatus)
        print(f"task {t.id} status changed to {t.status}")
    
    
    def _taskDelete(self , cmd:str ) -> None:
        before , sep , after = cmd.partition("task delete ")
        taskId = after.strip()
        result = self.tasks.deleteTask(taskId)
        if(result):
            print(f"deleted task with id {taskId}")