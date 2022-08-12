
from typing import Union
from login import handleLogin
from login import getTelegramCode

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Login(BaseModel):
    appId: str
    appHash: str
    phoneNumber: str

@app.get("/")


def read_root():
    return {"Hello": "World"}
LoginCredentials = {}
@app.post("/login")
async def login(credentials: Login):
     print(credentials,type(credentials))
    #  print(credentials.AppId)
     LoginCredentials['appId'] = credentials.appId
     LoginCredentials['appHash'] = credentials.appHash
     LoginCredentials['phoneNumber'] = credentials.phoneNumber
     handleLogin(getattr(getattr(credentials,'phoneNumber'),credentials,'appId'),getattr(credentials,'appHash'))

@app.post('/getTelegramCode')
def getCode(code:int):
    getTelegramCode(LoginCredentials['phoneNumber'],code)