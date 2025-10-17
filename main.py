from todolist.config.setting import Setting
from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.interface.CLI.sh import CLI


def main():
    settings =  Setting().initializeSettings()
    project_repo = ProjectsRepo()
    task_repo = TasksRepo()
    project_service = ProjectService(project_repo, task_repo, settings)
    task_service = TaskService(project_repo , task_repo , settings )

    cli = CLI(project_service , task_service)
    cli.run()

if __name__ == "__main__":
    main()