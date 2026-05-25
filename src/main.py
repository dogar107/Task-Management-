from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.tasks.routes import task_routes
from src.users.routes import user_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes)
app.include_router(task_routes)