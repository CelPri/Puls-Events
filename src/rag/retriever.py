from datetime import datetime, timezone, timedelta
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from dateutil import parser



# Modèle d'embeddings utilisé pour interroger l'index FAISS
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Charge l'index FAISS sauvegardé localement.
def get_vectorstore(): 
    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
#Récupère les documents depuis FAISS. Si une période est fournie, applique un filtrage temporel.
def retrieve_documents(question: str, k: int = 100, start=None, end=None):
    vectorstore = get_vectorstore()
    if start and end:
        docs = vectorstore.similarity_search("", k=1000)
    else:
        docs = vectorstore.similarity_search(question, k=k)


    # Si pas de dates demandées, on retourne directement
    if not start or not end:
        return docs

    try:
        # Conversion des dates demandées en UTC
        start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
        end_dt = datetime.fromisoformat(end).replace(
            tzinfo=timezone.utc
        ) + timedelta(days=1)

    except Exception:
        # si parsing raté, on ne filtre pas
        return docs

    filtered = []

    for d in docs:
        sd = d.metadata.get("start_date")
        ed = d.metadata.get("end_date")
       


        if not sd or not ed:
            continue

        try:
            ev_start = parser.isoparse(sd).astimezone(timezone.utc)
            ev_end = parser.isoparse(ed).astimezone(timezone.utc)
        except Exception:
            continue


        # chevauchement temporel
        if ev_start <= end_dt and ev_end >= start_dt:
            filtered.append(d)

    return filtered
