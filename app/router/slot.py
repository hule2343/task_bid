import app.cruds.user as crud
from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.responses import JSONResponse
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.models import User,Bidder,Bid,Slot
from app.schemas.users import UserBase,UserDisplay
from app.schemas.slot import SlotRequest,SlotCancelRequest
from app.router.auth import Token
from app.cruds.auth import oauth2_scheme,get_current_active_user
import app.cruds.slot as crud
from typing import Union
from sqlalchemy.future import select

router=APIRouter()

@router.get("/")
async def slot_list(name:str|None=None,end:bool|None=None,db:Session=Depends(get_db)):
    if name:
        slot=crud.slot_get(name,db)
        return slot
    if end:
        slot=crud.slot_finished(db)
    slots=crud.slot_all(db)
    return slots

@router.post("/")
async def slot_post(slot:SlotRequest,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)):
    response=crud.slot_post(slot,db,user)
    return response


@router.post("/{slot_id}/cancel")
async def slot_cancel(slot_id:str,request:SlotCancelRequest,user:User=Depends(get_current_active_user) , db:Session=Depends(get_db)):
    slot=crud.slot_cancel(slot_id,user,request.premire_point,db)
    return slot

@router.post('/{slot_id}/reassign')
async def slot_reassign(slot_id:str,user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    slot=crud.slot_reassign(slot_id,user.id,db)
    return crud.slot_response(slot)

@router.post('/{slot_id}/complete')
async def slot_complete(slot_id:str,user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    response=crud.slot_complete(slot_id,user,db)
    return response

