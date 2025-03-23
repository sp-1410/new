from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
EVENTS_FILE = "events.json"

# Load events from JSON
def load_events():
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

# Save events to JSON
def save_events(events):
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f, indent=4)

events = load_events()  # Load events on startup

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_event", methods=["POST"])
def add_event():
    data = request.json
    if not data or "name" not in data or "date" not in data:
        return jsonify({"error": "Invalid event data"}), 400

    event = {"name": data["name"], "date": data["date"]}
    events.append(event)
    save_events(events)
    return jsonify(event)

@app.route("/get_events", methods=["GET"])
def get_events():
    today = datetime.today()
    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        event["days_left"] = (event_date - today).days
    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
