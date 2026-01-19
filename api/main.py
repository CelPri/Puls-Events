from fastapi import FastAPI
from pydantic import BaseModel
from src.rag.chatbot import answer
import subprocess
from fastapi import HTTPException

app = FastAPI(title="RAG Events API")

class Question(BaseModel):
    question: str


@app.post("/ask")
def ask(question: Question):
    if not question.question or not question.question.strip():
        raise HTTPException(
            status_code=400,
            detail="La question ne peut pas être vide."
        )

    result = answer(question.question)
    return {"answer": result}



@app.post("/rebuild")
def rebuild():
    subprocess.run(["python", "build_faiss.py"], check=True)
    return {"status": "FAISS index rebuilt"}
