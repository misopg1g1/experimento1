from fastapi import FastAPI,HTTPException
from fastapi import Body
from cryptography.fernet import Fernet
import logging
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse
import hashlib
import httpx
import os


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
    resultFromCheck = checkHash(message)
    logging.debug(resultFromCheck)
    if resultFromCheck:
        #Encode and send to sidecar
        fernet = Fernet(keySecret.encode())
        encoded = json.dumps(message).encode()
        encrypted = fernet.encrypt(encoded)
        strEncryted = encrypted.decode()
        msg = { "encrypted": strEncryted }
        url = os.getenv('URL_MICRO','http://localhost:8005')
        logging.debug(msg)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=msg)
        return response.json()
    else: 
        raise HTTPException(status_code=403,detail='Informacion alterada')