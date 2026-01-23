import os
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    ContextPrecision,
    ContextRecall,
    AnswerRelevancy,
    Faithfulness,
)
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.llms import LangchainLLMWrapper
from langchain_mistralai import ChatMistralAI

from src.rag.chatbot import answer

from src.rag.retriever import retrieve_documents


# -------- LLM RAGAS --------
ragas_llm = LangchainLLMWrapper(
    ChatMistralAI(
        api_key=os.environ["MISTRAL_API_KEY"],
        model_name="mistral-small-latest",
        temperature=0,
    )
)

# -------- QUESTIONS --------
questions = [
    "Quels événements culturels ont lieu à Bordeaux ?",
    "Quels concerts ou événements de musique pop ont lieu à Bordeaux ?",
    "Quels événements sont prévus à Bordeaux le 10 décembre 2025 ?",
    "Qui a gagné la Coupe du monde de football ?",
]

ground_truths = [
    "De nombreux événements culturels ont lieu à Bordeaux, notamment des expositions, des spectacles vivants, des conférences et des ateliers artistiques tout au long de l’année.",
    "Aucun concert explicitement identifié comme de la musique pop n’est référencé dans les données OpenAgenda disponibles.",
    "Aucun événement ne débute exactement le 10 décembre 2025 à Bordeaux, mais plusieurs expositions et événements sont en cours à cette période.",
    "Cette question n’est pas liée aux événements culturels référencés dans la base OpenAgenda.",
]

# -------- ANSWERS --------
answers = [answer(q) for q in questions]


# -------- CONTEXTS (OBLIGATOIRE POUR RAGAS) --------
contexts = [
    [doc.page_content for doc in retrieve_documents(q)]
    for q in questions
]

# -------- DATASET --------
dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "contexts": contexts,
    "ground_truth": ground_truths,
})

# -------- EMBEDDINGS --------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -------- EVALUATION --------
results = evaluate(
    dataset=dataset,
    metrics=[
        ContextPrecision(llm=ragas_llm),
        ContextRecall(llm=ragas_llm),
        AnswerRelevancy(llm=ragas_llm, embeddings=embeddings),
        Faithfulness(llm=ragas_llm),
    ],
    embeddings=embeddings,
)

print(results)
