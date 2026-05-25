from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.utils.helpers import isauthenticated
from src.utils.db import get_db
from src.tasks.dtos import TaskSchema
from src.tasks import controller

task_routes = APIRouter(prefix="/tasks")


@task_routes.post("/create")
def create_task(
    body: TaskSchema,
    db: Session = Depends(get_db),
    user = Depends(isauthenticated)
):
    return controller.create_task(body, db, user)


@task_routes.get("/all-tasks")
def get_tasks(
    db: Session = Depends(get_db),
    user = Depends(isauthenticated)
):
    return controller.get_tasks(db, user)


@task_routes.delete("/delete/{id}")
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(isauthenticated)
):
    return controller.delete_task(id, db, user)


@task_routes.put("/update/{id}")
def update_task(
    id: int,
    body: TaskSchema,
    db: Session = Depends(get_db),
    user = Depends(isauthenticated)
):
    return controller.update_task(id, body, db, user)