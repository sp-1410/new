// Function to add an event
function addEvent() {
    let name = document.getElementById("eventName").value.trim();
    let date = document.getElementById("eventDate").value;

    if (!name || !date) {
        alert("⚠️ Please enter both event name and date!");
        return;
    }

    fetch("/add_event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, date: date })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`❌ Error: ${data.error}`);
        } else {
            alert(`✅ Event "${data.name}" added!`);
            document.getElementById("eventName").value = ""; // Clear input
            document.getElementById("eventDate").value = "";
            loadEvents();  // Refresh events list
        }
    })
    .catch(error => console.error("Error adding event:", error));
}

// Function to load events
function loadEvents() {
    fetch("/get_events")
    .then(response => response.json())
    .then(events => {
        let eventList = document.getElementById("eventList");
        eventList.innerHTML = "";

        events.forEach(event => {
            let listItem = document.createElement("li");

            let daysLeft = event.days_left !== undefined ? event.days_left : "Unknown";

            listItem.innerHTML = `<strong>${event.name}</strong> - ${event.date} (${daysLeft} days left) 
                <button onclick="deleteEvent('${event.name}')">❌ Delete</button>`;

            eventList.appendChild(listItem);

            // Show an alert if deadline is close
            if (daysLeft !== "Unknown" && daysLeft <= 2) {
                alert(`⚠️ Hurry! Only ${daysLeft} days left for "${event.name}"`);
            }
        });
    })
    .catch(error => console.error("Error fetching events:", error));
}

// Function to delete an event
function deleteEvent(eventName) {
    fetch("/delete_event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: eventName })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadEvents();  // Refresh list after deletion
    })
    .catch(error => console.error("Error deleting event:", error));
}

// Call the function on page load
window.onload = loadEvents;
