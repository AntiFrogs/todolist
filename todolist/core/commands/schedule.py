import schedule
from todolist.core.services.task_service import TaskService 
from todolist.core.services.project_service import ProjectService 

def scheduleCommands(taskService: TaskService , projectService: ProjectService) -> None:
    """
    schdules services

    Params:
        taskService: TaskService
        projectService: ProjectService

    Returns:
        None
    """

    schedule.every().day.at("00:00:01").do(taskService.autoCloseOverdueTasks)

    #  Running all when the program runs
    schedule.run_all() 