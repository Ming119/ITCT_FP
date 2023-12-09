from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
origins = [
  "http://localhost:3000",
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

@app.post("/send")
def send(data: Data):
  print(data.message)
  return {"message": "Message received"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
