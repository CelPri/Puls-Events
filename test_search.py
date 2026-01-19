from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# Charger l’index
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# Test de recherche
query = "concert de jazz"
results = vectorstore.similarity_search(query, k=5)

print("Résultats :\n")
for r in results:
    print("- Texte :", r.page_content[:120], "...")
    print("  Métadonnées :", r.metadata)
    print()
