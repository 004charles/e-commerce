/**=====================
   Cookie JS
==========================**/
document.addEventListener("DOMContentLoaded", function () {
    const cookieBox = document.querySelector(".cookie");
    const allowBtn = document.querySelector(".allow-btn");
    const declineBtn = document.querySelector(".decline-btn");

    if (localStorage.getItem("cookieAction")) {
        cookieBox.classList.add("hide");
    }

    function hideCookie(action) {
        cookieBox.classList.add("hide");
        localStorage.setItem("cookieAction", action);
    }

    if (allowBtn) {
        allowBtn.addEventListener("click", function () {
            hideCookie("allow");
        });
    }

    if (declineBtn) {
        declineBtn.addEventListener("click", function () {
            hideCookie("decline");
        });
    }
});
