from typing import Union
from fastapi import FastAPI
from app.router import admin, achivement,authority,bid, slot, user,auth,task,bidder,tag
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


origins = [
    'http://localhost:3000','http://localhost:5432'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(admin.router,prefix='/admin')
app.include_router(achivement.router,prefix="/achivements")
app.include_router(authority.router,prefix="/authority")
app.include_router(bid.router,prefix="/bids")
app.include_router(slot.router,prefix="/slots")
app.include_router(task.router,prefix="/tasks")
app.include_router(user.router,prefix="/users")
app.include_router(auth.router,prefix="")
app.include_router(bidder.router,prefix="/bidders")
app.include_router(tag.router,prefix="/tags")