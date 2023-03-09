import datetime
from fastapi import FastAPI,HTTPException,status
from app.models.models import User
from app.schemas.slot import SlotRequest
from app.models.models import Slot,Bidder,Task,Bid
from sqlalchemy.orm import Session
from app.cruds.response import slots_response, slot_response,user_response ,bidder_response
from sqlalchemy.future import select
from app.cruds.bidder import bidder_get
def slot_all(db:Session):
    items=db.scalars(select(Slot)).all()
    
    return slots_response(items)
def slot_finished(db:Session):
    item=db.execute(select(Slot).filter(Slot.end_time<datetime.datetime.now())).scalars().all()
    return slots_response(item)
def slot_get(name:str,db:Session):
    item=db.scalars(select(Slot).filter_by(name=name).limit(1)).first()
    respone_slot=slot_response(item)
    return respone_slot


def slot_post(slot:SlotRequest,db:Session,user:User):
    task=db.get(Task,slot.task)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    slot=Slot(name=slot.name,
              start_time=datetime.datetime(slot.start_time.year,
                                           slot.start_time.month,
                                           slot.start_time.day,
                                           slot.start_time.hour,
                                           slot.start_time.minute),
              end_time=datetime.datetime(slot.end_time.year,
                                           slot.end_time.month,
                                           slot.end_time.day,
                                           slot.end_time.hour,
                                           slot.end_time.minute),
              task_id=slot.task,
              creater_id=user.id)
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot_response(slot)

def slot_cancel(slot_id:str,user:User,premire_point:int ,db:Session):
    slot=db.get(Slot,slot_id)
    bid=slot.bid
    if bid is None:
        raise HTTPException(
            status_code =status.HTTP_405_METHOD_NOT_ALLOWED
        )
    bidder=db.scalars(select(Bidder).filter(Bidder.bid_id==bid.id,Bidder.user_id==user.id).limit(1)).first()
    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    if bidder.is_canceled:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT
        )
    bidder.is_canceled=True
    bidder.point+=premire_point
    user.point-=premire_point
    db.commit()
    return slot_response(slot)


def slot_reassign(slot_id:str,user_id:str,db:Session):
    slot=db.get(Slot,slot_id)
    bid=slot.bid
    if bid is None:
        raise HTTPException(
            status_code =status.HTTP_405_METHOD_NOT_ALLOWED
        )
    bidder=db.scalars(select(Bidder).filter(Bidder.bid_id==bid.id,Bidder.user_id==user_id).limit(1)).first()
    if not bidder:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    bidder.is_canceled=False
    db.commit()
    user=db.get(User,user_id)
    slot.assignees.append(user)
    db.commit()
    return slot

    
def slot_complete(slot_id:str,user:User,db:Session):
    slot=db.get(Slot,slot_id)
    if slot.start_time > datetime.datetime.now():
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )
    slots = user.slots
    if slot not in slots:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )
    bid=slot.bid
    bidder=db.scalars(select(Bidder).filter(Bidder.bid_id==bid.id,Bidder.user_id==user.id).limit(1)).first()
    slot.assignees.remove(user)
    user.exp_task.append(slot.task)
    user.point+=bidder.point
    db.commit()
    return user_response(user)


