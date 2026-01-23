from src.fetch_openagenda import parse_events


def test_parse_events_filters_events_without_description():
    raw_events = [
        {
            "uid": 1,
            "title": {"fr": "Expo"},
            "description": {"fr": "Une exposition à Bordeaux"},
            "firstTiming": {"begin": "2025-11-20"},
            "lastTiming": {"end": "2025-11-21"},
            "originAgenda": {"title": "Ville de Bordeaux"},
        },
        {
            "uid": 2,
            "title": {"fr": "Concert"},
            "description": {"fr": None},  # ← doit être filtré
        },
    ]

    parsed = parse_events(raw_events)

    assert len(parsed) == 1
    assert parsed[0]["uid"] == 1
