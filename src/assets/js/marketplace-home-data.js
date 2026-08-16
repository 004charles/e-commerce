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

    function updateAllOriginalProductCards(data) {
        if (!data.products || !data.products.length) {
            return;
        }
        var slides = document.querySelectorAll(".product-box.productMain");
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

    function updateOriginalBannerImages(data) {
        var banners = (data.banners || []).filter(function (banner) { return banner.image; });
        if (!banners.length) return;
        var images = document.querySelectorAll(".banner-box img, .banner-box-9 img, .offer-product-box img, .menu-banner img");
        images.forEach(function (image, index) {
            var banner = banners[index];
            if (!banner) return;
            image.src = banner.image;
            image.alt = banner.title || "Marketplace Angola";
            var link = image.closest("a");
            if (link && banner.button_url) link.href = banner.button_url;
        });
    }

    function updateOriginalCategoryCards(data) {
        if (!data.categories || !data.categories.length) return;
        var cards = document.querySelectorAll(".category-box-slide .category-box");
        data.categories.slice(0, cards.length).forEach(function (category, index) {
            var card = cards[index];
            card.href = category.url;
            var image = card.querySelector("img");
            var name = card.querySelector("h4");
            if (image && category.image) {
                image.src = category.image;
                image.alt = category.name;
            }
            if (name) name.textContent = category.name;
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        fetch("/home/data/", {headers: {"Accept": "application/json"}})
            .then(function (response) { return response.ok ? response.json() : null; })
            .then(function (data) {
                if (data) {
                    updateAllOriginalProductCards(data);
                    updateOriginalCategoryCards(data);
                    updateOriginalBannerImages(data);
                }
            })
            .catch(function () {
                // O conteúdo original do tema permanece visível quando não há dados do marketplace.
            });
    });
})();
