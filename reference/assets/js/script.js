/*-----------------------------------------------------------------------------------

 Template Name: Kartify
 Template URI: themes.pixelstrap.com/Kartify
 Description: This is E-commerce website
 Author: Pixelstrap
 Author URI: https://themeforest.net/user/pixelstrap

-----------------------------------------------------------------------------------

01. Tap To Tap Js
02. Sub Dropdown Menu Js
03. Sticky Header Js
04. Dropdown Filter Js
05. Ratio Js
06. Onclick Link Add & Remove Js
07. Open Search Bar Js
08. Wishlist Box Remove Js
09. Change Website Title Js
10. Switch Authentication Js
11. Open Select Option Js
12. Change Text Js
13. Size List Active Add & Remove Js
14. Open Search Box Suggestion Js
15. Empty Cart Js
16. Disable Inspect Js
17. Quantity Js
18. Page Load Newsletter Modal Js
19. Exit Modal Open Js
20. Random Timer On Exit Modal Js
21. Page Loader Js
22. Recent Product Show Js
*/

/*====================
    01. Tap To Tap Js
=======================*/
var scrollToTopBtn = document.querySelector(".tap-top-button");
var rootElement = document.documentElement;

function handleScroll() {
    var scrollTotal = rootElement.scrollHeight - rootElement.clientHeight;
    if (rootElement.scrollTop / scrollTotal > 0.1) {
        scrollToTopBtn.classList.add("show");
    } else {
        scrollToTopBtn.classList.remove("show");
    }
}

function scrollToTop() {
    rootElement.scrollTo({
        top: 0,
        behavior: "smooth",
    });
}
scrollToTopBtn.addEventListener("click", scrollToTop);
document.addEventListener("scroll", handleScroll);

/*====================
    02. Sub Dropdown Menu Js
=======================*/
const subButtons = document.querySelectorAll(".sub-dropdown-hover .dropdown-item");

subButtons.forEach((btn) => {
    btn.addEventListener("click", function (e) {
        e.preventDefault();

        const parentItem = this.closest(".dropdown-item");

        parentItem.classList.toggle("show");
    });
});

/*====================
    03. Sticky Header Js
=======================*/
const header = document.querySelector("header");
const toggleClass = "sticky-header";

window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll > 300) {
        header.classList.add(toggleClass);
    } else {
        header.classList.remove(toggleClass);
    }
});

/*====================
    04. Dropdown Filter Js
=======================*/
document.querySelectorAll(".dropdown-box .dropdown-menu a").forEach(function (element) {
    element.addEventListener("click", function (event) {
        var a = event.target.closest("a");
        var getSampling = a.textContent;
        var dropdownToggle = event.target.closest(".dropdown-menu").previousElementSibling;
        dropdownToggle.querySelector("span").textContent = getSampling;
    });
});

/*====================
    05. Ratio Js
=======================*/
window.addEventListener("load", () => {
    const bgImg = document.querySelectorAll(".bg-img");
    for (i = 0; i < bgImg.length; i++) {
        let bgImgEl = bgImg[i];
        if (bgImgEl.classList.contains("bg-top")) {
            bgImgEl.parentNode.classList.add("b-top");
        } else if (bgImgEl.classList.contains("bg-bottom")) {
            bgImgEl.parentNode.classList.add("b-button");
        } else if (bgImgEl.classList.contains("bg-center")) {
            bgImgEl.parentNode.classList.add("b-center");
        } else if (bgImgEl.classList.contains("bg-left")) {
            bgImgEl.parentNode.classList.add("b-left");
        } else if (bgImgEl.classList.contains("bg-right")) {
            bgImgEl.parentNode.classList.add("b-right");
        }

        if (bgImgEl.classList.contains("blur-up")) {
            bgImgEl.parentNode.classList.add("blur-up", "lazyload");
        }

        if (bgImgEl.classList.contains("bg_size_content")) {
            bgImgEl.parentNode.classList.add("b_size_content");
        }

        bgImgEl.parentNode.classList.add("bg-size");
        const bgSrc = bgImgEl.src;
        bgImgEl.style.display = "none";
        bgImgEl.parentNode.setAttribute(
            "style",
            `
            background-image: url(${bgSrc});
            background-size:cover;
            background-position: center;
            background-repeat: no-repeat;
            display: block;
        `
        );
    }
});

/*====================
    06. Onclick Link Add & Remove Js
=======================*/
const shopBtns = document.querySelectorAll(".shopBtn");

shopBtns.forEach((btn) => {
    btn.dataset.originalId = btn.getAttribute("id");
    btn.dataset.originalTarget = btn.getAttribute("data-bs-target");
});

function updateOnclick() {
    shopBtns.forEach((btn) => {
        if (window.innerWidth < 1200) {
            btn.setAttribute("onclick", "location.href='shop-left-sidebar.html';");

            btn.removeAttribute("id");
            btn.removeAttribute("data-bs-toggle");
            btn.removeAttribute("data-bs-target");
            btn.removeAttribute("aria-selected");
            btn.removeAttribute("role");
            btn.removeAttribute("tabindex");
        } else {
            btn.removeAttribute("onclick");

            btn.setAttribute("id", btn.dataset.originalId);
            btn.setAttribute("data-bs-toggle", "tab");
            btn.setAttribute("data-bs-target", btn.dataset.originalTarget);
            btn.setAttribute("aria-selected", "false");
            btn.setAttribute("role", "tab");
            btn.setAttribute("tabindex", "-1");
        }
    });
}

updateOnclick();

window.addEventListener("resize", updateOnclick);

/*====================
    07. Open Search Bar Js
=======================*/
const div = document.getElementById("searchOffcanvas");
const searchOverlay = document.getElementById("searchOverlay");
const addBtn = document.getElementById("searchClick");
const removeBtn = document.getElementById("close-btn");
const resultBox = document.getElementById("resultBox");

addBtn.addEventListener("click", () => {
    div.classList.add("show");
    searchOverlay.classList.add("show");
    resultBox.classList.add("show");
});

removeBtn.addEventListener("click", () => {
    resultBox.classList.remove("show");
    div.classList.remove("show");
    searchOverlay.classList.remove("show");
});

searchOverlay.addEventListener("click", () => {
    resultBox.classList.remove("show");
    div.classList.remove("show");
    removeBtn.classList.remove("show");
});

/*=====================
    08. Wishlist Box Remove Js
==========================*/
const productList = document.querySelector('.wishlist-offcanvas .product-box-list');

productList.addEventListener('click', function (event) {
    const btn = event.target.closest('.wishlist-btn');
    if (!btn) return;

    const li = btn.closest('li');
    if (!li) return;

    const remainingItems = productList.querySelectorAll('.wishlist-offcanvas .product-box-list li');
    const isLastItem = remainingItems.length === 1;

    li.remove();

    if (isLastItem) {
        const noData = document.createElement('li');
        noData.innerHTML = `
      <div class="no-data" id="noDataContainer">
        <svg>
          <use xlink:href="../assets/images/wishlist-no-data.svg#no-data"></use>
        </svg>
          <p>No products in the wishlist.</p>
      </div>
  `;
        productList.appendChild(noData);
    }
});

function checkEmptyList() {
    const productList = document.querySelector(".product-box-list");
    const emptyMessage = document.querySelector(".empty-message");

    if (productList.children.length === 0) {
        productList.style.display = "none";
        emptyMessage.style.display = "block";
    } else {
        productList.style.display = "block";
        emptyMessage.style.display = "none";
    }
}

/* remove logic */
document.querySelectorAll(".close-button").forEach((btn) => {
    btn.addEventListener("click", function () {
        const li = this.closest("li");
        if (li) {
            li.remove();
            checkEmptyList();
        }
    });
});

checkEmptyList();

/*=====================
    09. Change Website Title Js
==========================*/
var title = document.title;

window.addEventListener("focus", function () {
    document.title = title;
});

window.addEventListener("blur", function () {
    document.title = "Come Back :(";
});

let accordionEnabled = false;

function enableAccordion() {
    const footerTitle = document.querySelectorAll(".footer-title");
    const footerLists = document.querySelectorAll(".footer-list");

    footerTitle.forEach(function (title) {
        if (!title.querySelector(".according-menu")) {
            const span = document.createElement("span");
            span.className = "according-menu float-end";
            span.innerHTML = '<i class="ri-arrow-down-s-line"></i>';
            title.querySelector("h4").appendChild(span);

            title.addEventListener("click", function () {
                footerTitle.forEach(function (item) {
                    item.classList.remove("active");
                    const span = item.querySelector(".according-menu");
                    if (span) span.innerHTML = '<i class="ri-arrow-down-s-line"></i>';
                    if (item.nextElementSibling) item.nextElementSibling.style.display = "none";
                });

                const nextElement = this.nextElementSibling;
                if (nextElement && (nextElement.style.display === "none" || nextElement.style.display === "")) {
                    this.classList.add("active");
                    const span = this.querySelector(".according-menu");
                    if (span) span.innerHTML = '<i class="ri-arrow-up-s-line"></i>';
                    nextElement.style.display = "flex";
                } else if (nextElement) {
                    const span = this.querySelector(".according-menu");
                    if (span) span.innerHTML = '<i class="ri-arrow-down-s-line"></i>';
                    nextElement.style.display = "none";
                }
            });
        }
    });

    footerLists.forEach(list => (list.style.display = "none"));
    accordionEnabled = true;
}

function disableAccordion() {
    const footerTitle = document.querySelectorAll(".footer-title");
    const footerLists = document.querySelectorAll(".footer-list");

    footerTitle.forEach(function (title) {
        title.classList.remove("active");
        const span = title.querySelector(".according-menu");
        if (span) span.remove();
    });

    footerLists.forEach(list => list.style.removeProperty("display"));
    accordionEnabled = false;
}

function handleFooter() {
    if (window.innerWidth <= 575) {
        if (!accordionEnabled) enableAccordion();
    } else {
        if (accordionEnabled) disableAccordion();
    }
}

handleFooter();

window.addEventListener("resize", handleFooter);

/*=====================
    10. Switch Authentication Js
==========================*/
let myPopup = document.querySelector(".login-box");
let btnClose = document.querySelector(".next-button");
let myPopup2 = document.querySelector(".signup-box");
let btnClose2 = document.querySelector(".next-button2");
let authForgotPass = document.querySelector(".forgot-password-box");
let forgotBtn = document.querySelector(".forgot-pass");
let cancelBtn = document.querySelector(".cancel-btn");
let signupBtn = document.querySelectorAll(".signup-btn");

setTimeout(poPup, 2000);
setTimeout(poPup2, 2000);

function poPup() {
    if (myPopup) myPopup.style.display = "block";
    if (myPopup2) myPopup2.style.display = "none";
    if (authForgotPass) authForgotPass.style.display = "none";
}

if (btnClose) {
    btnClose.onclick = function () {
        authForgotPass.style.display = "none";
        myPopup.style.display = "none";
        myPopup2.style.display = "block";
    };
}

function poPup2() {
    if (authForgotPass) authForgotPass.style.display = "none";
    if (myPopup) myPopup.style.display = "block";
    if (myPopup2) myPopup2.style.display = "none";
}

if (btnClose2) {
    btnClose2.onclick = function () {
        authForgotPass.style.display = "none";
        myPopup.style.display = "block";
        myPopup2.style.display = "none";
    };
}

if (forgotBtn) {
    forgotBtn.onclick = function () {
        authForgotPass.style.display = "block"
        myPopup.style.display = "none";
        myPopup2.style.display = "none";
    };
}

if (cancelBtn) {
    cancelBtn.onclick = function () {
        authForgotPass.style.display = "none"
        myPopup.style.display = "block";
        myPopup2.style.display = "none";
    };
}

if (signupBtn) {
    signupBtn.forEach((btn) => {
        btn.onclick = function () {
            authForgotPass.style.display = "none"
            myPopup.style.display = "none";
            myPopup2.style.display = "block";
        };
    });
}

let loginBtn = document.querySelectorAll(".login-btn");
if (loginBtn) {
    loginBtn.forEach((btn) => {
        btn.onclick = function () {
            authForgotPass.style.display = "none"
            myPopup.style.display = "block";
            myPopup2.style.display = "none";
        };
    });
}

/*=====================
    11. Open Select Option Js
==========================*/
const viewBtns = document.querySelectorAll(".select-btn");
const selectBoxes = document.querySelectorAll(".select-option-box");
const closeBtns = document.querySelectorAll(".close-btn");

viewBtns.forEach((viewBtn, index) => {
    viewBtn.addEventListener("click", () => {
        selectBoxes[index].classList.add("show");
    });
});

closeBtns.forEach((closeBtn, index) => {
    closeBtn.addEventListener("click", () => {
        selectBoxes[index].classList.remove("show");
    });
});

/*=====================
    12. Change Text Js
==========================*/
const changeTexts = document.querySelectorAll(".add-cart-btn");

changeTexts.forEach((changeText) => {
    changeText.addEventListener("click", function () {
        changeText.textContent = "Added Cart";
        changeText.classList.add("show");
    });
});

/*=====================
    13. Size List Active Add & Remove Js
==========================*/
const productBoxes = document.querySelectorAll(".product-box-4-main");

productBoxes.forEach((box, index) => {
    const sizeLinks = box.querySelectorAll(".size-list li a");
    const savedSize = localStorage.getItem(`product-${index}-size`);

    if (savedSize) {
        sizeLinks.forEach((l) => {
            if (l.textContent.trim() === savedSize) {
                l.classList.add("active");
            }
        });
    }

    sizeLinks.forEach((link) => {
        link.addEventListener("click", function (e) {
            e.preventDefault();

            sizeLinks.forEach((l) => l.classList.remove("active"));

            this.classList.add("active");

            localStorage.setItem(`product-${index}-size`, this.textContent.trim());
        });
    });
});

/*=====================
    14. Open Search Box Suggestion Js
==========================*/
const searchInputBox = document.getElementById("searchInputBox");
const resultBox1 = document.getElementById("resultBox");
const overlay = document.getElementById("searchOverlay");

searchInputBox.addEventListener("click", () => {
    resultBox1.classList.add("show");
    overlay.classList.add("show");
});

overlay.addEventListener("click", () => {
    resultBox1.classList.remove("show");
    overlay.classList.remove("show");
});

/*=====================
    15. Empty Cart Js
==========================*/
function CheckProductQuantity() {
    let AllProducts = document.getElementsByClassName("table-row");
    if (AllProducts.length === 0) {
        document.querySelector(".empty-card").classList.add("show");
    }
}

const product_details = document.getElementsByClassName("table-row");
const product_details_array = Array.from(product_details);

product_details_array.forEach((item) => {
    let DeleteButton = item.querySelector(".remove-row");
    DeleteButton.addEventListener("click", (event) => {
        item.remove();
        CheckProductQuantity();
    });
});

/*=====================
    16. Disable Inspect Js
==========================*/
document.addEventListener("contextmenu", (e) => e.preventDefault());

/* Disable specific keys */
document.onkeydown = function (e) {
    /* F12 */
    if (e.keyCode == 123) {
        return false;
    }
    /* Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C */
    if (e.ctrlKey && e.shiftKey && (e.keyCode == 73 || e.keyCode == 74 || e.keyCode == 67)) {
        return false;
    }
    /* Ctrl+U (View Source) */
    if (e.ctrlKey && e.keyCode == 85) {
        return false;
    }
};

/* Detect if DevTools open */
(function () {
    let devtoolsOpen = false;
    const element = new Image();
    Object.defineProperty(element, "id", {
        get: function () {
            devtoolsOpen = true;
            alert("Developer Tools are disabled 🚫");
            window.location.href = "about:blank";
        }
    });
    setInterval(function () {
        devtoolsOpen = false;
        console.log(element);
        if (devtoolsOpen) {
            /* extra safety */
            window.location.href = "about:blank";
        }
    }, 1000);
})();

/*=====================
    17. Quantity Js
==========================*/
document.addEventListener("DOMContentLoaded", function () {
    const qtyContainers = document.querySelectorAll(".quantity-box-2");

    qtyContainers.forEach(container => {
        const minusBtn = container.querySelector(".qty-btn-minus");
        const plusBtn = container.querySelector(".qty-btn-plus");
        const input = container.querySelector(".input-qty");

        if (!input) return;

        function toggleMinus() {
            if (parseInt(input.value, 10) <= parseInt(input.min || 0, 10)) {
                minusBtn.disabled = true;
            } else {
                minusBtn.disabled = false;
            }
        }

        toggleMinus();

        minusBtn.addEventListener("click", () => {
            let value = parseInt(input.value, 10) || 0;
            if (value > parseInt(input.min || 0, 10)) {
                input.value = value - 1;
            }
            toggleMinus();
        });

        plusBtn.addEventListener("click", () => {
            let value = parseInt(input.value, 10) || 0;
            input.value = value + 1;
            toggleMinus();
        });
    });
});


/*=====================
    18. Page Load Newsletter Modal Js
==========================*/
document.addEventListener("DOMContentLoaded", function () {
    if (!localStorage.getItem("modalShown")) {
        var myModal = new bootstrap.Modal(document.getElementById('newsletterModal'));
        myModal.show();
        localStorage.setItem("modalShown", "true");
    }
});

/*====================
    19. Exit Modal Open js
=======================*/
document.addEventListener("DOMContentLoaded", function () {
    const exitModalEl = document.getElementById("exitModal");
    const exitModal = new bootstrap.Modal(exitModalEl);

    if (!localStorage.getItem("exitModalShown")) {
        document.addEventListener("mouseout", function (e) {
            if (e.clientY <= 0) {
                exitModal.show();
                localStorage.setItem("exitModalShown", "true");
            }
        });
    }
});

/*====================
    20. Random Timer On Exit Modal Js
=======================*/
window.onload = function () {
    let minMinutes = 10;
    let maxMinutes = 30;

    let randomMinutes = Math.floor(Math.random() * (maxMinutes - minMinutes + 1)) + minMinutes;

    let remaining = randomMinutes * 60;

    let minutesEl = document.getElementById("minutes");
    let secondsEl = document.getElementById("seconds");

    updateDisplay(remaining);
    let timer = setInterval(() => {
        remaining--;
        updateDisplay(remaining);

        if (remaining <= 0) {
            clearInterval(timer);
        }
    }, 1000);

    function updateDisplay(seconds) {
        let m = Math.floor(seconds / 60);
        let s = seconds % 60;

        let minStr = (m < 10 ? "0" + m : "" + m);
        let secStr = (s < 10 ? "0" + s : "" + s);

        minutesEl.innerHTML = "";
        secondsEl.innerHTML = "";

        minStr.split("").forEach(digit => {
            let span = document.createElement("span");
            span.innerText = digit;
            minutesEl.appendChild(span);
        });

        secStr.split("").forEach(digit => {
            let span = document.createElement("span");
            span.innerText = digit;
            secondsEl.appendChild(span);
        });
    }
}

/*====================
    21. Page Loader Js
=======================*/
const loadingText = new SplitType(".loading-text.initial", {
    types: "chars"
});
const completeText = new SplitType(".loading-text.complete", {
    types: "chars"
});

gsap.set(".loading-text.complete", {
    y: "100%"
});
gsap.set(loadingText.chars, {
    opacity: 0,
    y: 100
});
gsap.set(completeText.chars, {
    opacity: 0,
    y: 100
});

gsap.to(loadingText.chars, {
    opacity: 1,
    y: 0,
    duration: 0.5,
    stagger: 0.05,
    ease: "power2.out"
});

const colorStages = [{
    bg: "rgb(230, 231, 233)",
    text: "rgba(32, 44, 60)",
    bar: "rgba(32, 44, 60)"
},
{
    bg: "rgba(135,135,135)",
    text: "rgba(255, 255, 255)",
    bar: "rgba(255, 255, 255)"
},
{
    bg: "rgb(35, 47, 62)",
    text: "rgb(221, 221, 221)",
    bar: "rgb(221, 221, 221)"
},
{
    bg: "rgb(54, 70, 83)",
    text: "rgb(255, 255, 255)",
    bar: "rgb(255, 255, 255)"
}
];

let currentStage = 0;

function updateColors(progress) {
    const stage = Math.floor(progress / 25);
    if (stage !== currentStage && stage < colorStages.length) {
        currentStage = stage;

        const {
            bg,
            text,
            bar
        } = colorStages[stage];

        gsap.to(".preloader", {
            backgroundColor: bg,
            duration: 0.6,
            ease: "power3.out"
        });

        gsap.to(".preloader-progress-bar", {
            backgroundColor: bar,
            duration: 0.6,
            ease: "power2.inOut"
        });

        gsap.to(".loading-text .char, .percentage", {
            color: text,
            duration: 0.6,
            ease: "power2.inOut"
        });
    }
}

// Logic for "Real" Progress
let progressProxy = {
    value: 0
};
const percentageEl = document.querySelector(".percentage");

function updateUI(val) {
    const progress = Math.round(val);
    if (percentageEl) percentageEl.textContent = progress;
    document.querySelector(".preloader-progress-bar").style.width = progress + "%";
    updateColors(progress);
}

// Initially move to 85% as assets load
const initialTween = gsap.to(progressProxy, {
    value: 85,
    duration: 10,
    ease: "power1.out",
    onUpdate: () => updateUI(progressProxy.value)
});

window.addEventListener('load', () => {
    initialTween.kill();
    gsap.to(progressProxy, {
        value: 100,
        duration: 0.8,
        ease: "power2.out",
        onUpdate: () => updateUI(progressProxy.value),
        onComplete: () => {
            const exitTl = gsap.timeline();
            exitTl.to(".loading-text.initial", {
                y: "-100%",
                duration: 0.5,
                ease: "power2.inOut"
            })
                .to(".loading-text.complete", {
                    y: "0%",
                    duration: 0.5,
                    ease: "power2.inOut"
                }, "<")
                .to(completeText.chars, {
                    opacity: 1,
                    y: 0,
                    duration: 0.3,
                    stagger: 0.03,
                    ease: "power2.out"
                }, "<0.2")
                .to(".preloader", {
                    opacity: 0,
                    duration: 1,
                    ease: "power2.inOut",
                    delay: 0.8,
                    onComplete: () => {
                        const preloaderEl = document.querySelector(".preloader");
                        if (preloaderEl) preloaderEl.style.display = "none";
                    }
                });
        }
    });
});

/*=====================
    22. Recent Product Show Js
==========================*/
const box = document.querySelector('.recently-product-box');
const closeBtn = document.querySelector('.recent-close');
const timerElement = document.querySelector('.recent-content .timer');

const products = [
    {
        imageSrc: '../assets/images/product/1.png',
        productName: 'Smart Watch Series X3',
        productLink: 'product-color.html',
        price: '239.00',
        originalPrice: '250.00'
    },
    {
        imageSrc: '../assets/images/product/23.png',
        productName: 'BlackBerry Keyone BBB100-7 64gb unlocked gSM',
        productLink: 'product-color.html',
        price: '1920.00',
        originalPrice: '2000.00'
    },
    {
        imageSrc: '../assets/images/product/30.png',
        productName: 'Canon EOS 1500D DSLR Camera Body+ 18-55 mm',
        productLink: 'product-color.html',
        price: '199.00',
        originalPrice: '252.00'
    },
    {
        imageSrc: '../assets/images/product/27.png',
        productName: 'Motorola Moto X4 32GB Unlocked Smartphone',
        productLink: 'product-color.html',
        price: '1220.00',
        originalPrice: '1269.00'
    },
    {
        imageSrc: '../assets/images/product/34.png',
        productName: 'Shears Kitchen Spoone 6 Piece Set with Wooden Block',
        productLink: 'product-color.html',
        price: '1209.00',
        originalPrice: '1225.00'
    },
    {
        imageSrc: '../assets/images/product/31.png',
        productName: 'Pro Healthy Lifestyle Edible Oil 5 litre Jar | Saffola Gold Refined Oil',
        productLink: 'product-color.html',
        price: '1920.00',
        originalPrice: '2000.00'
    },
    {
        imageSrc: '../assets/images/product/35-1.png',
        productName: 'Herschel Leather duffle bag in brown color',
        productLink: 'product-color.html',
        price: '670.00',
        originalPrice: '900.00'
    },
    {
        imageSrc: '../assets/images/product/26.png',
        productName: 'EvoFox Game Box 32 GB with Asphalt 8 ',
        productLink: 'product-color.html',
        price: '130.00',
        originalPrice: '153.00'
    }
];

let currentIndex = 0;

function getRandomDelay(minSeconds, maxSeconds) {
    const min = minSeconds * 1000;
    const max = maxSeconds * 1000;
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomTimeText() {
    const minutes = Math.floor(Math.random() * 61);
    if (minutes === 0) return "Just now";
    if (minutes === 1) return "1 minute ago";
    if (minutes < 60) return `${minutes} minutes ago`;
    return "An hour ago";
}

function updateRecentProduct(product) {
    if (!box) return;

    const img = box.querySelector('img');
    const link = box.querySelector('.recent-content a');
    const priceTag = box.querySelector('.price');

    if (img) img.src = product.imageSrc;
    if (link) {
        link.textContent = product.productName;
        link.href = product.productLink;
    }
    if (priceTag) {
        priceTag.innerHTML = `$${product.price} <del>$${product.originalPrice}</del>`;
    }

    if (timerElement) {
        timerElement.textContent = getRandomTimeText();
    }

    box.classList.add('active');

    const removeDelay = getRandomDelay(7, 8);
    setTimeout(() => {
        box.classList.remove('active');

        const nextDelay = getRandomDelay(8, 9);
        setTimeout(() => {
            currentIndex = (currentIndex + 1) % products.length;
            updateRecentProduct(products[currentIndex]);
        }, nextDelay);
    }, removeDelay);
}

if (closeBtn && box) {
    closeBtn.addEventListener('click', () => {
        box.classList.remove('active');
    });
}

const initialDelay = getRandomDelay(8, 9);
setTimeout(() => {
    updateRecentProduct(products[currentIndex]);
}, initialDelay);