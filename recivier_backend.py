from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from grove.adc import ADC
from time import sleep
import asyncio
import timeit
from hamming_code import hamming_decode
from bitarray import bitarray

# === LIGHT SENSOR SETTING ===
threshold = 300
channel = 2
adc = ADC()
timer = timeit.default_timer
decoded_message = ''

async def read_header(channel, adc) -> float:
  count    = 0
  interval = 0

  while adc.read(channel) < threshold:
    pass

  while True:
    start = timer()
    while adc.read(channel) > threshold:
      pass

    interval += timer() - start
    count += 1

    if count == 16: break
    while adc.read(channel) < threshold:
      pass
  
  return interval / count

async def read_length(channel, adc, interval) -> int:
  count      = 0
  length_str = ""

  while adc.read(channel) < threshold:
    pass

  while True:
    start = timer()
    while adc.read(channel) > threshold:
      pass

    t = timer() - start
    length_str += t > interval and "1" or "0"
    count += 1

    if count == 16: break
    while adc.read(channel) < threshold:
      pass
  
  return int(length_str, 2)

async def read_data(channel, adc, interval, length) -> str:
  count    = 0
  data_str = ''

  while adc.read(channel) < threshold:
    pass

  while True:
    start = timer()
    while adc.read(channel) > threshold:
      pass

    t = timer() - start
    data_str += t > interval and "1" or "0"
    count += 1

    if count == length * 12: break
    while adc.read(channel) < threshold:
      pass

  return data_str

async def read_message():
  global decoded_message
  while True:
    interval = await read_header(channel, adc)
    length = await read_length(channel, adc, interval)
    start = timer()
    message = await read_data(channel, adc, interval, length)
    end = timer()
    decoded_message = hamming_decode(message)
    print(decoded_message, end = '')
    print(f"bps: {length*12 / (end - start)}")
# ============================

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

@app.post("/get_recive")
def get_recive():
  global decoded_message
  message = decoded_message
  decoded_message = ''
  return {"message": message}

@app.on_event("startup")
async def startup_event():
  asyncio.create_task(read_message())
# ==========================

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("recivier_backend:app", host="0.0.0.0", port=8002, reload=True)
  