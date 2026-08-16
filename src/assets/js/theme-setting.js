/*=====================
    Template Settings Js
==========================*/
document.addEventListener("DOMContentLoaded", () => {
    const langSwitch = document.createElement("div");
    langSwitch.className = "lang-switch";
    langSwitch.innerHTML = `
      <button id="darkBtn">Dark <i class="ri-moon-fill"></i></button>
      <button id="rtlBtn">RTL <i class="ri-text-direction-l"></i></button>
    `;
    document.body.prepend(langSwitch);

    const darkBtn = document.getElementById("darkBtn");
    const rtlBtn = document.getElementById("rtlBtn");
    const rtlLink = document.getElementById("rtl-link");

    /* Dark mode restore */
    if (localStorage.getItem("template") === "dark") {
        document.body.classList.add("dark");
        darkBtn.classList.add("active");
        darkBtn.innerHTML = `Light <i class="ri-sun-fill"></i>`;
    }

    /* RTL restore */
    if (localStorage.getItem("rtl") === "true") {
        document.documentElement.setAttribute("dir", "rtl");
        rtlLink.setAttribute("href", "../assets/css/vendors/bootstrap.rtl.css");
        rtlBtn.classList.add("active");
        rtlBtn.innerHTML = 'LTR <i class="ri-text-direction-r"></i>';
    }

    /* Dark mode toggle */
    darkBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        if (document.body.classList.contains("dark")) {
            localStorage.setItem("template", "dark");
            darkBtn.classList.add("active");
            darkBtn.innerHTML = `Light <i class="ri-sun-fill"></i>`;
        } else {
            localStorage.setItem("template", "light");
            darkBtn.classList.remove("active");
            darkBtn.innerHTML = `Dark <i class="ri-moon-fill"></i>`;
        }
    });

    /* RTL toggle */
    rtlBtn.addEventListener("click", () => {
        if (document.documentElement.getAttribute("dir") === "rtl") {
            document.documentElement.removeAttribute("dir");
            rtlLink.setAttribute("href", "../assets/css/vendors/bootstrap.css");
            localStorage.setItem("rtl", "false");
            rtlBtn.classList.remove("active");
            rtlBtn.innerHTML = `RTL <i class="ri-text-direction-l"></i>`;
        } else {
            document.documentElement.setAttribute("dir", "rtl");
            rtlLink.setAttribute("href", "../assets/css/vendors/bootstrap.rtl.css");
            localStorage.setItem("rtl", "true");
            rtlBtn.classList.add("active");
            rtlBtn.innerHTML = `LTR <i class="ri-text-direction-r"></i>`;
        }
    });
});