(function () {
    "use strict";

    function getCookie(name) {
        var cookies = document.cookie ? document.cookie.split(";") : [];
        for (var i = 0; i < cookies.length; i += 1) {
            var cookie = cookies[i].trim();
            if (cookie.indexOf(name + "=") === 0) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return "";
    }

    function formatPrice(value) {
        return Number(value || 0).toLocaleString("pt-PT", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }) + " Kz";
    }

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

    function post(url, data) {
        var body = new URLSearchParams(data);
        return fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
            },
            body: body,
            credentials: "same-origin",
        }).then(function (response) {
            return response.json().then(function (payload) {
                if (!response.ok || !payload.ok) {
                    throw new Error(payload.error || "Não foi possível atualizar o carrinho.");
                }
                return payload.cart;
            });
        });
    }

    function updateCartBadge(cart) {
        document.querySelectorAll("#cartOffcanvas ~ *, [href*='#cartOffcanvas'] .label span").forEach(function () {
            // The exact badge is updated below using the stable cart offcanvas trigger selector.
        });
        document.querySelectorAll("a[href*='#cartOffcanvas'] .label span").forEach(function (badge) {
            badge.textContent = cart.item_count;
        });
        document.querySelectorAll("[data-cart-count]").forEach(function (badge) {
            badge.textContent = cart.item_count;
        });
    }

    function renderCart(cart) {
        var list = document.querySelector("#cartOffcanvas .product-box-list");
        if (!list) return;
        var groups = cart.groups || [];
        var items = [];
        groups.forEach(function (group) {
            group.items.forEach(function (item) {
                items.push('<li class="vertical-product-box" data-cart-product-id="' + item.product_id + '">' +
                    '<a href="' + escapeHtml(item.url) + '" class="product-image">' +
                        '<img src="' + escapeHtml(item.image || "/assets/images/product/1.png") + '" class="img-fluid" alt="' + escapeHtml(item.name) + '">' +
                    '</a>' +
                    '<div class="product-content">' +
                        '<a href="' + escapeHtml(item.url) + '"><h5 class="name title-color">' + escapeHtml(item.name) + '</h5></a>' +
                        '<h5 class="price">' + formatPrice(item.price) + (item.original_price ? ' <del class="text-danger">' + formatPrice(item.original_price) + '</del>' : '') + (item.discount_percent && Number(item.discount_percent) > 0 ? ' <span class="badge bg-danger">-' + escapeHtml(item.discount_percent) + '%</span>' : '') + '</h5>' +
                        '<div class="quantity-box qty-container">' +
                            '<button class="btn qty-btn-minus" data-cart-action="decrease" data-product-id="' + item.product_id + '"><i class="ri-subtract-line"></i></button>' +
                            '<button class="btn btn-trash" data-cart-action="remove" data-product-id="' + item.product_id + '"><i class="ri-delete-bin-line"></i></button>' +
                            '<input type="number" name="qty" disabled class="quantity form-control input-qty" value="' + item.quantity + '">' +
                            '<button class="btn qty-btn-plus" data-cart-action="increase" data-product-id="' + item.product_id + '"><i class="ri-add-line"></i></button>' +
                        '</div>' +
                    '</div>' +
                    '<button class="btn close-button" data-cart-action="remove" data-product-id="' + item.product_id + '"><i class="ri-delete-bin-line"></i></button>' +
                '</li>');
            });
        });
        list.innerHTML = items.length ? items.join("") : '<li class="empty-cart"><svg><use xlink:href="../assets/images/inner-page/empty-cart.svg#emptyCart"></use></svg><h4>O seu carrinho está vazio.</h4></li>';
        var total = document.querySelector("#cartOffcanvas #total-price");
        if (total) total.textContent = formatPrice(cart.subtotal);
        updateCartBadge(cart);
    }

    function showMessage(message) {
        var existing = document.querySelector(".marketplace-cart-message");
        if (existing) existing.remove();
        var notice = document.createElement("div");
        notice.className = "alert alert-warning marketplace-cart-message position-fixed top-0 end-0 m-3";
        notice.style.zIndex = "2000";
        notice.textContent = message;
        document.body.appendChild(notice);
        window.setTimeout(function () { notice.remove(); }, 3500);
    }

    function refreshCart() {
        return fetch("/cart/api/", {headers: {"Accept": "application/json"}, credentials: "same-origin"})
            .then(function (response) { return response.json(); })
            .then(function (payload) {
                if (payload.ok) renderCart(payload.cart);
                return payload.cart;
            });
    }

    function addProduct(productId, quantity) {
        return post("/cart/api/add/", {product_id: productId, quantity: quantity || 1})
            .then(function (cart) {
                renderCart(cart);
                showMessage("Produto adicionado ao carrinho.");
                return cart;
            })
            .catch(function (error) { showMessage(error.message); });
    }

    document.addEventListener("DOMContentLoaded", function () {
        refreshCart().then(function () {
            var params = new URLSearchParams(window.location.search);
            var canvas = document.getElementById("cartOffcanvas");
            if (params.get("open_cart") === "1" && canvas && window.bootstrap && window.bootstrap.Offcanvas) {
                window.bootstrap.Offcanvas.getOrCreateInstance(canvas).show();
            }
        });

        document.addEventListener("click", function (event) {
            var actionButton = event.target.closest("[data-cart-action]");
            if (actionButton) {
                event.preventDefault();
                var productId = actionButton.getAttribute("data-product-id");
                var item = actionButton.closest("[data-cart-product-id]");
                var current = item ? Number(item.querySelector(".input-qty").value || 1) : 1;
                if (actionButton.dataset.cartAction === "remove") {
                    post("/cart/api/remove/", {product_id: productId}).then(renderCart).catch(function (error) { showMessage(error.message); });
                } else {
                    var next = actionButton.dataset.cartAction === "increase" ? current + 1 : current - 1;
                    post("/cart/api/update/", {product_id: productId, quantity: next}).then(renderCart).catch(function (error) { showMessage(error.message); });
                }
                return;
            }

            var cardButton = event.target.closest(".cart-button[data-product-id]");
            if (cardButton) {
                event.preventDefault();
                addProduct(cardButton.getAttribute("data-product-id"), 1);
            }
        });

        document.addEventListener("click", function (event) {
            var checkoutButton = event.target.closest(".check-out-button");
            if (checkoutButton) {
                event.preventDefault();
                window.location.href = "/orders/checkout/";
                return;
            }

            var detailButton = event.target.closest("[data-marketplace-add-to-cart]");
            if (!detailButton) return;
            event.preventDefault();
            event.stopPropagation();
            var quantityInput = document.querySelector(".quantity-box-2 .qty-input");
            addProduct(detailButton.getAttribute("data-product-id"), quantityInput ? quantityInput.value : 1);
        }, true);
    });

    window.marketplaceAddToCart = addProduct;
})();
