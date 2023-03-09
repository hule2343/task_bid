from typing import Dict
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class DateTime(BaseModel):
    year:int
    month:int
    day:int
    hour:int
    minute:int

class TenderRequest(BaseModel):
    tender_point:int
    class Config:
        orm_mode=True

class BidBase(BaseModel):
    name:str
    open_time:DateTime
    close_time:DateTime
    slot:Dict
    start_point:int
    buyout_point:int
    
class Bid(BaseModel):
    id:UUID
    name:str
    is_complete:bool
    lowest_user_id:UUID
    lowest_user:Dict

class BidRequest(BaseModel):
    name:str|None
    open_time:DateTime
    close_time:DateTime
    slot:UUID
    start_point:int
    buyout_point:int
    class Config:
        orm_mode=True

class BidConvertRequest(BaseModel):
    user_id:str
    class Config:
        orm_mode=True