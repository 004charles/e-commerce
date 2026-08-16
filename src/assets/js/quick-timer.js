/*=====================
    Quick Timer Js
==========================*/
function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());

    /***** CONVERT THE TIME TO A USEABLE FORMAT *****/
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);

    /***** OUTPUT THE CLOCK DATA AS A REUSABLE OBJECT *****/
    return {
        'total': t,
        'minutes': minutes,
        'seconds': seconds
    };
}

/***** DISPLAY THE CLOCK AND STOP IT WHEN IT REACHES ZERO *****/
function initializeClock(id, endtime) {
    var clock = document.getElementById(id);
    var minutesSpan = clock.querySelector('.minutes');
    var secondsSpan = clock.querySelector('.seconds');

    function updateClock() {
        var t = getTimeRemaining(endtime);

        minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
        secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

        if (t.total <= 0) {
            clearInterval(timeinterval);
        }
    }

    updateClock();
    var timeinterval = setInterval(updateClock, 1000);
}

/***** SET A VALID END DATE *****/
var deadline = new Date(Date.parse(new Date()) + 12 * 60 * 1000);
initializeClock('quickClock', deadline);