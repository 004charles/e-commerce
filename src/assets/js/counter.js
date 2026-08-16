/**=====================
   Counter JS
==========================**/
const eventDate = new Date("2026-10-21T14:00:00-06:00");
const countdownElement = document.getElementById("countdown");
const daysElement = document.getElementById("days");
const hoursElement = document.getElementById("hours");
const minutesElement = document.getElementById("minutes");
const secondsElement = document.getElementById("seconds");

function updateCountdown() {
    const now = new Date();
    const difference = eventDate - now;

    if (difference <= 0) {
        clearInterval(interval);
        countdownElement.innerHTML =
            `<h2 style="font-size: 2.5rem; color: rgba(var(--primary-color), 1)">Page Ready</h2>`;
        return;
    }

    const days = Math.floor(difference / (1000 * 60 * 60 * 24));
    const hours = Math.floor(
        (difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((difference % (1000 * 60)) / 1000);

    daysElement.textContent = days;
    hoursElement.textContent = String(hours).padStart(2, "0");
    minutesElement.textContent = String(minutes).padStart(2, "0");
    secondsElement.textContent = String(seconds).padStart(2, "0");
}

const interval = setInterval(updateCountdown, 1000);
updateCountdown();