from time import sleep
from fastapi import FastAPI
from pydantic import BaseModel
from hamming_code import hamming_encode
from fastapi.middleware.cors import CORSMiddleware
from gpiozero import LED
import asyncio

async def send_msg(msg: str):
  led = LED(13)
  for i in msg:
    if i == '1':
      led.on()
      await asyncio.sleep(0.008)
      led.off()
    else:
      led.on()
      await asyncio.sleep(0.004)
      led.off()
    await asyncio.sleep(0.004)
  led.close()

# === WEB SERVER SETTING ===
app = FastAPI()
origins = ["http://localhost:3000",]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class Data(BaseModel):
  message: str

@app.post("/send")
async def send(data: Data):
  encoded_message = await hamming_encode(data.message)
  preamble = f'{0xAAAA:0>16b}'
  length   = f'{len(encoded_message):0>16b}'
  package  = preamble + length + encoded_message
  print(preamble)
  print(length)
  print(package)
  await send_msg(package)

  return {"message": "Message sent"}
# ==========================

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("sender_backend:app", host="0.0.0.0", port=8001, reload=True)

