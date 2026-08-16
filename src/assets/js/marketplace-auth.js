(() => {
    const modal = document.querySelector("#authenticationModal");
    if (!modal) return;

    const csrfToken = () => {
        const match = document.cookie.match(/(^|; )csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[2]) : "";
    };

    const feedback = (form, message, success = false) => {
        let box = form.querySelector(".marketplace-auth-feedback");
        if (!box) {
            box = document.createElement("div");
            box.className = "marketplace-auth-feedback mt-3";
            form.prepend(box);
        }
        box.textContent = message;
        box.classList.toggle("text-success", success);
        box.classList.toggle("text-danger", !success);
    };

    const request = async (form, endpoint) => {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken() },
            credentials: "same-origin",
            body: new FormData(form),
        });
        const raw = await response.text();
        let data;
        try {
            data = JSON.parse(raw);
        } catch (parseError) {
            const error = new Error(
                response.status === 403
                    ? "A sessão de segurança expirou. Atualize a página e tente novamente."
                    : "O servidor devolveu uma resposta inesperada. Tente novamente."
            );
            error.payload = { status: response.status, raw };
            throw error;
        }
        if (!response.ok) {
            const error = new Error(data.message || "Não foi possível concluir a operação.");
            error.payload = data;
            throw error;
        }
        return data;
    };

    const loginForm = modal.querySelector(".login-box form");
    const loginButton = modal.querySelector(".login-box a.btn-bg-theme");
    if (loginForm && loginButton) {
        const fields = loginForm.querySelectorAll("input");
        if (fields[0]) fields[0].name = "email";
        if (fields[1]) fields[1].name = "password";
        loginButton.addEventListener("click", async (event) => {
            event.preventDefault();
            try {
                const data = await request(loginForm, "/account/modal/login/");
                feedback(loginForm, data.message, true);
                window.location.href = data.redirect || "/";
            } catch (error) {
                feedback(loginForm, error.message);
            }
        });
    }

    const signupForm = modal.querySelector(".signup-box form");
    const signupButton = modal.querySelector(".signup-box a.btn-bg-theme");
    if (signupForm && signupButton) {
        const fields = signupForm.querySelectorAll("input");
        if (fields[0]) fields[0].name = "full_name";
        if (fields[1]) fields[1].name = "email";
        if (fields[2]) fields[2].name = "password";
        const agreement = signupForm.querySelector("input[type=checkbox]");
        if (agreement) agreement.name = "terms";
        signupButton.addEventListener("click", async (event) => {
            event.preventDefault();
            try {
                const data = await request(signupForm, "/account/modal/register/");
                feedback(signupForm, data.message, true);
                window.location.href = data.redirect || "/";
            } catch (error) {
                feedback(signupForm, error.message);
            }
        });
    }

    const resetForm = modal.querySelector(".forgot-password-box form");
    if (resetForm) {
        const email = resetForm.querySelector("input[type=email]");
        if (email) email.name = "email";
        resetForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            try {
                const data = await request(resetForm, "/account/modal/password-reset/");
                feedback(resetForm, data.message, true);
            } catch (error) {
                feedback(resetForm, error.message);
            }
        });
    }

    const params = new URLSearchParams(window.location.search);
    if (params.get("open_auth") === "1" && window.bootstrap && window.bootstrap.Modal) {
        window.bootstrap.Modal.getOrCreateInstance(modal).show();
    }

    fetch("/account/session-status/", { credentials: "same-origin", headers: { "Accept": "application/json" } })
        .then((response) => response.json())
        .then((session) => {
            const loginLinks = document.querySelectorAll("a[href*='authenticationModal'], a.login-btn");
            const accountLinks = document.querySelectorAll("a[href='user-dashboard.html'], a[href='/account/profile/']");
            if (!session.authenticated) return;
            loginLinks.forEach((link) => {
                link.textContent = "A minha conta";
                link.href = session.profile_url;
                link.removeAttribute("data-bs-toggle");
            });
            accountLinks.forEach((link) => {
                link.href = session.profile_url;
                if (link.textContent.trim() === "My Account" || link.textContent.trim() === "Account") {
                    link.textContent = session.name;
                }
            });
            const userDropdown = document.querySelector(".user-dropdown");
            if (userDropdown && !userDropdown.querySelector(".marketplace-logout-link")) {
                const item = document.createElement("li");
                item.innerHTML = '<a class="btn login-btn marketplace-logout-link" href="' + session.logout_url + '">Terminar sessão</a>';
                userDropdown.appendChild(item);
            }
        })
        .catch(() => {});
})();
