from fastapi import FastAPI,HTTPException
from fastapi import Body
from cryptography.fernet import Fernet
import logging
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse
import hashlib


app = FastAPI()
# Definir como secreto
keySecret = "ExychbZpaYH93LDTjPvflVgSOXkkIkR999XP_gkBIHk="

logging.basicConfig(filename='app.log', level=logging.DEBUG)

def checkHash(message: dict[str, str]):
    newMsg = message.copy()
    if "hash" in newMsg:
        del newMsg["hash"]
    hash_object = hashlib.md5()
    hash_object.update(json.dumps(newMsg).encode())
    if "hash" in message and message["hash"] == hash_object.hexdigest():
        return True
    else:
        return False
     

@app.post("/")
async def decrypt_message(message: dict[str, str]):
    return 'Response from the microservice!'