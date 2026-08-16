(() => {
    const languages = [
        { code: "pt", label: "Por" },
        { code: "en", label: "Eng" },
        { code: "zh-hans", label: "中" },
        { code: "es", label: "Esp" },
        { code: "fr", label: "Fr" },
    ];

    const translations = {
        pt: {
            search: "Estou a procurar...",
            home: "Início",
            shop: "Loja",
            product: "Produto",
            sales: "Promoções",
            features: "Funcionalidades",
            pages: "Páginas",
            seller: "Vendedor",
            blog: "Blog",
            recent: "Vistos recentemente",
            account: "A minha conta",
            contact: "Contactos",
            callNow: "Ligue agora",
            shipping: "DEVOLUÇÕES GRATUITAS. ENVIO STANDARD EM PEDIDOS SUPERIORES A 99 €",
            ending: "Termina em:",
            hotItems: "Produtos em destaque, preços acessíveis, atualizações diárias.",
            wishlist: "Favoritos",
            cart: "Carrinho",
            login: "Entrar",
            flashSale: "Promoção relâmpago",
            seeDeals: "Ver todas as ofertas",
            popular: "Produtos populares",
            category: "Todas as categorias",
            shopByCategories: "Comprar por categorias",
            allCategory: "Todas as categorias",
            popular: "Produtos populares",
            recommendations: "Recomendações",
            topKitchen: "Melhores produtos para a cozinha",
            topTech: "Melhores produtos tecnológicos",
            topAppliances: "Melhores eletrodomésticos",
            topTrending: "Tendências",
        },
        en: {
            search: "I'm searching for...",
            home: "Home",
            shop: "Shop",
            product: "Product",
            sales: "Sales",
            features: "Features",
            pages: "Pages",
            seller: "Seller",
            blog: "Blog",
            recent: "Recent Viewer",
            account: "My Account",
            contact: "Contact Us",
            callNow: "Call us now",
            shipping: "FREE RETURNS. STANDARD SHIPPING ORDERS $99+",
            ending: "Ending in:",
            hotItems: "Hot items, Affordable price, Daily updates.",
            wishlist: "Wishlist",
            cart: "Cart",
            login: "Log In",
            flashSale: "Flash Sale",
            seeDeals: "See all deals",
            popular: "Popular Product",
            category: "All Category",
            shopByCategories: "Shop By Categories",
            allCategory: "All Category",
            popular: "Popular Product",
            recommendations: "Recommendations",
            topKitchen: "Top Kitchen items",
            topTech: "Top Tech items",
            topAppliances: "Top Kitchen Appliances",
            topTrending: "Top Trending",
        },
        "zh-hans": {
            search: "搜索商品...",
            home: "首页",
            shop: "商店",
            product: "商品",
            sales: "促销",
            features: "功能",
            pages: "页面",
            seller: "卖家",
            blog: "博客",
            recent: "最近浏览",
            account: "我的账户",
            contact: "联系我们",
            callNow: "联系我们",
            shipping: "免费退货。订单满99美元标准配送",
            ending: "结束于：",
            hotItems: "热门商品，实惠价格，每日更新。",
            wishlist: "收藏",
            cart: "购物车",
            login: "登录",
            flashSale: "限时优惠",
            seeDeals: "查看全部优惠",
            popular: "热门商品",
            category: "全部分类",
            shopByCategories: "按类别购物",
            allCategory: "全部分类",
            popular: "热门商品",
            recommendations: "推荐",
            topKitchen: "热门厨房用品",
            topTech: "热门科技产品",
            topAppliances: "热门厨房电器",
            topTrending: "热门趋势",
        },
        es: {
            search: "Estoy buscando...",
            home: "Inicio",
            shop: "Tienda",
            product: "Producto",
            sales: "Ofertas",
            features: "Funciones",
            pages: "Páginas",
            seller: "Vendedor",
            blog: "Blog",
            recent: "Vistos recientemente",
            account: "Mi cuenta",
            contact: "Contacto",
            callNow: "Llámanos ahora",
            shipping: "DEVOLUCIONES GRATUITAS. ENVÍO ESTÁNDAR EN PEDIDOS SUPERIORES A 99 €",
            ending: "Termina en:",
            hotItems: "Productos destacados, precios asequibles, actualizaciones diarias.",
            wishlist: "Favoritos",
            cart: "Carrito",
            login: "Iniciar sesión",
            flashSale: "Oferta relámpago",
            seeDeals: "Ver todas las ofertas",
            popular: "Productos populares",
            category: "Todas las categorías",
            shopByCategories: "Comprar por categorías",
            allCategory: "Todas las categorías",
            popular: "Productos populares",
            recommendations: "Recomendaciones",
            topKitchen: "Principales artículos de cocina",
            topTech: "Principales productos tecnológicos",
            topAppliances: "Principales electrodomésticos",
            topTrending: "Tendencias",
        },
        fr: {
            search: "Je recherche...",
            home: "Accueil",
            shop: "Boutique",
            product: "Produit",
            sales: "Promotions",
            features: "Fonctionnalités",
            pages: "Pages",
            seller: "Vendeur",
            blog: "Blog",
            recent: "Vus récemment",
            account: "Mon compte",
            contact: "Contact",
            callNow: "Appelez maintenant",
            shipping: "RETOURS GRATUITS. LIVRAISON STANDARD POUR LES COMMANDES DE PLUS DE 99 €",
            ending: "Se termine dans :",
            hotItems: "Articles populaires, prix abordables, mises à jour quotidiennes.",
            wishlist: "Favoris",
            cart: "Panier",
            login: "Se connecter",
            flashSale: "Vente flash",
            seeDeals: "Voir toutes les offres",
            popular: "Produits populaires",
            category: "Toutes les catégories",
            shopByCategories: "Acheter par catégorie",
            allCategory: "Toutes les catégories",
            popular: "Produits populaires",
            recommendations: "Recommandations",
            topKitchen: "Meilleurs articles de cuisine",
            topTech: "Meilleurs produits technologiques",
            topAppliances: "Meilleurs appareils de cuisine",
            topTrending: "Tendances",
        },
    };

    const staticLabels = {
        pt: {
            "Product review": "Avaliação do produto",
            "Product bundle": "Conjunto de produtos",
            "Product zoom": "Zoom do produto",
            "Wishlist & compare": "Favoritos e comparar",
            "Top Selling Product": "Produto mais vendido",
            "Add to Cart": "Adicionar ao carrinho",
            Newsletter: "Newsletter",
            "Become a Seller": "Torne-se vendedor",
            "Seller grid": "Lojas em grelha",
            "read more": "ler mais",
            "Shop Now": "Comprar agora",
            "In Stock": "Em stock",
            "Few Stock": "Pouco stock",
            "Subscribe to our newsletter": "Subscreva a nossa newsletter",
            "Subscribe Now!": "Subscrever agora!",
            "Contact Info": "Informações de contacto",
            Information: "Informações",
            "Our Services": "Os nossos serviços",
            "My Cart": "O meu carrinho",
            "My Wishlist": "Os meus favoritos",
            "Shopping Cart": "Carrinho de compras",
            "View Cart": "Ver carrinho",
            "Read cookies policies.": "Ler a política de cookies.",
            Decline: "Recusar",
            Allow: "Aceitar",
            "Clear All": "Limpar tudo",
            Categories: "Categorias",
            "Search ..": "Pesquisar...",
            Price: "Preço",
            Color: "Cor",
            "Customer Review": "Avaliações dos clientes",
            Discount: "Desconto",
            "Upto 5% (06)": "Até 5% (06)",
            "5% - 10% (08)": "5% - 10% (08)",
            "10% - 15% (10)": "10% - 15% (10)",
            "15% - 25% (14)": "15% - 25% (14)",
            "More Than 25% (13)": "Mais de 25% (13)",
            "Sort By": "Ordenar por",
            Latest: "Mais recentes",
            Popular: "Mais populares",
            "Low - High": "Preço: menor para maior",
            "High - Low": "Preço: maior para menor",
            "No Products Found": "Nenhum produto encontrado",
            "Upto 5% (06)": "Até 5% (06)",
            "upto 5% (06)": "até 5% (06)",
            "upto 5%": "até 5%",
            "More than 25% (13)": "Mais de 25% (13)",
            "More than 25%": "Mais de 25%",
            "more than 25% (13)": "mais de 25% (13)",
            "more than 25%": "mais de 25%",
        },
        en: {},
        "zh-hans": {
            "Product review": "商品评价",
            "Product bundle": "商品套装",
            "Product zoom": "商品缩放",
            "Wishlist & compare": "收藏与比较",
            "Top Selling Product": "热销商品",
            "Add to Cart": "加入购物车",
            Newsletter: "新闻通讯",
            "Become a Seller": "成为卖家",
            "Seller grid": "卖家网格",
            "read more": "阅读更多",
            "Shop Now": "立即购买",
            "In Stock": "有库存",
            "Few Stock": "库存不足",
            "Subscribe to our newsletter": "订阅我们的新闻通讯",
            "Subscribe Now!": "立即订阅！",
            "Contact Info": "联系信息",
            Information: "信息",
            "Our Services": "我们的服务",
            "My Cart": "我的购物车",
            "My Wishlist": "我的收藏",
            "Shopping Cart": "购物车",
            "View Cart": "查看购物车",
            Decline: "拒绝",
            Allow: "允许",
            "Clear All": "清除全部",
            Categories: "分类",
            "Search ..": "搜索...",
            Price: "价格",
            Color: "颜色",
            "Customer Review": "客户评价",
            Discount: "折扣",
            "Sort By": "排序",
            Latest: "最新",
            Popular: "热门",
            "Low - High": "价格从低到高",
            "High - Low": "价格从高到低",
            "No Products Found": "未找到商品",
        },
        es: {
            "Product review": "Reseña del producto",
            "Product bundle": "Conjunto de productos",
            "Product zoom": "Zoom del producto",
            "Wishlist & compare": "Favoritos y comparar",
            "Top Selling Product": "Producto más vendido",
            "Add to Cart": "Añadir al carrito",
            Newsletter: "Boletín",
            "Become a Seller": "Hazte vendedor",
            "Seller grid": "Tiendas en cuadrícula",
            "read more": "leer más",
            "Shop Now": "Comprar ahora",
            "In Stock": "En stock",
            "Few Stock": "Poco stock",
            "Subscribe to our newsletter": "Suscríbete a nuestro boletín",
            "Subscribe Now!": "¡Suscribirse ahora!",
            "Contact Info": "Información de contacto",
            Information: "Información",
            "Our Services": "Nuestros servicios",
            "My Cart": "Mi carrito",
            "My Wishlist": "Mis favoritos",
            "Shopping Cart": "Carrito de compra",
            "View Cart": "Ver carrito",
            Decline: "Rechazar",
            Allow: "Aceptar",
            "Clear All": "Borrar todo",
            Categories: "Categorías",
            "Search ..": "Buscar...",
            Price: "Precio",
            Color: "Color",
            "Customer Review": "Opiniones de clientes",
            Discount: "Descuento",
            "Sort By": "Ordenar por",
            Latest: "Más recientes",
            Popular: "Más populares",
            "Low - High": "Precio: menor a mayor",
            "High - Low": "Precio: mayor a menor",
            "No Products Found": "No se encontraron productos",
        },
        fr: {
            "Product review": "Avis sur le produit",
            "Product bundle": "Ensemble de produits",
            "Product zoom": "Zoom du produit",
            "Wishlist & compare": "Favoris et comparer",
            "Top Selling Product": "Produit le plus vendu",
            "Add to Cart": "Ajouter au panier",
            Newsletter: "Newsletter",
            "Become a Seller": "Devenir vendeur",
            "Seller grid": "Boutiques en grille",
            "read more": "lire la suite",
            "Shop Now": "Acheter maintenant",
            "In Stock": "En stock",
            "Few Stock": "Stock limité",
            "Subscribe to our newsletter": "Abonnez-vous à notre newsletter",
            "Subscribe Now!": "S'abonner maintenant !",
            "Contact Info": "Coordonnées",
            Information: "Informations",
            "Our Services": "Nos services",
            "My Cart": "Mon panier",
            "My Wishlist": "Mes favoris",
            "Shopping Cart": "Panier",
            "View Cart": "Voir le panier",
            Decline: "Refuser",
            Allow: "Accepter",
            "Clear All": "Tout effacer",
            Categories: "Catégories",
            "Search ..": "Rechercher...",
            Price: "Prix",
            Color: "Couleur",
            "Customer Review": "Avis clients",
            Discount: "Réduction",
            "Sort By": "Trier par",
            Latest: "Plus récents",
            Popular: "Plus populaires",
            "Low - High": "Prix croissant",
            "High - Low": "Prix décroissant",
            "No Products Found": "Aucun produit trouvé",
        },
    };
    staticLabels.en = Object.fromEntries(Object.keys(staticLabels.pt).map((key) => [key, key]));

    const replaceStaticText = (language) => {
        const labels = staticLabels[language] || staticLabels.pt;
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const textNodes = [];
        while (walker.nextNode()) textNodes.push(walker.currentNode);
        textNodes.forEach((node) => {
            const source = node.nodeValue.trim();
            if (!source || !labels[source]) return;
            node.nodeValue = node.nodeValue.replace(source, labels[source]);
        });
    };

    const readCookie = (name) => document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`))?.[1] || "";
    const currentLanguage = () => languages.some((item) => item.code === readCookie("marketplace_language"))
        ? readCookie("marketplace_language")
        : "pt";

    const csrfToken = () => decodeURIComponent(readCookie("csrftoken"));

    const applyText = (selector, value) => {
        document.querySelectorAll(selector).forEach((element) => {
            if (element.children.length === 0) element.textContent = value;
        });
    };

    const createLanguageMenu = (language) => {
        const button = document.querySelector("#select-language");
        const menu = button?.closest(".dropdown")?.querySelector(".dropdown-menu");
        if (!menu) return;
        const entries = [...menu.querySelectorAll("li")];
        while (entries.length < languages.length) {
            const item = document.createElement("li");
            item.innerHTML = '<a class="dropdown-item" href="#"><span></span></a>';
            menu.appendChild(item);
            entries.push(item);
        }
        languages.forEach((item, index) => {
            const link = entries[index].querySelector("a");
            if (!link) return;
            link.dataset.marketplaceLanguage = item.code;
            link.removeAttribute("onclick");
            link.querySelector("span").textContent = item.label;
        });
        const selected = languages.find((item) => item.code === language) || languages[0];
        button.querySelector("span").textContent = selected.label;
    };

    const applyTranslations = (language) => {
        const t = translations[language] || translations.pt;
        document.documentElement.lang = language;
        document.querySelector("#searchInputBox")?.setAttribute("placeholder", t.search);
        document.querySelectorAll("#search, input[placeholder='Search ..']").forEach((element) => { element.setAttribute("placeholder", t.search); });
        document.querySelector("#select-language1 span")?.replaceChildren(document.createTextNode("AOA"));
        applyText(".right-header .content-list li:nth-child(1) a", t.account);
        applyText(".right-header .content-list li:nth-child(2) a", t.contact);
        document.querySelectorAll(".category-button span").forEach((element) => { element.textContent = t.shopByCategories; });
        document.querySelectorAll(".product-link").forEach((element) => { if (element.textContent.trim() === "Recent Viewer") element.textContent = t.recent; });
        document.querySelectorAll(".contact-list h5").forEach((element) => { if (element.textContent.trim() === "Call us now") element.textContent = t.callNow; });
        document.querySelectorAll(".middle-header span").forEach((element) => { if (element.textContent.includes("FREE RETURNS")) element.textContent = t.shipping; });
        document.querySelectorAll("body *").forEach((element) => {
            const text = element.textContent.trim();
            if (text === "Ending in :") element.textContent = t.ending;
            if (text === "Hot items, Affordable price, Daily updates.") element.textContent = t.hotItems;
        });
        applyText(".right-header .content-list li:nth-child(4) a", t.wishlist);
        applyText(".right-header .content-list li:nth-child(5) a", t.cart);
        applyText(".right-header .content-list li:nth-child(6) a", t.login);
        const navItems = [t.home, t.shop, t.product, t.sales, t.features, t.pages, t.seller, t.blog];
        document.querySelectorAll(".navbar-nav > li > a.nav-link").forEach((element, index) => {
            if (navItems[index]) element.textContent = navItems[index];
        });
        applyText(".category-menu span, .category-menu button span", t.shopByCategories);
        document.querySelectorAll(".header-nav-middle span").forEach((element) => {
            if (element.textContent.trim() === "Shop By Categories") element.textContent = t.shopByCategories;
            if (element.textContent.trim() === "Recent Viewer") element.textContent = t.recent;
        });
        document.querySelectorAll("button, a, h3, h4, h5").forEach((element) => {
            const text = element.textContent.trim();
            if (text === "All Category") element.textContent = t.allCategory;
            if (text === "Popular Product") element.textContent = t.popular;
            if (text === "Recommendations") element.textContent = t.recommendations;
            if (text === "Top Kitchen items") element.textContent = t.topKitchen;
            if (text === "Top Tech items") element.textContent = t.topTech;
            if (text === "Top Kitchen Appliances") element.textContent = t.topAppliances;
            if (text === "Top Trending") element.textContent = t.topTrending;
            if (text === "See all deals") element.textContent = t.seeDeals;
        });
        createLanguageMenu(language);
        replaceStaticText(language);
    };

    window.setLanguage = (language) => {
        if (!languages.some((item) => item.code === language)) return;
        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/i18n/setlang/";
        form.innerHTML = `
            <input type="hidden" name="language" value="${language}">
            <input type="hidden" name="next" value="${window.location.pathname}${window.location.search}">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken()}">
        `;
        document.body.appendChild(form);
        form.submit();
    };

    document.addEventListener("click", (event) => {
        const link = event.target.closest("[data-marketplace-language]");
        if (!link) return;
        event.preventDefault();
        window.setLanguage(link.dataset.marketplaceLanguage);
    });

    const init = () => applyTranslations(currentLanguage());
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init, { once: true });
    else init();
})();
