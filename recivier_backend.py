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

@app.get("/")
def read_root():
  return {"message": "Hello World"}

@app.post("/get_recive")
def send():
  return {"message": "TBD"}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run("recivier_backend:app", host="0.0.0.0", port=8002, reload=True)
  