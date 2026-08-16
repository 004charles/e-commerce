/*====================
    LazyLoad Js
=======================*/
window.addEventListener("load", () => {
    const images = document.querySelectorAll("img");

    images.forEach(img => {
        img.classList.add("loaded");
    });
});