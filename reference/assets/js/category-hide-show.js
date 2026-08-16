/**=====================
   Category Hide & Show JS
==========================**/
document.addEventListener("DOMContentLoaded", function () {
    const btn = document.querySelector(".categoryButton");

    btn.addEventListener("click", function () {
        const homeSection = document.querySelector(".home-section");
        const left = homeSection.querySelector(".custom-xxl-3");
        const right = homeSection.querySelector(".col-12, .custom-xxl-9");

        if (left && right) {
            if (left.style.display === "none") {
                left.style.display = "";
                right.classList.remove("col-12");
                right.classList.add("custom-xxl-9");
                console.log("Left shown & Right normal");
            } else {
                left.style.display = "none";
                right.classList.remove("custom-xxl-9");
                right.classList.add("col-12");
                console.log("Left hidden & Right expanded");
            }
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.querySelector(".categoryButton");

    btn.addEventListener("click", function () {
        const homeSection = document.querySelector(".home-section");
        const left = homeSection.querySelector(".custom-col-xxl-3");
        const right = homeSection.querySelector(".col-12, .custom-col-xxl-9");

        if (left && right) {
            if (left.style.display === "none") {
                left.style.display = "";
                right.classList.remove("col-12");
                right.classList.add("custom-col-xxl-9");
                console.log("Left shown & Right normal");
            } else {
                left.style.display = "none";
                right.classList.remove("custom-col-xxl-9");
                right.classList.add("col-12");
                console.log("Left hidden & Right expanded");
            }
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.querySelector(".categoryButton");

    btn.addEventListener("click", function () {
        const homeSection = document.querySelector(".product-banner-section");
        const left = homeSection.querySelector(".custom-col-xxl-3");
        const right = homeSection.querySelector(".col-12, .custom-col-xxl-9");

        if (left && right) {
            if (left.style.display === "none") {
                left.style.display = "";
                right.classList.remove("col-12");
                right.classList.add("custom-col-xxl-9");
                console.log("Left shown & Right normal");
            } else {
                left.style.display = "none";
                right.classList.remove("custom-col-xxl-9");
                right.classList.add("col-12");
                console.log("Left hidden & Right expanded");
            }
        }
    });
});