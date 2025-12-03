from fastapi import APIRouter
from todolist.api.controllers import projects_controller

api_router = APIRouter(prefix="/api")

api_router.include_router(projects_controller.router)
