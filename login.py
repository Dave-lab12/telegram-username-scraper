from http import client
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import json


client

def handleLogin(phone, api_id, api_hash):
    client = TelegramClient(phone, api_id, api_hash)
    # If you don't have a active session it will create one for you.
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        return "code sent to your phone"
    return "logged in"

def getTelegramCode(phone,code):
    client.sign_in(phone, code)
    return "successfully logged in"

def getGroups():
    chats = []
    last_date = None
    chunk_size = 2000
    groups = []

    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue