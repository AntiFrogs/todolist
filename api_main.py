from fastapi import FastAPI

from todolist.api.routers import api_router
from todolist.config.setting import Setting
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.core.services.project_service import ProjectService
from todolist.core.services.task_service import TaskService
from todolist.core.commands.schedule import scheduleCommands

app = FastAPI(
    title="TodoList API",
    version="1.0.0",
    description="Phase 3 Web API for the TodoList project",
)

app.include_router(api_router)


def _build_services() -> tuple[ProjectService, TaskService]:
    """
    Create ProjectService and TaskService
    """
    settings = Setting().initializeSettings()
    project_repo = ProjectsRepo()
    task_repo = TasksRepo()
    project_service = ProjectService(project_repo, task_repo, settings)
    task_service = TaskService(project_repo, task_repo, settings)
    return project_service, task_service


@app.on_event("startup")
def startup_schedule_autoclose() -> None:
    """
    FastAPI startup hook that runs once when the API server starts.
    """
    project_service, task_service = _build_services()
    scheduleCommands(task_service, project_service)
