/*=====================
    Image Change js
==========================*/
var loadFile = function (event) {
    var file = event.target.files[0];
    if (!file) return;

    var allowedTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif"];

    if (!allowedTypes.includes(file.type)) {
        alert("Only JPEG, JPG, PNG, and GIF files are allowed.");
        event.target.value = "";
        return;
    }

    if (file.size > 4 * 1024 * 1024) {
        alert("File size exceeds 4 MB. Please choose a smaller file.");
        event.target.value = "";
        return;
    }

    var image = document.getElementById("output");
    image.src = URL.createObjectURL(file);
};

