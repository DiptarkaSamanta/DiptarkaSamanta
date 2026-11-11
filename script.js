function updateClock() {
  const now = new Date();

  // Explicitly sync and format in Indian Standard Time (IST)
  const timeFormatter = new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Kolkata",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: true
  });

  const dateFormatter = new Intl.DateTimeFormat("en-US", {
    timeZone: "Asia/Kolkata",
    weekday: "short",
    month: "short",
    day: "2-digit",
    year: "numeric"
  });

  const parts = timeFormatter.formatToParts(now);
  let hours = parts.find(p => p.type === "hour").value;
  let minutes = parts.find(p => p.type === "minute").value;
  let seconds = parts.find(p => p.type === "second").value;
  let dayPeriod = parts.find(p => p.type === "dayPeriod").value;

  const timeEl = document.getElementById("time");
  if (timeEl) {
    timeEl.textContent = `${hours}:${minutes}:${seconds} ${dayPeriod}`;
  }

  const ampmEl = document.getElementById("ampm");
  if (ampmEl) {
    ampmEl.textContent = dayPeriod;
  }

  const dateEl = document.getElementById("date");
  if (dateEl) {
    dateEl.textContent = `${dateFormatter.format(now)} (IST)`;
  }
}

updateClock();
setInterval(updateClock, 1000);
