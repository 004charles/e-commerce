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
        card.querySelectorAll("a.product-image, .product-content > a, .product-content a").forEach(function (link) {
            link.href = product.url;
        });
        card.querySelectorAll("img.productImage, .product-image img").forEach(function (image) {
            if (product.image) image.src = product.image;
            image.alt = product.name;
        });
        card.querySelectorAll(".productName, .product-content > a h3, .product-content > a h4, .product-content > a h5, .product-content .name").forEach(function (name) {
            name.textContent = product.name;
        });
        card.querySelectorAll(".price").forEach(function (price) {
            price.innerHTML = escapeHtml(product.price) +
                (product.compare_at_price ? " <del>" + escapeHtml(product.compare_at_price) + "</del>" : "") +
                (product.discount_percent && Number(product.discount_percent) > 0 ? " <span class=\"badge bg-danger\">-" + escapeHtml(product.discount_percent) + "%</span>" : "");
        });
        card.querySelectorAll("[data-product-id]").forEach(function (element) {
            element.setAttribute("data-product-id", product.id);
        });
        var sold = card.querySelector(".sold");
        if (sold) sold.textContent = product.store + " · Stock: " + product.stock;
    }

    function applyProductCards(products) {
        if (!products.length) return;
        document.querySelectorAll(".productMain.product-box-4").forEach(function (card, index) {
            applyProductCard(card, products[index % products.length]);
        });
        document.querySelectorAll(".vertical-product-box").forEach(function (card, index) {
            applyProductCard(card, products[index % products.length]);
        });
    }

    function applyRecentSearch(products) {
        if (!products.length) return;
        document.querySelectorAll(".result-list-box").forEach(function (list) {
            list.querySelectorAll("a").forEach(function (link, index) {
                var product = products[index % products.length];
                link.textContent = product.name;
                link.href = product.url;
            });
        });
        document.querySelectorAll(".search-list-box a").forEach(function (link, index) {
            var product = products[index % products.length];
            link.href = product.url;
            var image = link.querySelector("img");
            if (image && product.image) {
                image.src = product.image;
                image.alt = product.name;
            }
        });
    }

    function applyCategories(categories) {
        if (!categories.length) return;
        document.querySelectorAll(".filter-category-2 li a").forEach(function (link, index) {
            var category = categories[index % categories.length];
            link.textContent = category.name;
            link.href = category.url;
        });
        document.querySelectorAll(".category-list .category-list-box").forEach(function (box, index) {
            var category = categories[index % categories.length];
            var name = box.querySelector(".name");
            var count = box.querySelector(".number");
            if (name) name.textContent = category.name;
            if (count) count.textContent = "(" + (category.count || 0) + ")";
            var checkbox = box.querySelector("input[type=checkbox]");
            if (checkbox) {
                checkbox.value = category.url;
                checkbox.setAttribute("data-category-url", category.url);
            }
        });
        document.querySelectorAll(".category-sm-box").forEach(function (box, index) {
            var category = categories[index % categories.length];
            var link = box.querySelector("a.category-image");
            var image = box.querySelector("a.category-image img");
            var heading = box.querySelector("h4");
            if (link) link.href = category.url;
            if (image) image.alt = category.name;
            if (heading) heading.textContent = category.name;
        });
        document.querySelectorAll(".category-menu-list a.sub-category-box").forEach(function (link, index) {
            var category = categories[index % categories.length];
            link.href = category.url;
            var heading = link.querySelector("h5");
            if (heading) heading.textContent = category.name;
        });
    }

    function applyPriceRange(products) {
        if (!products.length) return;
        var values = products.map(function (product) {
            return Number(String(product.price || "").replace(/[^0-9.]/g, ""));
        }).filter(function (value) { return Number.isFinite(value) && value > 0; });
        if (!values.length) return;
        var minimum = Math.floor(Math.min.apply(Math, values));
        var maximum = Math.ceil(Math.max.apply(Math, values));
        var format = function (value) {
            return new Intl.NumberFormat("pt-PT").format(value) + " Kz";
        };
        var minLabel = document.querySelector("#min-price");
        var maxLabel = document.querySelector("#max-price");
        if (minLabel) minLabel.textContent = format(minimum);
        if (maxLabel) maxLabel.textContent = format(maximum);
        var minInput = document.querySelector("#minRange");
        var maxInput = document.querySelector("#maxRange");
        if (minInput && maxInput) {
            minInput.min = String(minimum);
            minInput.max = String(maximum);
            minInput.value = String(minimum);
            maxInput.min = String(minimum);
            maxInput.max = String(maximum);
            maxInput.value = String(maximum);
            [minInput, maxInput].forEach(function (input) {
                input.dispatchEvent(new Event("input", {bubbles: true}));
            });
            window.setTimeout(function () {
                if (minLabel) minLabel.textContent = format(minimum);
                if (maxLabel) maxLabel.textContent = format(maximum);
            }, 0);
        }
    }

    function applyCategoryMeta(data) {
        var categoryName = data.category_name || "Catálogo";
        document.title = categoryName + " | Marketplace Angola";
        document.querySelectorAll(".breadcrumb-contain h2").forEach(function (heading) {
            heading.textContent = categoryName;
        });
        var breadcrumb = document.querySelector(".breadcrumb-contain .breadcrumb-item.active");
        if (breadcrumb) breadcrumb.textContent = categoryName;
        var search = document.querySelector("#search");
        if (search) search.placeholder = "Pesquisar em " + categoryName + "...";
    }

    document.addEventListener("DOMContentLoaded", function () {
        var source = document.getElementById("catalog-page-data");
        if (!source) return;
        try {
            var data = JSON.parse(source.textContent || "{}");
            var products = data.products || [];
            applyCategoryMeta(data);
            applyPriceRange(products);
            applyProductCards(products);
            applyRecentSearch(products);
            applyCategories(data.categories || []);
        } catch (error) {
            // O template original continua disponível se os dados do catálogo não estiverem acessíveis.
        }
    });
})();
