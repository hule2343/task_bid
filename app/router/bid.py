from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.bid import BidRequest,TenderRequest
from app.models.models import User
from app.models.models import Bid,Bidder
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds.auth import get_current_active_user
import app.cruds.bid as crud
import app.cruds.slot as crudslot
from app.cruds import auth
from  sqlalchemy.future import select
router=APIRouter()

@router.get("/")
async def bid_get(name:str|None=None,db:Session=Depends(get_db)):
    if name:
        bid=crud.bid_get(name,db)
        return bid
    bids=crud.bid_all(db)
    return bids
    
@router.post("/")
async def bid_post(bid:BidRequest,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)):
    if auth.check_authority(user,'POST','/bids/'):
        response=crud.bid_post(bid,db,user)
        return response
    elif bid.buyout_point==0:
        response=crud.bid_post(bid,db,user)
        return response

@router.post('/personal')
async def bid_post_personal(bid:BidRequest,db:Session=Depends(get_db),user:User=Depends(get_current_active_user)):
    if auth.check_authority(user,'POST','/bids/personal'):
        response=crud.bid_post_personal(bid,db,user)
        return response

@router.get('/open')
async def bid_user_bidable(db:Session=Depends(get_db)):
    response=crud.bid_user_bidable(db)
    return response


@router.get('/lack')
async def bid_user_lacking(user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    response=crud.bid_lack(user,db)
    return response["lack_bids"]

@router.get('/lack_exp')
async def bid_exp_lacking(user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    response=crud.bid_lack(user,db)
    return response["lack_exp_bids"]

@router.post("/{bid_id}/tender")
async def bid_tender(bid_id:str,request:TenderRequest,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    bid=db.get(Bid,bid_id)
    if bid.is_complete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    response=crud.bid_tender(bid_id,request.tender_point,current_user,db)
    return response

@router.post("/{bid_id}/tenderlack")
async def bid_tenderlack(bid_id:str,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_db)):
    bid=db.get(Bid,bid_id)
    if not bid.is_complete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if not bid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    response=crud.bid_tenderlack(bid_id,current_user,db)
    return response

@router.post("/{bid_id}/close")
async def bid_close(bid_id:str,db:Session=Depends(get_db)):
    slot=crud.bid_close(bid_id,db)
    return slot

@router.get('/lack')
async def bid_get_lack(db:Session=Depends(get_db)):
    bids=crud.bid_lack(db)
    return bids

