(function () {
    "use strict";

    var input = document.getElementById("searchInputBox");
    var resultBox = document.getElementById("resultBox");
    if (!input || !resultBox) return;

    var popularBox = resultBox.querySelector(".search-result-box");
    var popularList = popularBox && popularBox.querySelector(".result-list-box");
    var popularTitle = popularBox && popularBox.querySelector(".result-title h4");
    var lastBox = resultBox.querySelector(".last-search-box");
    var recentlyBox = resultBox.querySelector(".last-seen-search-box");
    var searchButton = document.querySelector(".search-button");
    var debounceTimer;
    var requestController;

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

    function price(value) {
        return Number(value || 0).toLocaleString("pt-PT", {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
        }) + " Kz";
    }

    function showOriginalSearchSections(show) {
        if (lastBox) lastBox.style.display = show ? "" : "none";
        if (recentlyBox) recentlyBox.style.display = show ? "" : "none";
    }

    function renderResults(payload) {
        if (!popularList || !popularTitle) return;
        var results = payload.results || [];
        popularTitle.textContent = payload.query ? "Resultados da pesquisa" : "Produtos populares";
        if (!payload.query) {
            showOriginalSearchSections(true);
            return;
        }
        showOriginalSearchSections(false);
        if (!results.length) {
            popularList.innerHTML = '<li class="search-no-results">Nenhum produto encontrado.</li>';
            return;
        }
        var comparisons = payload.comparisons || [];
        popularList.innerHTML = results.map(function (item, index) {
            var location = item.location || "Localização não indicada";
            var oldPrice = item.compare_at_price ? '<del>' + price(item.compare_at_price) + '</del>' : "";
            var promotionBadge = item.discount_percent && Number(item.discount_percent) > 0 ? '<span class="badge bg-danger">-' + escapeHtml(item.discount_percent) + '%</span>' : "";
            var comparison = comparisons.find(function (entry) { return entry.name === item.name; });
            var comparisonLabel = comparison ? '<small class="marketplace-search-compare">Comparar preços: ' + comparison.offers.length + ' lojas</small>' : "";
            var badge = index === 0 ? '<span class="marketplace-search-best">Menor preço</span>' : "";
            var image = item.image ? '<img src="' + escapeHtml(item.image) + '" class="img-fluid" alt="' + escapeHtml(item.name) + '">' : "";
            return '<li class="marketplace-search-result">' +
                '<a href="' + escapeHtml(item.url) + '" class="marketplace-search-result-link">' +
                    '<span class="marketplace-search-image">' + image + '</span>' +
                    '<span class="marketplace-search-info">' +
                        '<strong>' + escapeHtml(item.name) + '</strong>' +
                        '<small>Loja: ' + escapeHtml(item.store) + '</small>' +
                        '<small>Localização: ' + escapeHtml(location) + '</small>' +
                        '<span class="marketplace-search-price">' + price(item.price) + ' ' + oldPrice + ' ' + promotionBadge + '</span>' +
                        comparisonLabel +
                        badge +
                    '</span>' +
                '</a>' +
            '</li>';
        }).join("");
    }

    function search(query) {
        var normalized = String(query || "").trim();
        if (requestController) requestController.abort();
        if (normalized.length < 2) {
            renderResults({query: "", results: []});
            return;
        }
        requestController = new AbortController();
        fetch("/home/search/?q=" + encodeURIComponent(normalized), {
            headers: {"Accept": "application/json"},
            credentials: "same-origin",
            signal: requestController.signal,
        })
            .then(function (response) { return response.json(); })
            .then(renderResults)
            .catch(function (error) {
                if (error.name !== "AbortError") {
                    renderResults({query: normalized, results: []});
                }
            });
    }

    input.addEventListener("input", function () {
        window.clearTimeout(debounceTimer);
        debounceTimer = window.setTimeout(function () { search(input.value); }, 220);
    });

    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            var query = input.value.trim();
            if (query) window.location.href = "/catalog/?q=" + encodeURIComponent(query);
        }
    });

    if (searchButton) {
        searchButton.addEventListener("click", function (event) {
            event.preventDefault();
            var query = input.value.trim();
            if (query) window.location.href = "/catalog/?q=" + encodeURIComponent(query);
        });
    }
})();
