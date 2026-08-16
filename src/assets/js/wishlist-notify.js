/**=====================
    Wishlist Notify Js
==========================**/
document.addEventListener("DOMContentLoaded", () => {
    const wishlistStates = JSON.parse(localStorage.getItem('wishlistStates')) || {};

    document.querySelectorAll('.wishlistProduct').forEach((icon, index) => {
        const iconId = `wishlist-${index}`;
        const productBox = icon.closest('.productMain');

        const productImageEl = productBox ? productBox.querySelector('.productImage') : null;
        const productNameEl = productBox ? productBox.querySelector('.productName') : null;

        const productImage = productImageEl ? productImageEl.src : '';
        const productName = productNameEl ? productNameEl.textContent : 'Unknown Product';

        if (!(iconId in wishlistStates)) {
            wishlistStates[iconId] = false;
        }

        if (wishlistStates[iconId]) {
            icon.classList.add('show');
        }

        let fadeOutTimeout;

        icon.addEventListener('click', () => {
            const alertBox = document.getElementById('alertBox');
            const alertMessage = document.getElementById('alertMessage');
            const progressBar = document.getElementById('progressBar');
            const removeButton = alertBox ? alertBox.querySelector('.remove-wishlist') : null;

            if (!alertBox || !alertMessage || !progressBar || !removeButton) {
                console.warn("⚠️ Alert box or its children missing in DOM");
                return;
            }

            const message = wishlistStates[iconId]
                ? 'Product removed successfully'
                : 'Product added successfully';

            alertMessage.innerHTML = `
                <h4>${message}</h4>
                <div class="alert-image">
                    <img src="${productImage}" alt="Product" class="img-fluid"/>
                    <h5>${productName}</h5>
                </div>
            `;

            alertBox.classList.toggle('removed', wishlistStates[iconId]);
            alertBox.classList.toggle('added', !wishlistStates[iconId]);

            icon.classList.toggle('show', !wishlistStates[iconId]);

            wishlistStates[iconId] = !wishlistStates[iconId];

            localStorage.setItem('wishlistStates', JSON.stringify(wishlistStates));

            alertBox.style.display = 'block';
            alertBox.style.opacity = '0';
            alertBox.style.transform = 'translateY(-20px)';

            let opacity = 0;
            let translateY = -20;
            const fadeIn = setInterval(() => {
                if (opacity < 1) {
                    opacity += 0.05;
                    translateY += 1;
                    alertBox.style.opacity = opacity.toFixed(2);
                    alertBox.style.transform = `translateY(${translateY}px)`;
                } else {
                    clearInterval(fadeIn);
                }
            }, 16);

            progressBar.offsetWidth;
            progressBar.style.animation = 'progressBarAnimation 25s linear forwards';

            function startFadeOut() {
                fadeOutTimeout = setTimeout(() => {
                    let opacityOut = 1;
                    let translateOut = 0;
                    const fadeOut = setInterval(() => {
                        if (opacityOut > 0) {
                            opacityOut -= 0.05;
                            translateOut -= 1;
                            alertBox.style.opacity = opacityOut.toFixed(2);
                            alertBox.style.transform = `translateY(${translateOut}px)`;
                        } else {
                            clearInterval(fadeOut);
                            alertBox.style.display = 'none';
                        }
                    }, 16);
                }, 2500);
            }

            startFadeOut();

            alertBox.addEventListener('mouseenter', () => {
                clearTimeout(fadeOutTimeout);
            });

            alertBox.addEventListener('mouseleave', () => {
                startFadeOut();
            });

            removeButton.textContent = wishlistStates[iconId]
                ? 'Remove Wishlist'
                : 'Add to Wishlist';

            removeButton.onclick = () => {
                if (wishlistStates[iconId]) {
                    wishlistStates[iconId] = false;
                    icon.classList.remove('show');
                    removeButton.textContent = 'Add to Wishlist';
                    alertBox.classList.remove('added');
                    alertBox.classList.add('removed');
                    alertMessage.innerHTML = `
                        <h4>Product removed from wishlist</h4>
                        <div class="alert-image">
                            <img src="${productImage}" alt="Product" class="img-fluid"/>
                            <h5>${productName}</h5>
                        </div>
                    `;
                } else {
                    wishlistStates[iconId] = true;
                    icon.classList.add('show');
                    removeButton.textContent = 'Remove Wishlist';
                    alertBox.classList.remove('removed');
                    alertBox.classList.add('added');
                    alertMessage.innerHTML = `
                        <h4>Product added to wishlist</h4>
                        <div class="alert-image">
                            <img src="${productImage}" alt="Product" class="img-fluid"/>
                            <h5>${productName}</h5>
                        </div>
                    `;
                }
                localStorage.setItem('wishlistStates', JSON.stringify(wishlistStates));
            };
        });

        const addCartButton = document.querySelector('.alert-box .add-cart-btn');
        if (addCartButton) {
            addCartButton.addEventListener('click', () => {
                const alertBox = document.getElementById('alertBox');
                if (alertBox) {
                    alertBox.style.display = 'none';
                }
            });
        }
    });
});
