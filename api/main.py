from fastapi import FastAPI
from pydantic import BaseModel
from src.rag.chatbot import answer
import subprocess
from fastapi import HTTPException

# Création de l'application FastAPI
app = FastAPI(title="RAG Events API")

# Modèle de données pour la requête /ask
# Attend un JSON de la forme : {"question": "..."}
class Question(BaseModel):
    question: str

# Endpoint principal : poser une question au système RAG
@app.post("/ask")
def ask(question: Question):
    # Vérification : question non vide
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

# Endpoint utilitaire : reconstruire l’index FAISS, utile si les données ont changé
@app.post("/rebuild")
def rebuild():
    subprocess.run(["python", "build_faiss.py"], check=True)
    return {"status": "FAISS index rebuilt"}

# Vérifier que l’API répond
@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint de métadonnées
@app.get("/metadata")
def metadata():
    return {
        "index_loaded": True,
        "source": "OpenAgenda",
        "zone": "Bordeaux",
        "type": "evenements culturels"
    }
