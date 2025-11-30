from todolist.config.setting import Setting
from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.interface.CLI.sh import CLI
from todolist.core.commands.schedule import scheduleCommands


def main():
    """The starting point of the program"""
    settings =  Setting().initializeSettings()
    project_repo = ProjectsRepo()
    task_repo = TasksRepo()
    project_service = ProjectService(project_repo, task_repo, settings)
    task_service = TaskService(project_repo , task_repo , settings )

    scheduleCommands(task_service , project_service)
    
    cli = CLI(project_service , task_service)
    cli.run()

# Only running when called and not when imported
if __name__ == "__main__":
    main()