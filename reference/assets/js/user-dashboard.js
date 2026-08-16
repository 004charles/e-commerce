/*=====================
    user Dashboard Js
==========================*/
document.addEventListener("DOMContentLoaded", function () {
    const listItems = document.querySelectorAll("li[data-class]");

    listItems.forEach((item) => {
        item.addEventListener("click", function () {
            const dataClass = item.getAttribute("data-class");

            const button = document.querySelector(
                `button[data-bs-target="#${dataClass}"]`);

            if (button) {
                button.click();
            }
        });
    });
});

const dashboardLeftSidebar = document.querySelector(".dashboard-left-sidebar");
const bgOverlay = document.querySelector(".bg-overlay");
const leftDashboardShow = document.querySelector(".left-dashboard-show");
const sidebarClose = document.querySelector(".sidebar-close");

leftDashboardShow.addEventListener("click", () => {
    dashboardLeftSidebar.classList.add("show");
    bgOverlay.classList.add("show");
});

sidebarClose.addEventListener("click", () => {
    dashboardLeftSidebar.classList.remove("show");
    bgOverlay.classList.remove("show");
});
bgOverlay.addEventListener("click", () => {
    dashboardLeftSidebar.classList.remove("show");
    bgOverlay.classList.remove("show");
});