from fastapi import APIRouter, Depends, status , HTTPException

from todolist.core.services.project_service import ProjectService
from todolist.data.projects_repo import ProjectsRepo
from todolist.data.tasks_repo import TasksRepo
from todolist.config.setting import Setting

from todolist.api.controller_schemas.requests import ProjectCreateRequest , ProjectUpdateRequest
from todolist.api.controller_schemas.responses import ProjectResponse


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


def get_project_service() -> ProjectService:
    """
    Dependency that creates a ProjectService instance.
    """
    setting = Setting.initializeSettings()
    projects_repo = ProjectsRepo()
    tasks_repo = TasksRepo()
    return ProjectService(projects_repo, tasks_repo, setting)


@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="List all projects",
    description=(
        "Return the complete list of projects stored in the system. "
        "Projects are returned in the order provided by the repository."
    ),
    responses={
        200: {"description": "List of projects returned successfully."},
    },
)
async def list_projects(service: ProjectService = Depends(get_project_service)):
    """
    Return all projects.
    """
    projects = service.list()
    return projects


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description=(
        "Create a new project with a name and optional description. "
        "The name must satisfy length constraints and must be unique among projects."
    ),
    responses={
        201: {"description": "Project created successfully."},
        400: {"description": "Validation error (name length, duplicate name, etc.)."},
    },
)
async def create_project(
    request: ProjectCreateRequest,
    service: ProjectService = Depends(get_project_service),
):
    """
    Create a new project using the service layer.
    """
    project = service.createProject(name=request.name, desc=request.desc or "")
    return project


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project by id",
    description="Retrieve a single project using its ID.",
    responses={
        200: {"description": "Project found and returned."},
        404: {"description": "Project with the given ID was not found."},
    },
)
async def get_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
):
    """
    Get a single project.
    """
    try:
        project = service.getProject(project_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    return project


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update an existing project",
    description=(
        "Update one or more fields of an existing project. "
        "Fields that are not provided in the request body remain unchanged."
    ),
    responses={
        200: {"description": "Project updated successfully."},
        400: {"description": "Validation error (invalid name, description, etc.)."},
        404: {"description": "Project with the given ID was not found."},
    },
)
async def update_project(
    project_id: str,
    request: ProjectUpdateRequest,
    service: ProjectService = Depends(get_project_service),
):
    """
    Partially update a project.
    """
    try:
        project = service.editProject(projectId=project_id, newName=request.name, newDesc=request.desc)
    except ValueError as e:
        message = str(e)
        if message == "Project not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)

    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Delete an existing project by its ID.",
    responses={
        204: {"description": "Project deleted successfully (no content)."},
        404: {"description": "Project with the given ID was not found."},
    },
)
async def delete_project(
    project_id: str,
    service: ProjectService = Depends(get_project_service),
):
    """
    Delete a project.
    """
    try:
        deleted = service.deleteProject(project_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return


