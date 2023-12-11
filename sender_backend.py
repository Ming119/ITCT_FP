from time import sleep
from gpiozero import LED
from fastapi import FastAPI
from pydantic import BaseModel
from hamming_code import hamming_encode
from fastapi.middleware.cors import CORSMiddleware

# === LED SETTING ===
# FIXME: gpio busy when init led
# led = LED(13)

def add_header(msg: str):
  preamble = f'{0xAAAA:0>16b}'
  length   = f'{len(msg):0>16b}'
  return preamble + length + msg

# FIXME: ref to above FIXME
# def send_msg(msg: str):
#   for i in msg:
#     if i == '1':
#       led.on()
#       sleep(0.005)
#       led.off()
#     else:
#       led.on()
#       sleep(0.003)
#       led.off()
#     sleep(0.003)
# ===================

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
  encoded_message = hamming_encode(data.message)
  package = add_header(encoded_message)
  
  # TODO: add header to encoded_message
  # then send the message to recivier
  # FIXME: ref to above FIXME
  # await send_msg(package)

  return {"message": "Message sent"}
# ==========================

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("sender_backend:app", host="0.0.0.0", port=8001, reload=True)
