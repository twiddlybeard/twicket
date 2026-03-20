import os
import json
import requests
from bs4 import BeautifulSoup

EVENT_URL = "https://www.twickets.live/en/event/1989018878176403456"
SNAPSHOT_PATH = "snapshots/tickets.json"

os.makedirs("snapshots", exist_ok=True)

def fetch_listings():
    response = requests.get(EVENT_URL, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Twickets uses JS, but some listings still appear in HTML
    ticket_cards = soup.select("div.ticket-card")  # may require adapting later
    listings = []

    for card in ticket_cards:
        listings.append({
            "title": card.get_text(strip=True),
            "id": hash(card.get_text(strip=True))
        })

    return listings

def load_previous():
    if not os.path.exists(SNAPSHOT_PATH):
        return []
    with open(SNAPSHOT_PATH, "r") as f:
        return json.load(f)

def save_snapshot(listings):
    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(listings, f, indent=2)

def main():
    print("Fetching latest listings…")
    current = fetch_listings()
    previous = load_previous()

    current_ids = {l["id"] for l in current}
    previous_ids = {l["id"] for l in previous}

    new_ids = current_ids - previous_ids

    if new_ids:
        print("🎉 NEW TICKETS FOUND!")
        for listing in current:
            if listing["id"] in new_ids:
                print("👉", listing["title"])
    else:
        print("No new listings.")

    save_snapshot(current)

if __name__ == "__main__":
    main()
