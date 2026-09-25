function updateClock() {
  const now = new Date();

  let hours = now.getHours();
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const seconds = String(now.getSeconds()).padStart(2, "0");
  const ampm = hours >= 12 ? "PM" : "AM";

  hours = hours % 12 || 12;
  hours = String(hours).padStart(2, "0");

  document.getElementById("time").textContent = `${hours}:${minutes}:${seconds}`;
  document.getElementById("ampm").textContent = ampm;

  document.getElementById("date").textContent = now.toLocaleDateString(undefined, {
    weekday: "short",
    month: "short",
    day: "2-digit",
    year: "numeric"
  });
}

updateClock();
setInterval(updateClock, 1000);
