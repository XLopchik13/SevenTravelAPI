from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import TaskCreate, TaskUpdate, TaskInDB
from app.CRUD import create_task, get_task, get_tasks, update_task, delete_task
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=TaskInDB)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    return await create_task(db, task.title, task.description, task.status)


@router.get("/", response_model=list[TaskInDB])
async def read_tasks(status: str | None = None, db: AsyncSession = Depends(get_db)):
    tasks = await get_tasks(db, status)
    return tasks


@router.get("/{task_id}", response_model=TaskInDB)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskInDB)
async def update_existing_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    updated_task = await update_task(db, task_id, task.title, task.description, task.status)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_existing_task(task_id: int, db: AsyncSession = Depends(get_db)):
    deleted_task = await delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
