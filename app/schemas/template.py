from uuid import UUID
from pydantic import BaseModel



class TemplateCreate(BaseModel):
    name:str
    slots:list[str]=[]

