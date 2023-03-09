from fastapi import APIRouter
from app.models.models import Authority,Method,User
from sqlalchemy.orm import Session
from fastapi import Depends
from app.cruds.auth import get_current_active_user,check_authority,authority_post
from app.database import get_db
from sqlalchemy.future import select
from app.schemas.authority import AuthorityRequest                                   
from app.cruds import bid
router=APIRouter()

@router.post("/closebid")
async def close_finished_bid(db:Session=Depends(get_db)):
    response=bid.close_all_bid(db)
    return response


