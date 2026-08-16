/*=====================
    Zoom Gallery Js
==========================*/
import lgZoom from "https://cdn.skypack.dev/lightgallery@2.0.0-beta.4/plugins/zoom";

const $lgContainer = document.getElementById("gallery-container");

const lg = lightGallery($lgContainer, {
    speed: 500,
    showZoomInOutIcons: true,
    actualSize: true,
    plugins: [lgZoom]
});