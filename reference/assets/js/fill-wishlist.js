/*=====================
    Fill Wishlist Js
==========================*/
(function () {
    document.addEventListener("DOMContentLoaded", () => {
        document.addEventListener("click", (event) => {
            const target = event.target;

            if (target.classList.contains("ri-heart-3-line")) {
                target.style.display = "none";
                target.nextElementSibling.style.display = "inline";
            }

            if (target.classList.contains("ri-heart-3-fill")) {
                target.style.display = "none";
                target.previousElementSibling.style.display = "inline";
            }
        });
    });
})();
