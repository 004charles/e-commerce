/* Local Iconsax bridge using the original SVG artwork bundled with the project. */
(() => {
    const initIcons = () => {
        document.querySelectorAll(".iconsax").forEach((element) => {
            const name = element.dataset.iconName?.toLowerCase().trim();
            if (!name || element.dataset.localIconLoaded === "true") return;
            element.dataset.localIconLoaded = "true";
            fetch(`/assets/svg/iconsax/${name}.svg`, { credentials: "same-origin" })
                .then((response) => {
                    if (!response.ok) throw new Error(`Icon ${name} unavailable`);
                    return response.text();
                })
                .then((svg) => {
                    element.innerHTML = svg;
                    element.setAttribute("aria-hidden", "true");
                })
                .catch(() => {
                    element.dataset.localIconLoaded = "false";
                });
        });
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initIcons, { once: true });
    } else {
        initIcons();
    }
})();
