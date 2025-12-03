from fastapi import FastAPI
from todolist.api.routers import api_router

app = FastAPI(
    title="TodoList API",
    version="1.0.0",
    description="Phase 3 Web API for the TodoList project",
)

app.include_router(api_router)
