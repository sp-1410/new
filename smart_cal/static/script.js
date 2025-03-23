function loadEvents() {
    fetch("/get_events")
    .then(response => response.json())
    .then(events => {
        let eventList = document.getElementById("eventList");
        eventList.innerHTML = "";

        events.forEach(event => {
            let listItem = document.createElement("li");

            let daysLeft = event.days_left !== undefined ? event.days_left : "Unknown";

            listItem.innerHTML = `<strong>${event.name}</strong> - ${event.date} (${daysLeft} days left)`;
            eventList.appendChild(listItem);

            // Highlight urgent events
            if (daysLeft <= 2) {
                listItem.classList.add("urgent");
                alert(`⚠️ Hurry! Only ${daysLeft} days left for "${event.name}"`);
            }
        });
    })
    .catch(error => console.error("Error fetching events:", error));
}

function addEvent() {
    let name = document.getElementById("eventName").value;
    let date = document.getElementById("eventDate").value;

    if (!name || !date) {
        alert("Please enter both an event name and date.");
        return;
    }

    fetch("/add_event", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name: name, date: date })
    })
    .then(response => response.json())
    .then(data => {
        alert(`Event "${data.name}" added successfully!`);
        loadEvents();
    })
    .catch(error => console.error("Error adding event:", error));
}

// Load events on page load
window.onload = loadEvents;
