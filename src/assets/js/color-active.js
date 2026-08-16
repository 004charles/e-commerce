/**=====================
   Color Active JS
==========================**/
document.querySelectorAll(".color-box-list li .btn").forEach(function (button) {
    button.addEventListener("click", function () {
        this.classList.toggle("active");
    });
});


document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.option-box .select-btn').forEach(function (button) {
        button.addEventListener("click", function () {
            document.querySelector('.select-option-box').classList.add("show");
        });
    });

    document.querySelectorAll('.close-btn').forEach(function (closeBtn) {
        closeBtn.addEventListener("click", function () {
            document.querySelector('.select-option-box').classList.remove("show");
        });
    });
});