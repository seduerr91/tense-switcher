from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from persuasion_service import PERSUASION

class Message(BaseModel):
    input: str
    tense: str
    output: str = None

app = FastAPI()
persuasion = PERSUASION()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"I invented a new word.": "Plagiarism."}

@app.post("/entry/")
async def transformer(message: Message):
    message.output = str(persuasion.transformer(message.input, message.tense))
    return {"output": message.output}
