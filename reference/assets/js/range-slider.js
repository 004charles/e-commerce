/*=====================
    Range Slider Js
==========================*/
const minRange = document.getElementById("minRange");
const maxRange = document.getElementById("maxRange");
const minPrice = document.getElementById("min-price");
const maxPrice = document.getElementById("max-price");
const rangeFill = document.querySelector(".range-fill");

function updateRange() {
    let maxVal = parseInt(maxRange.value, 10);
    let minVal = parseInt(minRange.value, 10);
    const isRTL = document.documentElement.getAttribute("dir") === "rtl";

    if (minVal > maxVal - 500) {
        minRange.value = maxVal - 500;
        minVal = maxVal - 500;
    }

    if (maxVal < minVal + 500) {
        maxRange.value = minVal + 500;
        maxVal = minVal + 500;
    }

    minPrice.textContent = `$${minVal}`;
    maxPrice.textContent = `$${maxVal}`;

    let percent1 = (minVal / minRange.max) * 100;
    let percent2 = (maxVal / maxRange.max) * 100;

    if (isRTL) {
        rangeFill.style.right = percent1 + "%";
        rangeFill.style.left = (100 - percent2) + "%";
    } else {
        rangeFill.style.left = percent1 + "%";
        rangeFill.style.right = (100 - percent2) + "%";
    }
}

minRange.addEventListener("input", updateRange);
maxRange.addEventListener("input", updateRange);

updateRange();