import os
import json
import re
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from src.rag.retriever import retrieve_documents

load_dotenv()

# LLM
llm = ChatMistralAI(
    api_key=os.environ.get("MISTRAL_API_KEY"),
    model_name="mistral-small-latest",
    temperature=0
)

# Prompt 1 : extraction d’intervalle de dates
date_prompt = ChatPromptTemplate.from_template(
    """Tu extrais un intervalle de dates depuis une question utilisateur.
Retourne UNIQUEMENT un JSON valide.

Règles :
- Jour précis : start_date = end_date
- Week-end : samedi / dimanche
- Mois : premier / dernier jour
- Sinon : {{}}

Format :
{{"start_date":"YYYY-MM-DD","end_date":"YYYY-MM-DD"}}

Exemples :
"le WE du 24 janvier 2026" : {{"start_date":"2026-01-24","end_date":"2026-01-25"}}
"événements en août 2026" : {{"start_date":"2026-08-01","end_date":"2026-08-31"}}
"que faire à Bordeaux ?" : {{}}

Question : {question}
JSON :"""
)


# Prompt 2 : génération RAG finale
rag_prompt = ChatPromptTemplate.from_template(
    """Tu es un assistant culturel.
Réponds UNIQUEMENT à partir du contexte fourni.
Si aucun événement ne correspond, dis-le clairement.
Utilise des listes à puces pour présenter les événements.

Contexte :
{context}

Question :
{question}
"""
)

def answer(question: str) -> str:
    # Extraction des dates
    date_chain = date_prompt | llm
    date_response = date_chain.invoke({"question": question})
   


    try:
        json_str = re.search(r"\{.*\}", date_response.content, re.S).group()
        dates = json.loads(json_str)
    except Exception:
        dates = {}


    # Retrieval avec filtrage temporel
    docs = retrieve_documents(
        question,
        start=dates.get("start_date"),
        end=dates.get("end_date"),
        k=500
    )

    if not docs:
        return "Aucun événement ne correspond à votre recherche."

    # Limitation du contexte
    docs = docs[:30]

    context = "\n\n".join(
        f"{d.metadata.get('start_date')} → {d.metadata.get('end_date')} | {d.page_content}"
        for d in docs
    )

    # Génération finale
    response = (rag_prompt | llm).invoke({
        "context": context,
        "question": question
    })

    return response.content
