from fastapi import FastAPI
from app.models.models import User,Task,Slot
from app.schemas.users import UserBase
from app.cruds.auth import get_password_hash
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import delete
from app.cruds.response import user_response,slots_response,tasks_response
import datetime
def user_all(db:Session):
    items=db.scalars(select(User)).all()
    response_users=[{"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,
            "point":user.point,
            "is_active":user.is_active} for user in items]
    return response_users

def user_get(name:str,db:Session):
    item=db.scalars(select(User).filter_by(name=name).limit(1)).first()
    response_user=user_response(item)
    return response_user


def user_register(user:UserBase,db:Session):
    user.password=get_password_hash(user.password)
    item = User(**user.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    response_user=user_response(item)
    return response_user

def user_delete(name:str,db:Session):
    db.execute(delete(User).where(User.name==name))
    db.commit()
    return name


def add_user_exp_task(request,user:User,db:Session):
    user=db.get(User,user.id)
    for task_id in request.exp_task:
        task=db.get(Task,task_id)
        user.exp_task.append(task)
    db.commit()
    return user_response(user)

def user_createslots(user_id:str,db:Session):
    user=db.get(User,user_id)
    slots=user.create_slot
    return slots_response(slots)

def user_createtask(user_id:str,db:Session):
    user=db.get(User,user_id)
    tasks=user.create_task
    return tasks_response(tasks)

def user_endslots(user_id:str,db:Session):
    slots=db.get(User,user_id).slots
    response_slots=[slot for slot in slots if slot.end_time<datetime.datetime.now()]
    return slots_response(response_slots)

def user_slots(user_id:str,db:Session):
    slots=db.get(User,user_id).slots
    response_slots=[slot for slot in slots if slot.end_time>datetime.datetime.now()]
    return slots_response(response_slots)