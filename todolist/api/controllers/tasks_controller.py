from fastapi import APIRouter, Depends, HTTPException, status

from todolist.core.services.task_service import TaskService
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.config.setting import Setting

from todolist.api.controller_schemas.requests import (
    TaskCreateRequest,
    TaskUpdateRequest,
)
from todolist.api.controller_schemas.responses import TaskResponse


router = APIRouter(tags=["tasks"])

def get_task_service() -> TaskService:
    """
    Dependency that creates a TaskService instance.
    """
    setting = Setting.initializeSettings()
    projects_repo = ProjectsRepo()
    tasks_repo = TasksRepo()
    return TaskService(projects_repo, tasks_repo, setting)


@router.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskResponse],
    summary="List tasks of a project",
)
async def list_project_tasks(project_id: str, service: TaskService = Depends(get_task_service)):
    """
    List all tasks that belong to a given project.
    """
    try:
        tasks = service.listTasks(project_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return tasks


@router.post( "/projects/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Create a task in a project")
async def create_task_for_project(
    project_id: str,
    request: TaskCreateRequest,
    service: TaskService = Depends(get_task_service),
):
    """
    Create a new task inside the specified project.
    """
    try:
        task = service.addTask(projectId=project_id, name=request.name, desc=request.desc or "", status=request.status or "todo", deadline=request.deadline)
    except ValueError as e:
        message = str(e)
        if message == "Project not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    return task



@router.get( "/tasks/{task_id}", response_model=TaskResponse, summary="Get a task by id")
async def get_task( task_id: str, service: TaskService = Depends(get_task_service)):
    """
    Get a single task by its id.
    """
    try:
        task = service.getTask(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task



@router.patch( "/tasks/{task_id}", response_model=TaskResponse, summary="Update an existing task")
async def update_task( task_id: str, request: TaskUpdateRequest, service: TaskService = Depends(get_task_service)):
    """
    Partially update a task.
    """

    # data = request.model_dump(exclude_unset=True)

    # new_name = data.get("name")
    # new_desc = data.get("desc")
    # new_status = data.get("status")
    # new_deadline = data.get("deadline")

    try:
        task = service.editTask(
            taskId=task_id,
            name= request.name ,
            desc= request.desc ,
            status= request.status ,
            deadline= request.deadline ,
        )
    except ValueError as e:
        message = str(e)
        if message == "Task not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

    return task


@router.delete( "/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a task")
async def delete_task(task_id: str, service: TaskService = Depends(get_task_service) ):
    """
    Delete a task by id.
    """
    try:
        deleted = service.deleteTask(task_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return