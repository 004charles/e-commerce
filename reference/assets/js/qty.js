/*=====================
    QTY Js
==========================*/
document.addEventListener('DOMContentLoaded', function () {
  const totalPriceElement = document.getElementById('total-price');
  const progressBar = document.querySelector('.cart-offcanvas .progress-bar');

  function updateTotal() {
    const cartItems = document.querySelectorAll('.cart-product-box .vertical-product-box');
    let total = 0;
    let itemCount = 0;

    cartItems.forEach(item => {
      const quantityInput = item.querySelector('.input-qty');
      const itemPrice = parseFloat(item.getAttribute('data-price')) || 0;

      if (quantityInput) {
        const quantity = parseInt(quantityInput.value, 10) || 1;
        total += quantity * itemPrice;
        itemCount += quantity;
      }
    });

    totalPriceElement.textContent = `$${(Math.round(total * 100) / 100).toFixed(2)}`;

    const progressValue = Math.min(itemCount * 10, 100);
    if (progressBar) {
      progressBar.style.width = `${progressValue}%`;

      progressBar.classList.remove('bg-red', 'bg-yellow', 'bg-green');
      if (progressValue <= 30) {
        progressBar.classList.add('bg-red');
      } else if (progressValue <= 70) {
        progressBar.classList.add('bg-yellow');
      } else {
        progressBar.classList.add('bg-green');
      }

      if (progressValue === 100) {
        progressBar.classList.add('show');
        setTimeout(() => {
          progressBar.classList.remove('show');
        }, 5000);
      }
    }

    if (cartItems.length === 0) {
      totalPriceElement.textContent = `$0.00`;
    }
  }

  function checkEmptyCart() {
    const productBoxes = document.querySelectorAll(".cart-offcanvas:not(.wishlist-offcanvas) .vertical-product-box");
    const emptyCartMessage = document.querySelector(".empty-cart");

    if (emptyCartMessage) {
      emptyCartMessage.style.display = productBoxes.length === 0 ? "block" : "none";
    }
  }

  function setupCartItem(item) {
    const decrementButton = item.querySelector('.qty-btn-minus');
    const incrementButton = item.querySelector('.qty-btn-plus');
    const trashButton = item.querySelector('.btn-trash');
    const closeButton = item.querySelector('.close-button');
    const quantityInput = item.querySelector('.input-qty');
    const priceElement = item.querySelector('.product-content .price');

    const itemPrice = parseFloat(priceElement.textContent.replace('$', '')) || 0;
    item.setAttribute('data-price', itemPrice);

    if (incrementButton) {
      incrementButton.addEventListener('click', () => {
        let quantity = parseInt(quantityInput.value, 10) || 1;
        quantityInput.value = quantity + 1;

        if (quantityInput.value > 1) {
          if (decrementButton) decrementButton.style.display = "inline-block";
          if (trashButton) trashButton.style.display = "none";
          if (closeButton) closeButton.style.display = "block";
        }

        updateTotal();
      });
    }

    if (decrementButton) {
      decrementButton.addEventListener('click', () => {
        let quantity = parseInt(quantityInput.value, 10) || 1;
        if (quantity > 1) {
          quantityInput.value = quantity - 1;

          if (quantityInput.value == 1) {
            if (decrementButton) decrementButton.style.display = "none";
            if (trashButton) trashButton.style.display = "inline-block";
            if (closeButton) closeButton.style.display = "none";
          }

          updateTotal();
        }
      });
    }

    if (trashButton) {
      trashButton.addEventListener('click', () => {
        item.remove();
        checkEmptyCart();
        updateTotal();
      });
    }

    if (closeButton) {
      closeButton.addEventListener('click', () => {
        item.remove();
        checkEmptyCart();
        updateTotal();
      });
    }
  }

  document.querySelectorAll('.cart-product-box .vertical-product-box').forEach(setupCartItem);

  checkEmptyCart();
  updateTotal();
});