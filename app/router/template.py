from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.cruds import template as crud
from app.cruds.auth import get_current_active_user
from app.schemas.template import TemplateCreate
from app.schemas.users import User
from app.models.models import Template
from sqlalchemy.future import select
router=APIRouter()

@router.get("/")
async def template_get(db:Session=Depends(get_db)):
    templates=db.execute(select(Template)).scalars().all()
    return templates

@router.post("/")
async def template_post(request:TemplateCreate,db:Session=Depends(get_db)):
    temple=crud.template_post(request,db)
    return temple

@router.post('/{template_id}/generate')
async def generate_slots_from_template(template_id:str,user:User=Depends(get_current_active_user),db:Session=Depends(get_db))
    
