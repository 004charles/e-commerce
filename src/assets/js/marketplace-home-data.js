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

    function applyProductCard(card, product) {
        if (!card || !product) return;
        card.setAttribute("data-product-id", product.id);
        var links = card.querySelectorAll("a.product-image, .product-content > a, .product-content a, a.main-image-box");
        links.forEach(function (link) { link.href = product.url; });
        var images = card.querySelectorAll(".product-image img, a.main-image-box img, .thumbnail-image img");
        images.forEach(function (image) {
            if (product.image) image.src = product.image;
            image.alt = product.name;
        });
        var names = card.querySelectorAll(".productName, .product-content .name, .product-content > a h3, .product-content > a h4");
        names.forEach(function (name) { name.textContent = product.name; });
        var prices = card.querySelectorAll(".price");
        prices.forEach(function (price) {
            price.innerHTML = escapeHtml(product.price) +
                (product.compare_at_price ? " <del>" + escapeHtml(product.compare_at_price) + "</del>" : "") +
                (product.discount_percent && Number(product.discount_percent) > 0 ? " <span class=\"badge bg-danger\">-" + escapeHtml(product.discount_percent) + "%</span>" : "");
        });
        var sold = card.querySelector(".sold");
        if (sold) sold.textContent = product.store + " · Stock: " + product.stock;
        var status = card.querySelector(".product-rating h5 span");
        if (status) status.textContent = product.stock > 10 ? "Disponível" : "Poucas unidades";
        var cartButton = card.querySelector(".cart-button, .cart-btn, .add-to-cart-btn");
        if (cartButton) cartButton.setAttribute("data-product-id", product.id);
    }

    function updateAllOriginalProductCards(data) {
        var products = data.products || [];
        if (!products.length) return;
        document.querySelectorAll(".product-box.productMain").forEach(function (card, index) {
            applyProductCard(card, products[index % products.length]);
        });
    }

    function updateVerticalProductCards(data) {
        var products = data.products || [];
        if (!products.length) return;
        document.querySelectorAll("section .vertical-product-box").forEach(function (card, index) {
            applyProductCard(card, products[index % products.length]);
        });
    }

    function updateHotDealCards(data) {
        var products = data.products || [];
        if (!products.length) return;
        document.querySelectorAll("section .hot-deal-product-box").forEach(function (card, index) {
            applyProductCard(card, products[index % products.length]);
        });
    }

    function updateOriginalBannerImages(data) {
        var banners = (data.banners || []).filter(function (banner) { return banner.image; });
        if (!banners.length) return;
        var images = document.querySelectorAll(".banner-box img, .banner-box-9 img, .offer-product-box img, .menu-banner img");
        images.forEach(function (image, index) {
            var banner = banners[index % banners.length];
            image.src = banner.image;
            image.alt = banner.title || "Marketplace Angola";
            var link = image.closest("a");
            if (link && banner.button_url) link.href = banner.button_url;
        });
    }

    function updateOriginalCategoryCards(data) {
        var categories = data.categories || [];
        if (!categories.length) return;
        document.querySelectorAll(".category-box-slide .category-box").forEach(function (card, index) {
            var category = categories[index % categories.length];
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

    function updateHotTags(data) {
        var categories = data.categories || [];
        if (!categories.length) return;
        document.querySelectorAll(".hot-tag-list a").forEach(function (link, index) {
            var category = categories[index % categories.length];
            link.href = category.url;
            link.textContent = category.name;
        });
    }

    function updateSectionTexts(data) {
        var blocks = {};
        (data.text_blocks || []).forEach(function (block) { blocks[block.key] = block; });
        var headingKeys = {
            "Flash Sale": "flash-sale",
            "Ofertas relâmpago": "flash-sale",
            "Get it all right here": "categories",
            "Compre por categorias": "categories",
            "Recommendations": "recommendations",
            "Recomendações": "recommendations",
            "Tendências": "trending",
            "Deal hot today": "hot-deals",
            "Oferta do dia": "hot-deals",
            "Hot Tag:": "hot-tags",
            "Categorias populares": "hot-tags",
            "Don't Miss This Offers": "offers",
            "Não perca estas ofertas": "offers",
        };
        document.querySelectorAll("section").forEach(function (section) {
            section.querySelectorAll("h2, h3").forEach(function (heading) {
                var current = heading.textContent.trim();
                var key = headingKeys[current];
                var block = key ? blocks[key] : null;
                if (block && block.title) heading.textContent = block.title;
            });
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        fetch("/home/data/", {headers: {"Accept": "application/json"}, credentials: "same-origin"})
            .then(function (response) { return response.ok ? response.json() : null; })
            .then(function (data) {
                if (!data) return;
                updateAllOriginalProductCards(data);
                updateVerticalProductCards(data);
                updateHotDealCards(data);
                updateOriginalCategoryCards(data);
                updateHotTags(data);
                updateOriginalBannerImages(data);
                updateSectionTexts(data);
            })
            .catch(function () {
                // O conteúdo original do tema permanece visível quando não há dados do marketplace.
            });
    });
})();
