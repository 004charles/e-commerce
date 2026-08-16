/*=====================
    Load More Js
==========================*/
document.addEventListener("DOMContentLoaded", function () {
    const cols = document.querySelectorAll(".product-list-section .col");
    const loadMoreBtn = document.getElementById("loadMoreBtn");

    let visibleCount = 14;
    const increment = 5;

    cols.forEach((col, i) => {
        col.style.display = i < visibleCount ? "block" : "none";
    });

    loadMoreBtn.addEventListener("click", function () {
        visibleCount += increment;
        cols.forEach((col, i) => {
            if (i < visibleCount) {
                col.style.display = "block";
            }
        });

        if (visibleCount >= cols.length) {
            loadMoreBtn.disabled = true;
            loadMoreBtn.innerText = "All Products Loaded";
        }
    });
});