(function () {
    "use strict";

    function getCookie(name) {
        const cookies = document.cookie ? document.cookie.split(";") : [];
        for (const cookie of cookies) {
            const trimmed = cookie.trim();
            if (trimmed.startsWith(name + "=")) return decodeURIComponent(trimmed.slice(name.length + 1));
        }
        return "";
    }

    function stars(rating) {
        return Array.from({ length: 5 }, (_, index) =>
            '<li><i class="' + (index < rating ? "ri-star-fill fill" : "ri-star-line") + '"></i></li>'
        ).join("");
    }

    function initializeReviews() {
        const contextElement = document.getElementById("review-context");
        const reviewTab = document.getElementById("review");
        if (!contextElement || !reviewTab) return;

        let context;
        try {
            context = JSON.parse(contextElement.textContent);
        } catch (error) {
            return;
        }

        const score = Number(context.rating || 0).toFixed(1);
        const count = Number(context.review_count || 0);
        const summary = reviewTab.querySelector(".customer-review-box h5");
        const countLabel = reviewTab.querySelector(".customer-review-box h6");
        if (summary) summary.innerHTML = score + " <span>/5</span>";
        if (countLabel) countLabel.textContent = count + (count === 1 ? " avaliação" : " avaliações");

        const distribution = context.rating_distribution || {};
        reviewTab.querySelectorAll(".rating-list .progress-bar").forEach((bar, index) => {
            const rating = 5 - index;
            const percent = Number((distribution[rating] || {}).percent || 0);
            bar.style.width = percent + "%";
            bar.textContent = percent + "%";
        });

        const list = reviewTab.querySelector(".review-people > .review-list");
        if (list) {
            list.innerHTML = (context.reviews || []).map((review) => (
                '<li><div class="people-box"><div><div class="people-image"><i class="ri-user-3-line"></i></div></div>' +
                '<div class="people-comment"><div class="name"><a href="#!">' + escapeHtml(review.name) + '</a>' +
                '<div class="product-rating"><ul class="rating">' + stars(Number(review.rating)) + '</ul></div></div>' +
                '<div class="date-time"><h5 class="text-content h6">' + escapeHtml(review.created_at) + '</h5></div>' +
                '<div class="reply"><p>' + escapeHtml(review.comment) + '</p></div></div></div></li>'
            )).join("") || '<li><div class="people-box"><div class="people-comment"><p class="text-content">Ainda não existem avaliações para este produto.</p></div></div></li>';
        }

        const formColumn = reviewTab.querySelector(".review-title h4.fw-500")?.closest(".col-xl-6");
        const form = formColumn?.querySelector(".row.g-sm-4");
        if (!form) return;
        const ratingField = form.querySelector("select");
        const commentField = form.querySelector("textarea");
        const submitButton = form.querySelector("button[type='submit']");
        const message = document.createElement("p");
        message.className = "review-form-message text-content mt-2";
        form.appendChild(message);

        if (!context.can_review) {
            if (ratingField) ratingField.disabled = true;
            if (commentField) commentField.disabled = true;
            if (submitButton) submitButton.disabled = true;
            message.textContent = context.authenticated
                ? (context.has_review ? "Já avaliaste este produto." : "Só podes avaliar produtos que compraste.")
                : "Inicia sessão e compra este produto para poderes avaliá-lo.";
            return;
        }

        if (submitButton) {
            submitButton.addEventListener("click", function (event) {
                event.preventDefault();
                submitButton.disabled = true;
                message.textContent = "A publicar...";
                const data = new URLSearchParams({
                    rating: ratingField?.value || "5",
                    comment: commentField?.value || "",
                });
                fetch(context.submit_url, {
                    method: "POST",
                    credentials: "same-origin",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "X-Requested-With": "XMLHttpRequest",
                        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                    },
                    body: data.toString(),
                }).then((response) => response.json()).then((result) => {
                    message.textContent = result.message || "Não foi possível publicar a avaliação.";
                    if (result.success) window.location.reload();
                    else submitButton.disabled = false;
                }).catch(() => {
                    message.textContent = "Não foi possível publicar a avaliação. Tenta novamente.";
                    submitButton.disabled = false;
                });
            });
        }
    }

    function escapeHtml(value) {
        return String(value || "").replace(/[&<>'"]/g, (character) => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
        }[character]));
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initializeReviews);
    else initializeReviews();
})();

