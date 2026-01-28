import requests
import json
from datetime import datetime, timedelta
import os

#BASE_URL = "https://api.openagenda.com/v2/events"
AGENDA_UID = "ville-de-bordeaux"
API_KEY = os.environ.get("OPENAGENDA_API_KEY")

# Calcule la date de début : aujourd’hui moins un an
# Sert à récupérer uniquement les événements récents
def get_date_range():
    today = datetime.now()
    one_year_ago = today - timedelta(days=365)
    return one_year_ago

# Récupère les événements depuis l’API OpenAgenda
def get_events():
    start_date = get_date_range()
    # Paramètres de la requête HTTP
    params = {
        "key": API_KEY,
        "limit": 200,
        "timings[gte]": start_date.isoformat(),
    }

    # Appel à l’API OpenAgenda
    response = requests.get(
        f"https://api.openagenda.com/v2/agendas/{AGENDA_UID}/events",
        params=params
    )
    # Lève une erreur si la requête HTTP échoue
    response.raise_for_status()
    # Conversion de la réponse JSON
    data = response.json()
    # Retourne uniquement la liste des événements
    return data.get("events", [])



# Applique le parsing à tous les événements
# et supprime ceux sans description
def parse_event(event):
    return {
        "title": event.get("title", {}).get("fr"),
        "description": event.get("description", {}).get("fr"),
        "start_date": event.get("firstTiming", {}).get("begin"),
        "end_date": event.get("lastTiming", {}).get("end"),
        "source": event.get("originAgenda", {}).get("title"),
        "uid": event.get("uid"),
    }
# Sauvegarde les événements nettoyés dans un fichier JSON
def parse_events(events):
    parsed = []
    for event in events:
        e = parse_event(event)
        if e["description"]:
            parsed.append(e)
    return parsed

# Point d’entrée du script
# Lance la récupération, le nettoyage et la sauvegarde
def save_events(events, filename="events.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    events = get_events()
    parsed_events = parse_events(events)
    save_events(parsed_events)
    print(f"{len(parsed_events)} événements sauvegardés")


