from fastapi import FastAPI ,status,HTTPException
from app.models.models import Authority
from app.models.models import Task,TaskTag
from app.schemas.task import TaskCreate,TaskUpdate
from app.schemas.users import User
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.future import select

async def task_all(db:Session):
    items=await db.scalars(select(Task)).all()
    return items


async def task_get(name:str,db:Session):
    item=db.scalars(select(Task).filter_by(name=name).limit(1)).first()
    return item

def task_response(task:Task):
    response_task={
        "id":task.id,
        "name":task.name,
        "detail":task.detail,
        "max_worker_num":task.max_woker_num,
        "min_worker_num":task.min_woker_num,
        "exp_worker_num":task.exp_woker_num,
        "creater_id":task.creater_id,
        "creater":task.creater.name
    }
    return response_task


def task_post(task:TaskCreate,current_user:User,db:Session):
    task=Task(creater=current_user, **task.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def task_delete(name:str,db:Session):
    db.scalars(select(Task).filter_by(name=name)).delete()
    db.commit()
    return name


def task_patch(request:TaskUpdate,task_id:str,db:Session):
    task=db.get(Task,task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No note with this id: {task_id} found')
    db.execute(update(Task).where(Task.id==task_id).values(
        name=request.name if request.name else task.name,
        detail=request.detail if request.detail else task.detail,
        max_woker_num=request.max_woker_num if request.max_woker_num else task.max_woker_num,
        min_woker_num=request.min_woker_num if request.min_woker_num else task.min_woker_num,
        exp_woker_num=request.exp_woker_num if request.exp_woker_num else task.exp_woker_num,
    ).execution_options(synchronize_session="evaluate"))
    db.commit()
    return task_response(task)


def task_add_authority(request:list[str],task_id:str,db:Session):
    task=db.get(Task,task_id)
    new_authority=[]
    for authority_id in request:
        authority=db.get(Authority,authority_id)
        new_authority.append(authority)
    task.authority=list(set(new_authority))
    db.commit()
    return task


def task_add_tag(request:list[str],task_id:str,db:Session):
    task=db.get(Task,task_id)
    new_tag=[]
    for tag_id in request:
        tag=db.get(TaskTag,tag_id)
        new_tag.append(tag)
    task.tag=list(set(new_tag))
    db.commit()
    return task

    