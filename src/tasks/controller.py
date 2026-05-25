from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import Task
from fastapi import HTTPException


# CREATE TASK
def create_task(body: TaskSchema, db: Session, user: dict):
    data = body.model_dump()

    new_task = Task(
        title=data["title"],
        description=data["description"],
        user_id=user["id"]
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {"status": "success", "data": new_task}


# GET ALL TASKS
def get_tasks(db: Session, user: dict):
    tasks = db.query(Task).filter(Task.user_id == user["id"]).all()
    return {"status": "success", "data": tasks}


# GET TASK BY ID
def get_tasks_id(task_id: int, db: Session):
    task = db.query(Task).get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"status": "success", "data": task}


# UPDATE TASK
def update_task(task_id: int, body: TaskSchema, db: Session, user: dict):
    task = db.query(Task).get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    data = body.model_dump()

    for key, value in data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return {"status": "success", "data": task}


# DELETE TASK
def delete_task(task_id: int, db: Session, user: dict):
    task = db.query(Task).get(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(task)
    db.commit()

    return {"status": "success", "message": "Task deleted successfully"}