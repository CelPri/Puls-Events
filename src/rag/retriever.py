from datetime import datetime, timezone, timedelta
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def get_vectorstore():
    return FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

def retrieve_documents(question: str, k: int = 100, start=None, end=None):
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search("", k=1000)


    # 👉 Comportement AVANT : pas de dates → on ne filtre pas
    if not start or not end:
        return docs

    try:
        # bornes demandées (naïves → UTC)
        start_dt = datetime.fromisoformat(start).replace(tzinfo=timezone.utc)
        end_dt = (datetime.fromisoformat(end).replace(tzinfo=timezone.utc)+ timedelta(days=1)
)
    except Exception:
        # sécurité : si parsing raté, on ne filtre pas
        return docs

    filtered = []
    for d in docs:
        sd = d.metadata.get("start_date")
        ed = d.metadata.get("end_date")
        if not sd or not ed:
            continue

        try:
            # dates événement (aware → UTC)
            ev_start = datetime.fromisoformat(sd).astimezone(timezone.utc)
            ev_end = datetime.fromisoformat(ed).astimezone(timezone.utc)
        except Exception:
            continue

        # chevauchement temporel
        if ev_start <= end_dt and ev_end >= start_dt:
            filtered.append(d)

    return filtered
