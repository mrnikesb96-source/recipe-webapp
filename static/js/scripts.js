document.addEventListener("DOMContentLoaded", function() {
    const loginOverlay = document.getElementById("login-overlay");
    const registerOverlay = document.getElementById("register-overlay");
    const showLoginLinks = document.querySelectorAll(".show-login");
    const showRegisterLink = document.getElementById("show-register");

    // Handle clicks on any login link
    showLoginLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            loginOverlay.style.display = "block";
            registerOverlay.style.display = "none";
        });
    });

    // Handle click on the register link
    showRegisterLink.addEventListener("click", function(e) {
        e.preventDefault();
        loginOverlay.style.display = "none";
        registerOverlay.style.display = "block";
    });

    // --- New part: server-side instructions ---
    if (document.body.dataset.showLogin === "true") {
        loginOverlay.style.display = "block";
        registerOverlay.style.display = "none";
    }

    if (document.body.dataset.showRegister === "true") {
        registerOverlay.style.display = "block";
        loginOverlay.style.display = "none";
    }
});