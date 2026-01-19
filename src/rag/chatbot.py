from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from src.rag.retriever import retrieve_documents
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatMistralAI(
    api_key=os.environ.get("MISTRAL_API_KEY"),
    model_name="mistral-small-latest",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_template(
    """Tu es un assistant culturel. Reponds à partir des elements suivants 

Contexte :
{context}

Question :
{question}
"""
)

def answer(question: str):
    docs = retrieve_documents(question)
    context = "\n".join([d.page_content for d in docs])

    chain = prompt | llm
    return chain.invoke({
        "context": context,
        "question": question
    })

def ask_rag(question: str) -> str:
    response = answer(question)

    # LangChain renvoie souvent un objet Message
    if hasattr(response, "content"):
        return response.content

    return str(response)
