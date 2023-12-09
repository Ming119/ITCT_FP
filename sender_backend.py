from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from hamming_code import hamming_encode, hamming_decode

app = FastAPI()
origins = [
  "http://localhost:3000",  # frontend
]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class Data(BaseModel):
  message: str

@app.get("/")
def read_root():
  return {"message": "Hello World"}

@app.post("/send")
def send(data: Data):
  encoded_message = hamming_encode(data.message)


  return {"message": "Message received"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("sender_backend:app", host="0.0.0.0", port=8001, reload=True)
