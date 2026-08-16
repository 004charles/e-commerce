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

    function applySettings(settings) {
        if (!settings) return;
        if (settings.site_name) document.title = settings.site_name;
        var shipping = document.querySelector(".top-header .middle-header .middle-content p span");
        if (shipping && settings.shipping_message) shipping.textContent = settings.shipping_message;

        document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
            if (settings.support_phone) {
                link.href = "tel:" + settings.support_phone.replace(/[^+\d]/g, "");
                var headings = link.querySelectorAll("h4, h5");
                var heading = headings[headings.length - 1];
                if (heading) heading.textContent = settings.support_phone;
            }
        });
        document.querySelectorAll('a[href^="mailto:"]').forEach(function (link) {
            if (settings.support_email) {
                link.href = "mailto:" + settings.support_email;
                var text = link.querySelector("h5");
                if (text) text.textContent = settings.support_email;
            }
        });

        var newsletterTitle = document.querySelector(".newsletter-section .newsletter-content h3");
        var newsletterDescription = document.querySelector(".newsletter-section .newsletter-content h4");
        if (newsletterTitle && settings.newsletter_title) newsletterTitle.textContent = settings.newsletter_title;
        if (newsletterDescription && settings.newsletter_description) newsletterDescription.textContent = settings.newsletter_description;

        ["facebook_url", "instagram_url", "twitter_url", "whatsapp_url"].forEach(function (key) {
            if (!settings[key]) return;
            var network = key.replace("_url", "");
            document.querySelectorAll('a[href*="' + network + '"]').forEach(function (link) {
                link.href = settings[key];
            });
        });
    }

    function applyLinks(links) {
        if (!links || !links.length) return;
        var groups = {
            top: links.filter(function (link) { return link.placement === "top"; }),
            header: links.filter(function (link) { return link.placement === "header"; }),
            category: links.filter(function (link) { return link.placement === "category"; }),
            footer: links.filter(function (link) { return link.placement === "footer"; }),
        };
        function update(selector, values) {
            if (!values.length) return;
            document.querySelectorAll(selector).forEach(function (link, index) {
                var item = values[index];
                if (!item) return;
                link.href = item.url;
                var label = link.querySelector("span") || link;
                if (label.childElementCount === 0) label.textContent = item.label;
            });
        }
        update(".right-header .content-list > li > a", groups.top);
        update(".nav-header .navbar-nav > li > a", groups.header);
        update(".category-menu-list .top-menu-list > li > a", groups.category);
        update("footer .footer-list a", groups.footer);
    }

    function applyTextBlocks(blocks) {
        (blocks || []).forEach(function (block) {
            if (block.key === "newsletter") {
                var title = document.querySelector(".newsletter-section .newsletter-content h3");
                var subtitle = document.querySelector(".newsletter-section .newsletter-content h4");
                if (title) title.textContent = block.title;
                if (subtitle && block.subtitle) subtitle.textContent = block.subtitle;
            }
        });
    }

    document.addEventListener("DOMContentLoaded", function () {
        fetch("/home/site-data/", {headers: {"Accept": "application/json"}, credentials: "same-origin"})
            .then(function (response) { return response.ok ? response.json() : null; })
            .then(function (payload) {
                if (!payload) return;
                applySettings(payload.settings);
                applyLinks(payload.links);
                applyTextBlocks(payload.text_blocks);
            })
            .catch(function () {
                // O conteúdo original permanece visível se a configuração não estiver disponível.
            });
    });
})();
