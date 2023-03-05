from fastapi import FastAPI
from fastapi import Body
from cryptography.fernet import Fernet
import logging
from pydantic import BaseModel
import json
from fastapi.responses import JSONResponse

app = FastAPI()
key = "ExychbZpaYH93LDTjPvflVgSOXkkIkR999XP_gkBIHk="


class Message(BaseModel):
    text: str


logging.basicConfig(filename='app.log', level=logging.DEBUG)


@app.post("/decrypt")
async def decrypt_message(message: Message):
    fernet = Fernet(key.encode())
    testJson = {'user': 'gerzonElCrack', 'hash': '12121'}
    convertedJson = json.dumps(testJson)
    enconded = convertedJson.encode()
    encrypted = fernet.encrypt(enconded)
    logging.debug(encrypted)
    try:
        decrypted = fernet.decrypt(message.text.encode())
        return json.loads(decrypted.decode())
    except Exception as e:
        logging.debug('error', e)
        return {"error": str(e)}