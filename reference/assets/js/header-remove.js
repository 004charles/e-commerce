/*=====================
    Header Banner Remove Js
==========================*/
let topHeaderBanner = document.querySelector(".top-header-banner");
let bannerRemove = document.querySelector(".banner-remove");

bannerRemove.onclick = function () {
    topHeaderBanner.style.display = "none";
};