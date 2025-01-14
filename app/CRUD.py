from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Task, TaskStatus


async def create_task(db: AsyncSession, title: str, description: str | None, status: TaskStatus):
    new_task = Task(title=title, description=description, status=status)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


async def get_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()


async def get_tasks(db: AsyncSession, status: TaskStatus | None = None):
    query = select(Task)
    if status:
        query = query.where(Task.status == status)
    result = await db.execute(query)
    return result.scalars().all()


async def update_task(db: AsyncSession, task_id: int, title: str, description: str | None, status: TaskStatus):
    task = await get_task(db, task_id)
    if not task:
        return None
    task.title = title
    task.description = description
    task.status = status
    await db.commit()
    await db.refresh(task)
    return task


async def delete_task(db: AsyncSession, task_id: int):
    task = await get_task(db, task_id)
    if not task:
        return None
    await db.delete(task)
    await db.commit()
    return task
