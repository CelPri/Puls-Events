import requests
import json
from datetime import datetime, timedelta


BASE_URL = "https://api.openagenda.com/v2/events"
AGENDA_UID = "ville-de-bordeaux"
API_KEY = "bb4beba0fed746f9a82473251c59085e"  

def get_date_range():
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    return one_year_ago, today

def get_events():
    start_date, end_date = get_date_range()

    params = {
        "key": API_KEY,
        "limit": 100,
        "timings[gte]": start_date.isoformat(),
        "timings[lte]": end_date.isoformat(),
    }

    response = requests.get(
        f"https://api.openagenda.com/v2/agendas/{AGENDA_UID}/events",
        params=params
    )



    response.raise_for_status()
    data = response.json()
    return data.get("events", [])




def parse_event(event):
    return {
        "title": event.get("title", {}).get("fr"),
        "description": event.get("description", {}).get("fr"),
        "start_date": event.get("firstTiming", {}).get("begin"),
        "end_date": event.get("lastTiming", {}).get("end"),
        "source": event.get("originAgenda", {}).get("title"),
        "uid": event.get("uid"),
    }

def parse_events(events):
    parsed = []
    for event in events:
        e = parse_event(event)
        if e["description"]:
            parsed.append(e)
    return parsed


def save_events(events, filename="events.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    events = get_events()
    parsed_events = parse_events(events)
    save_events(parsed_events)
    print(f"{len(parsed_events)} événements sauvegardés")


