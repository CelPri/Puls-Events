import json


def chunk_events(events):
    """
    Découpe les événements en chunks simples.
    Fonction testable unitairement.
    """
    chunks = []
    for i, event in enumerate(events):
        if event.get("description"):
            chunks.append({
                "uid": event.get("uid"),
                "text": event.get("description"),
                "start_date": event.get("start_date"),
                "end_date": event.get("end_date"),
                "title": event.get("title"),
                "source": event.get("source"),
                "chunk_id": i,   # nécessaire pour build_faiss.py
            })
    return chunks


if __name__ == "__main__":
    # Chargement des événements nettoyés
    with open("data/events.json", "r", encoding="utf-8") as f:
        events = json.load(f)

    # Découpage en chunks
    chunks = chunk_events(events)

    # Sauvegarde des chunks
    with open("data/events_chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"{len(chunks)} chunks générés")
