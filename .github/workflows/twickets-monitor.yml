import os
import json
import requests

EVENT_ID = "1989018878176403456"
API_URL = f"https://www.twickets.live/api/listings?eventId={EVENT_ID}"
EVENT_URL = f"https://www.twickets.live/en/event/{EVENT_ID}"
SNAPSHOT_PATH = "snapshots/tickets.json"
TEAMS_WEBHOOK_URL = os.getenv("TEAMS_WEBHOOK_URL")

os.makedirs("snapshots", exist_ok=True)


def fetch_listings():
    """Fetch JSON listings from Twickets API (avoids Cloudflare 403)."""
    r = requests.get(API_URL, timeout=15)
    r.raise_for_status()
    data = r.json()

    listings = []
    for item in data.get("items", []):
        listings.append({
            "id": item.get("id"),
            "title": (
                f"{item.get('sectionName', '')} "
                f"{item.get('rowName', '')} "
                f"£{item.get('price', '')}".strip()
            )
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


def send_teams_message(message: str):
    if not TEAMS_WEBHOOK_URL:
        print("⚠️ TEAMS_WEBHOOK_URL not set — cannot send Teams message.")
        return

    payload = { "text": message }

    r = requests.post(TEAMS_WEBHOOK_URL, json=payload)
    if r.status_code != 200:
        print(f"❌ Failed to send Teams notification: {r.text}")
    else:
        print("📨 Sent Teams alert successfully.")


def main():
    print("Fetching latest listings…")
    current = fetch_listings()
    previous = load_previous()

    current_ids = {l["id"] for l in current}
    previous_ids = {l["id"] for l in previous}

    new_ids = current_ids - previous_ids

    if new_ids:
        print("🎉 NEW TICKETS FOUND!")

        msg = [
            "🎟 **New Twickets Tickets Found!**",
            f"Event: {EVENT_URL}",
            ""
        ]

        for listing in current:
            if listing["id"] in new_ids:
                print("👉", listing["title"])
                msg.append(f"- {listing['title']}")

        send_teams_message("\n".join(msg))
    else:
        print("No new listings.")

    save_snapshot(current)


if __name__ == "__main__":
    main()
