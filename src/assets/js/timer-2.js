/**=====================
    Timer 2 JS
==========================**/
function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 24));

    return {
        'total': t,
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    };
}

function initializeClock(className, endtime) {
    var clocks = document.querySelectorAll('.' + className);

    clocks.forEach(function (clock) {
        var daysSpan = clock.querySelector('.days');
        var hoursSpan = clock.querySelector('.hours');
        var minutesSpan = clock.querySelector('.minutes');
        var secondsSpan = clock.querySelector('.seconds');

        function updateClock() {
            var t = getTimeRemaining(endtime);

            if (daysSpan) daysSpan.innerHTML = ('0' + t.days).slice(-2);
            if (hoursSpan) hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
            if (minutesSpan) minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
            if (secondsSpan) secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

            if (t.total <= 0) {
                clearInterval(timeinterval);
                clock.classList.add('time-up');

                var randomMonths = Math.floor(Math.random() * 3) + 6;
                var now = new Date();
                var newDeadline = new Date(now.setMonth(now.getMonth() + randomMonths));

                console.log(`⏰ New random timer set for ${randomMonths} months later`);

                setTimeout(() => {
                    clock.classList.remove('time-up');
                    initializeClock(className, newDeadline);
                }, 1000);
            }
        }

        updateClock();
        var timeinterval = setInterval(updateClock, 1000);
    });
}

var randomMonths = Math.floor(Math.random() * 3) + 6;
var deadline = new Date();
deadline.setMonth(deadline.getMonth() + randomMonths);

initializeClock('clockdiv-2', deadline);
