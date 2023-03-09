import datetime
from fastapi import FastAPI,HTTPException,status
from app.models.models import User
from app.schemas.slot import SlotRequest
from app.models.models import Slot,Bidder,Bid,Task
from sqlalchemy.orm import Session
from sqlalchemy.future import select


def bid_response(bid:Bid):
    response={
        "id":bid.id,
        "name":bid.name,
        "open_time":{
            "year":bid.open_time.year,
            "month":bid.open_time.month,
            "day":bid.open_time.day,
            "hour":bid.open_time.hour,
            "minute":bid.open_time.minute,
        },
        "close_time":{
            "year":bid.close_time.year,
            "month":bid.close_time.month,
            "day":bid.close_time.day,
            "hour":bid.close_time.hour,
            "minute":bid.close_time.minute,
        },
        "slot":{
            "id":bid.slot_id,
            "name":bid.slot.name,
        },
        "start_point":bid.start_point,
        "buyout_point":bid.buyout_point,
        "is_complete":bid.is_complete,
    }
    return response    


def bids_response(bids:list[Bid]):
    respone_bids=[{
        "id":bid.id,
        "name":bid.name,
        "open_time":{
            "year":bid.open_time.year,
            "month":bid.open_time.month,
            "day":bid.open_time.day,
            "hour":bid.open_time.hour,
            "minute":bid.open_time.minute,
        },
        "close_time":{
            "year":bid.close_time.year,
            "month":bid.close_time.month,
            "day":bid.close_time.day,
            "hour":bid.close_time.hour,
            "minute":bid.close_time.minute,
        },
        "slot":{
            "id":bid.slot_id,
            "name":bid.slot.name,
            "start_time":{
            "year":bid.slot.start_time.year,
            "month":bid.slot.start_time.month,
            "day":bid.slot.start_time.day,
            "hour":bid.slot.start_time.hour,
            "minute":bid.slot.start_time.minute,
        },
            "end_time":{
            "year":bid.slot.end_time.year,
            "month":bid.slot.end_time.month,
            "day":bid.slot.end_time.day,
            "hour":bid.slot.end_time.hour,
            "minute":bid.slot.end_time.minute,
        },
        },
        "start_point":bid.start_point,
        "buyout_point":bid.buyout_point,
        "is_complete":bid.is_complete,
    } for bid in bids]
    return respone_bids


def bids_response_for_user(bids:list[Bid],user:User,db:Session):
    respone_bids=bids_response(bids)
    for bid in respone_bids:
        bidder=db.scalars(select(Bidder).filter(Bidder.bid_id==bid['id'],Bidder.user_id==user.id).join(Bid.bidder).order_by(Bidder.point).limit(1)).first()
        if bidder==None:
            bid["user_bidpoint"]="notyet"
            continue
        bid['user_bidpoint']=bidder.point
    return respone_bids

def bidder_response(bidder:Bidder):
    response={
        "id":bidder.bid_id,
        "name":bidder.bid.name,
        "user_id":bidder.user_id,
        'user':bidder.user.name,
        "point":bidder.point
    }
    return response

def bidders_response(bidder:list[Bidder]):
    response=[{
        "id":bidder.bid_id,
        "name":bidder.bid.name,
        "user_id":bidder.user_id,
        'user':bidder.user.name,
        "point":bidder.point
    } for bidder in bidder]
    return response

def slot_response(slot:Slot):
    response={
        "id":slot.id,
        "name":slot.name,
        "start_time":{
            "year":slot.start_time.year,
            "month":slot.start_time.month,
            "day":slot.start_time.day,
            "hour":slot.start_time.hour,
            "minute":slot.start_time.minute,
        },
        "end_time":{
            "year":slot.end_time.year,
            "month":slot.end_time.month,
            "day":slot.end_time.day,
            "hour":slot.end_time.hour,
            "minute":slot.end_time.minute,
        },
        "assignees":users_response(slot.assignees),
        "creater":creater_response(slot.creater),
        "task":slot.task,
        "bid":slot.bid,
        "template":slot.template
        
    }
    return response


def slots_response(slots:list[Slot]):
    response=[{
        "id":slots.id,
        "name":slots.name,
        "start_time":{
            "year":slots.start_time.year,
            "month":slots.start_time.month,
            "day":slots.start_time.day,
            "hour":slots.start_time.hour,
            "minute":slots.start_time.minute,
        },
        "end_time":{
            "year":slots.end_time.year,
            "month":slots.end_time.month,
            "day":slots.end_time.day,
            "hour":slots.end_time.hour,
            "minute":slots.end_time.minute,
        },
        "creater":creater_response(slots.creater),
        "task":task_response(slots.task),
    } for slots in slots]
    return response


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


def tasks_response(tasks:list[Task]):
    response_tasks=[{
        "id":task.id,
        "name":task.name,
        "detail":task.detail,
        "max_worker_num":task.max_woker_num,
        "min_worker_num":task.min_woker_num,
        "exp_worker_num":task.exp_woker_num,
        "creater_id":task.creater_id,
        "creater":task.creater.name
    } for task in tasks]
    
    return response_tasks


def user_response(user:User):
    response_user={"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,
            "achivement":user.achivement,
            "exp_task":user.exp_task,
            "slots":user.slots,
            "create_slot":user.create_slot,
            "create_task":user.create_task,
            "point":user.point,
            "bid":user.bid,
            "is_active":user.is_active}
    return response_user

def creater_response(user:User):
    response_user={"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,}
    return response_user

def users_response(users:list[User]):
    response_users=[{"id":user.id,
            "name":user.name,
            "block":user.block,
            "room_number":user.room_number,
            "point":user.point,
            "is_active":user.is_active} for user in users]
    return response_users