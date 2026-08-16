(function () {
    "use strict";

    var translations = {
        "my account": "A minha conta",
        "account": "A minha conta",
        "contact us": "Contactos",
        "contact us": "Contactos",
        "blog": "Ajuda",
        "wishlist": "Favoritos",
        "cart": "Carrinho",
        "log in": "Entrar",
        "all category": "Todas as categorias",
        "laptop": "Computadores portáteis",
        "camera": "Câmaras",
        "device": "Dispositivos",
        "watch": "Relógios",
        "beauty": "Beleza",
        "headphone": "Auscultadores",
        "furniture": "Mobiliário",
        "movie & tv": "Filmes e TV",
        "music": "Música",
        "electronic": "Eletrónica",
        "grocery": "Mercearia",
        "man's fashion": "Moda masculina",
        "woman's fashion": "Moda feminina",
        "baby": "Bebé",
        "health & wellness": "Saúde e bem-estar",
        "auto & tires": "Automóvel e pneus",
        "household essentials": "Essenciais para casa",
        "toys": "Brinquedos",
        "sport & outdoor": "Desporto e exterior",
        "top 20": "Mais vendidos",
        "best rated": "Melhor avaliados",
        "editor's choices": "Escolhas da plataforma",
        "recommendations": "Recomendações",
        "flash sale": "Promoção relâmpago",
        "contact info": "Informações de contacto",
        "information": "Informações",
        "our services": "Nossos serviços",
        "get shopping app": "Aplicação móvel",
        "offer": "Promoções",
        "search": "Pesquisa",
        "faq's": "Perguntas frequentes",
        "mobile phones": "Telemóveis",
        "television": "Televisores",
        "washing machine": "Máquinas de lavar",
        "women fashion": "Moda feminina",
        "my shop": "A minha loja",
        "checkout": "Finalizar compra",
        "tracking order": "Acompanhar pedido",
        "functionalities": "Serviços",
        "features": "Serviços",
        "pages": "Informações",
        "popular product": "Produtos populares",
        "last search": "Pesquisas recentes",
        "remove all": "Limpar tudo",
        "recently viewed": "Vistos recentemente",
        "shop by categories": "Comprar por categorias",
        "home": "Início",
        "shop": "Catálogo",
        "product": "Produtos",
        "features": "Funcionalidades",
        "pages": "Páginas",
        "seller": "Vendedor",
        "shop grid": "Todos os produtos",
        "shop collection": "Categorias",
        "shop left sidebar": "Catálogo",
        "shop right sidebar": "Catálogo",
        "shop list infinite": "Catálogo",
        "shop banner": "Promoções",
        "shop category": "Categorias",
        "shop full width": "Catálogo",
        "shop list": "Lista de produtos",
        "shop recent view": "Vistos recentemente",
        "product page": "Página de produto",
        "product variants": "Variações de produto",
        "product features": "Funcionalidades do produto",
        "product thumbnail": "Detalhe do produto",
        "product image": "Imagens do produto",
        "product slider": "Galeria do produto",
        "product sticky": "Detalhe do produto",
        "product full width": "Detalhe do produto",
        "product simple": "Produto",
        "product classified": "Produto",
        "product review": "Avaliações",
        "product bundle": "Conjuntos de produtos",
        "product zoom": "Ampliar produto",
        "product light zoom": "Galeria ampliada",
        "product sticky checkout": "Comprar agora",
        "wishlist & compare": "Favoritos e comparação",
        "top selling product": "Produtos mais vendidos",
        "order tracking": "Acompanhar pedido",
        "add to cart": "Adicionar ao carrinho",
        "newsletter": "Novidades",
        "exit": "Sair",
        "daily deals": "Ofertas do dia",
        "top promotions": "Principais promoções",
        "now trending": "Tendências",
        "mobiles, computers": "Telemóveis e computadores",
        "mobiles, laptop": "Telemóveis e computadores",
        "tv, appliances, electronics": "TV, eletrodomésticos e eletrónica",
        "men's fashion": "Moda masculina",
        "women's fashion": "Moda feminina",
        "home, kitchen, pets": "Casa, cozinha e animais",
        "beauty, health, grocery": "Beleza, saúde e mercearia",
        "sports, fitness, bags, luggage": "Desporto, fitness e acessórios",
        "toys, baby products, kid's fashion": "Brinquedos, bebés e moda infantil",
        "car, motorbike, industrial": "Automóvel, motos e indústria",
        "free returns. standard shipping orders $99+": "Entrega em Angola. Preços e stock atualizados."
    };

    var routeByLabel = {
        "a minha conta": "/account/profile/",
        "a minha loja": "/stores/dashboard/",
        "finalizar compra": "/orders/checkout/",
        "contactos": "/#contactos",
        "ajuda": "/#contactos",
        "favoritos": "/#wishlist",
        "carrinho": "/?open_cart=1",
        "entrar": "/?open_auth=1",
        "início": "/",
        "catálogo": "/catalog/",
        "produtos": "/catalog/",
        "categorias": "/catalog/",
        "promoções": "/catalog/?promotions=1",
        "vendedor": "/stores/apply/",
        "minha conta": "/account/profile/",
        "serviços": "/catalog/",
        "informações": "/#contactos",
        "ver todas as ofertas": "/catalog/",
        "acompanhar pedido": "/account/orders/",
        "avaliacoes": "/catalog/"
    };

    function normalize(value) {
        return String(value || "").replace(/\s+/g, " ").trim().toLowerCase();
    }

    function translateText(element) {
        if (!element) return;
        var original = normalize(element.textContent);
        var translated = translations[original];
        if (!translated) return;
        var textNodes = Array.from(element.childNodes).filter(function (node) {
            return node.nodeType === Node.TEXT_NODE && normalize(node.textContent);
        });
        if (textNodes.length) {
            textNodes[0].textContent = translated;
            textNodes.slice(1).forEach(function (node) { node.textContent = ""; });
        } else if (element.children.length === 0) {
            element.textContent = translated;
        }
    }

    function updateLink(link) {
        var originalHref = link.getAttribute("href") || "";
        var hasIcon = !!link.querySelector("i, svg, [data-icon-name]");
        var isInteractiveControl = link.id === "searchClick" || link.hasAttribute("data-bs-toggle") || /Offcanvas|Modal/.test(originalHref);
        if (isInteractiveControl || (hasIcon && !normalize(link.textContent))) return;
        var labelElement = link.querySelector("span, h3, h4, h5") || link;
        translateText(labelElement);
        var label = normalize(labelElement.textContent);
        if (routeByLabel[label]) link.href = routeByLabel[label];

        var oldHref = link.getAttribute("href") || "";
        if (/\.html(?:#|$)/i.test(oldHref)) {
            if (/shop|category|collection/i.test(oldHref)) link.href = "/catalog/";
            else if (/product/i.test(oldHref)) link.href = "/catalog/";
            else if (/user-dashboard|account/i.test(oldHref)) link.href = "/account/profile/";
            else if (/cart/i.test(oldHref)) link.href = "/?open_cart=1";
            else if (/wishlist/i.test(oldHref)) link.href = "/#wishlist";
            else if (/contact/i.test(oldHref)) link.href = "/#contactos";
            else if (/blog|faq/i.test(oldHref)) link.href = "/#contactos";
            else if (/search/i.test(oldHref)) link.href = "/catalog/";
            else if (/checkout/i.test(oldHref)) link.href = "/orders/checkout/";
            else if (/order-tracking|tracking/i.test(oldHref)) link.href = "/account/orders/";
        }
    }

    function hideRedundantLinks() {
        var seen = {};
        var mainAllowed = {produtos: true, lojas: true, promoções: true, categorias: true, vendedor: true, ajuda: true};
        document.querySelectorAll(".demo-list, .demo-list li").forEach(function (item) {
            item.style.display = "none";
            item.setAttribute("aria-hidden", "true");
        });
        document.querySelectorAll(".nav-header a.login-btn, .main-header a.login-btn").forEach(function (link) {
            var item = link.closest("li");
            if (item) item.style.display = "none";
        });
        document.querySelectorAll(".nav-header .navbar-nav > li").forEach(function (item) {
            var directLink = item.querySelector(":scope > a");
            if (!directLink) return;
            var label = normalize(directLink.textContent);
            if (!mainAllowed[label] || seen[label]) {
                item.style.display = "none";
                item.setAttribute("aria-hidden", "true");
            } else {
                seen[label] = true;
            }
        });
        document.querySelectorAll(".top-header a, .nav-header a, .category-menu-list a, footer a").forEach(function (link) {
            var label = normalize(link.textContent);
            var href = normalize(link.getAttribute("href"));
            var isBlog = label.indexOf("blog") !== -1 || href.indexOf("blog") !== -1;
            var isDemoPage = /shop-grid|shop-collection|shop-right|shop-list|shop-banner|shop-category|shop-full|product-|index-[2-6]|coming-soon|user-dashboard|wishlist\.html|cart\.html/.test(href);
            var isDuplicatePromotion = label === "promoções" && seen[label];
            if (isBlog || isDemoPage || isDuplicatePromotion) {
                var item = link.closest("li");
                if (item) {
                    item.style.display = "none";
                    item.setAttribute("aria-hidden", "true");
                } else {
                    link.style.display = "none";
                }
                return;
            }
            if (label) seen[label] = true;
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        document.querySelectorAll("a").forEach(updateLink);
        document.querySelectorAll(".header-logo, .sub-footer-logo").forEach(function (link) { link.href = "/"; });
        document.querySelectorAll("a").forEach(function (link) {
            var label = normalize(link.textContent);
            if (label === "log in") {
                link.textContent = "Entrar";
                link.href = "/?open_auth=1";
            }
            if (["aud", "eur", "cny"].indexOf(label) !== -1) {
                var currencyItem = link.closest("li");
                if (currencyItem) currencyItem.style.display = "none";
            }
            var languageOrCurrency = /^english|^france|^germany|^chinese|1$/.test(link.id || "");
            var iconOrControl = !!link.querySelector("i, svg, [data-icon-name]") || link.id === "searchClick" || link.hasAttribute("data-bs-toggle") || /Offcanvas|Modal/.test(link.getAttribute("href") || "");
            if (!languageOrCurrency && !iconOrControl && link.getAttribute("href") === "index.html#!") {
                link.href = "/catalog/";
            }
            if (languageOrCurrency) link.href = "#";
        });
        hideRedundantLinks();
        document.querySelectorAll(".middle-content span, .result-title h4, .dropdown-title h4, .menu-title h3, .menu-title h4, .footer-title h4, .footer-title-2 h4, .tab-title, .nav-tabs button, #pills-top-tabe, #pills-rate-tabe, #pills-choice-tabe").forEach(translateText);
        document.querySelectorAll(".navbar-toggler + a, .category-button span").forEach(translateText);
    });
})();
