/*=====================
    Isotop Js
==========================*/
var grid = document.querySelector('.grid');
var msnry;
var imgAll = document.querySelectorAll('.grid-item');
var imgFashion = document.querySelectorAll('.fashion');
var imgBags = document.querySelectorAll('.electronic');
var imgOthers = document.querySelectorAll('.grocery');
const tabsUl = document.getElementById('filter-tab-group');
const lis = tabsUl.children;
const gridItems = grid.children;


imagesLoaded(grid, function () {
    setTimeout(() => {
        msnry = new Masonry(grid, {
            itemSelector: '.grid-item',
            columnWidth: '.grid-sizer',
            percentPosition: true
        });
    }, 1000)
});

function filterClass(childElems, parentElem, className) {

    [...parentElem].map(element => {
        const elementBtn = element.querySelector(".tab-filter");
        elementBtn?.classList.remove(className)

    });
    childElems.classList.add(className)

}

function showImages(showImg, hideImg1, hideImg2) {
    for (let i = 0; i < showImg.length; i++) {
        showImg[i].style.display = "block";
    }
    for (let i = 0; i < hideImg1.length; i++) {
        hideImg1[i].style.display = "none";
    }
    for (let i = 0; i < hideImg2.length; i++) {
        hideImg2[i].style.display = "none";
    }
}

tabsUl.addEventListener('click', (event) => {
    let tabLi = event.target.closest(".tab-filter");
    if (!tabLi) return
    filterClass(tabLi, lis, 'active');

    if (event.target.id == "all") {
        for (let i = 0; i < imgAll.length; i++) {
            imgAll[i].style.display = "block";
        }
    }

    if (event.target.id == "fashion") {
        showImages(imgFashion, imgBags, imgOthers);
    }

    if (event.target.id == "electronic") {
        showImages(imgBags, imgFashion, imgOthers);
    }

    if (event.target.id == "grocery") {
        showImages(imgOthers, imgBags, imgFashion);
    }

    msnry.layout();
});



