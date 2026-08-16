(function () {
    "use strict";

    function escapeHtml(value) {
        return String(value || "").replace(/[&<>'"]/g, function (character) {
            return {
                "&": "&amp;",
                "<": "&lt;",
                ">": "&gt;",
                "'": "&#039;",
                '"': "&quot;",
            }[character];
        });
    }

    function updateOriginalProductCards(data) {
        if (!data.products || !data.products.length) {
            return;
        }
        var slides = document.querySelectorAll(".flash-sale-section .product-slider-7 .swiper-slide");
        data.products.slice(0, slides.length).forEach(function (product, index) {
            var slide = slides[index];
            slide.setAttribute("data-product-id", product.id);
            var cartButton = slide.querySelector(".cart-button");
            if (cartButton) cartButton.setAttribute("data-product-id", product.id);
            var imageLink = slide.querySelector(".product-image");
            var image = slide.querySelector(".product-image img");
            var nameLink = slide.querySelector(".product-content > a");
            var name = slide.querySelector(".productName");
            var price = slide.querySelector(".price");
            var sold = slide.querySelector(".sold");

            if (imageLink) imageLink.href = product.url;
            if (image) {
                image.src = product.image || image.src;
                image.alt = product.name;
            }
            if (nameLink) nameLink.href = product.url;
            if (name) name.textContent = product.name;
            if (price) {
                price.innerHTML = escapeHtml(product.price) +
                    (product.compare_at_price ? " <del>" + escapeHtml(product.compare_at_price) + "</del>" : "") +
                    (product.discount_percent && Number(product.discount_percent) > 0 ? " <span class=\"badge bg-danger\">-" + escapeHtml(product.discount_percent) + "%</span>" : "");
            }
            if (sold) sold.textContent = product.store + " · Stock: " + product.stock;
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        fetch("/home/data/", {headers: {"Accept": "application/json"}})
            .then(function (response) { return response.ok ? response.json() : null; })
            .then(function (data) { if (data) { updateOriginalProductCards(data); } })
            .catch(function () {
                // O conteúdo original do tema permanece visível quando não há dados do marketplace.
            });
    });
})();
