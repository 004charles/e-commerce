/*=====================
   Grid Change JS
==========================*/
document.querySelectorAll(".grid-option li").forEach(li => {
    li.addEventListener("click", () => {
        li.classList.add("active");
        li.parentElement.querySelectorAll("li").forEach(sib => {
            if (sib !== li) sib.classList.remove("active");
        });
    });
});

const safeClick = (selector, callback) => {
    const el = document.querySelector(selector);
    if (el) el.addEventListener("click", callback);
};

const setRowCols = (el, cols) => {
    if (!el) return;
    [...el.classList]
        .filter(c => c.startsWith("row-cols-"))
        .forEach(c => el.classList.remove(c));
    el.classList.add(`row-cols-${cols}`);
};

const applyGrid = (cols, extraClasses = []) => {
    const section = document.querySelector(".product-list-section");
    if (!section) return;

    section.classList.remove("list-style");
    setRowCols(section, cols);
    section.classList.add(...extraClasses);
};

safeClick(".grid-option .list-btn", () => {
    const section = document.querySelector(".product-list-section");
    if (!section) return;

    setRowCols(section, 1);
    section.classList.add("list-style");
});

safeClick(".grid-option .grid-btn", () => {
    applyGrid("xxl-4", ["row-cols-xl-3", "row-cols-lg-2", "row-cols-md-3", "row-cols-2"]);
});

safeClick(".grid-option .three-grid", () => {
    applyGrid("xl-3", ["row-cols-lg-2", "row-cols-md-3", "row-cols-2"]);
});

safeClick(".grid-option .two-grid", () => {
    applyGrid(2);
});

safeClick(".grid-option .five-grid", () => {
    applyGrid("xxl-5", ["row-cols-xl-3", "row-cols-lg-2", "row-cols-md-3", "row-cols-2"]);
});

const contentWidth = window.innerWidth || document.documentElement.clientWidth;

if (contentWidth < 1199) {
    document.querySelector(".grid-option .grid-btn")?.classList.add("active");
} else if (contentWidth < 1399) {
    document.querySelector(".grid-option .three-grid")?.classList.add("active");
}
