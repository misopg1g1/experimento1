from fastapi import FastAPI, HTTPException
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

logger = logging.getLogger('logerapp')
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
    if "encrypted" in message:
        fernet = Fernet(keySecret.encode())
        encoded = message["encrypted"].encode()
        decrypted = fernet.decrypt(encoded)
        msg = json.loads(decrypted.decode())
        result = checkHash(msg)
        if result:
            #Llamar microservicio
            url = os.getenv('URL_MICRO',"http://localhost:8006")
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=msg)
            return response.json()
        else:
            raise HTTPException(status_code=403,detail='Informacion alterada')
    else:
        raise HTTPException(status_code=403,detail='Fallo encriptacion')