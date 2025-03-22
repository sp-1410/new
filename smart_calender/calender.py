from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

EVENTS_FILE = "events.json"

# Load existing events from file
def load_events():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r") as f:
            return json.load(f)
    return []

# Save events to file
def save_events():
    with open(EVENTS_FILE, "w") as f:
        json.dump(events, f)

events = load_events()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_event", methods=["POST"])
def add_event():
    data = request.get_json()
    event = {"name": data["name"], "date": data["date"]}
    events.append(event)
    save_events()  # Save event to file
    return jsonify(event)

@app.route("/get_events", methods=["GET"])
def get_events():
    today = datetime.today()

    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d")
        event["days_left"] = (event_date - today).days  # ✅ Recalculate

    return jsonify(events)

if __name__ == "__main__":
    app.run(debug=True)
