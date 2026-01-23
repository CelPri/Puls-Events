from src.chunk_events import chunk_events


def test_chunk_events_returns_chunks():
    events = [
        {
            "uid": 1,
            "title": "Expo",
            "description": "Une exposition à Bordeaux." * 20,
        }
    ]

    chunks = chunk_events(events)

    assert chunks is not None
    assert len(chunks) > 0
