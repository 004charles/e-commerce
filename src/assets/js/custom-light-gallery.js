/**=====================
   Custom Light Gallery JS
==========================**/
lightGallery(document.getElementById('lightgallery'), {
    selector: 'a',
    closable: true,
    zoomFromOrigin: false,
    plugins: [lgZoom, lgThumbnail],
});