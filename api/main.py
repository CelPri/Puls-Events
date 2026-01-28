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

    try:
        result = answer(question.question)
        return {"answer": result}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erreur interne lors du traitement de la question."
        )

    result = answer(question.question)
    return {"answer": result}



@app.post("/rebuild")
def rebuild():
    subprocess.run(["python", "build_faiss.py"], check=True)
    return {"status": "FAISS index rebuilt"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metadata")
def metadata():
    return {
        "index_loaded": True,
        "source": "OpenAgenda",
        "zone": "Bordeaux",
        "type": "evenements culturels"
    }
