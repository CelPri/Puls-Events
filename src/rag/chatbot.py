import os
import json
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from src.rag.retriever import retrieve_documents

load_dotenv()

# LLM unique (utilisé pour tout)
llm = ChatMistralAI(
    api_key=os.environ.get("MISTRAL_API_KEY"),
    model_name="mistral-small-latest",
    temperature=0
)

# Prompt 1 : extraction de date (générique, sans lister les mois en Python)
date_prompt = ChatPromptTemplate.from_template(
    """Tu extrais une date depuis une question utilisateur.
Retourne UNIQUEMENT un JSON valide.

Règles :
- Si un mois et une année sont présents → retourne {{"year": "YYYY", "month": "MM"}}
- Sinon → retourne {{}}

Exemples :
"événements en août 2026" → {{"year": "2026", "month": "08"}}
"que faire à Bordeaux ?" → {{}}

Question : {question}
JSON :"""
)

# Prompt 2 : RAG final
rag_prompt = ChatPromptTemplate.from_template(
    """Tu es un assistant culturel.
Réponds UNIQUEMENT à partir du contexte fourni.
Si le contexte est vide, dis-le clairement.

Contexte :
{context}

Question :
{question}
"""
)

def filter_by_month(docs, year: str, month: str):
    start = f"{year}-{month}-01"
    end = f"{year}-{month}-31"

    return [
        d for d in docs
        if d.metadata.get("start_date") <= end
        and d.metadata.get("end_date") >= start
    ]

def answer(question: str) -> str:
    # 1. Extraction date via LLM
    date_chain = date_prompt | llm
    date_response = date_chain.invoke({"question": question})

    target = {}
    try:
        clean = date_response.content.replace("```json", "").replace("```", "").strip()
        if clean.startswith("{"):
            target = json.loads(clean)
    except Exception:
        target = {}

    # 2. Rappel large FAISS
    docs = retrieve_documents(question, k=500)

    # 3. Filtrage date si applicable
    if target.get("year") and target.get("month"):
        docs = filter_by_month(docs, target["year"], target["month"])

        if not docs:
            return f"Aucun événement trouvé pour {target['month']}/{target['year']}."

    # 4. Limiter le contexte
    docs = docs[:30]

    context = "\n\n".join(
        f"{d.metadata.get('start_date')} → {d.metadata.get('end_date')} | {d.page_content}"
        for d in docs
    )

    # 5. Génération finale
    response = (rag_prompt | llm).invoke({
        "context": context,
        "question": question
    })

    return response.content
