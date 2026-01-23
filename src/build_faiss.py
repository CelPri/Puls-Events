import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

def build_faiss_index():
    # Charger les chunks
    with open("data/events_chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    # Préparer les documents LangChain
    documents = []
    for c in chunks:
        documents.append(
            Document(
                page_content=c["text"],
                metadata={
                    "uid": c["uid"],
                    "title": c["title"],
                    "start_date": c["start_date"],
                    "end_date": c["end_date"],
                    "source": c["source"],
                    "chunk_id": c["chunk_id"],
                }
            )
        )

    # Modèle d’embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Création de l’index Faiss
    vectorstore = FAISS.from_documents(documents, embeddings)

    # Sauvegarde locale
    vectorstore.save_local("faiss_index")
    
    return vectorstore


if __name__ == "__main__":
    build_faiss_index()

print("Index Faiss créé et sauvegardé")
