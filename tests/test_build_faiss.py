import json
import os
import shutil
from src.build_faiss import build_faiss_index


def test_build_faiss_index_runs():
    # Créer un faux fichier events_chunks.json
    fake_chunks = [
        {
            "uid": 1,
            "text": "Une exposition à Bordeaux",
            "title": "Expo",
            "start_date": "2025-01-01",
            "end_date": "2025-01-02",
            "source": "Test",
            "chunk_id": 0
        }
    ]

    with open("data/events_chunks.json", "w", encoding="utf-8") as f:
        json.dump(fake_chunks, f)

    # Lancer la fonction
    vectorstore = build_faiss_index()
    assert vectorstore is not None

    # Nettoyage
    os.remove("data/events_chunks.json")
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")
