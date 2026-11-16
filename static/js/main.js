document.addEventListener("DOMContentLoaded", () => {

    const menuButton = document.getElementById("mobileMenuButton");
    const menuCloseButton = document.getElementById("mobileMenuClose");
    const mobileMenu = document.getElementById("mobileMenu");
    const menuOverlay = document.getElementById("mobileMenuOverlay");

    if (!menuButton || !menuCloseButton || !mobileMenu || !menuOverlay) {
        return;
    }

    function openMenu() {
        mobileMenu.classList.remove("translate-x-full");
        menuOverlay.classList.remove("hidden");

        requestAnimationFrame(() => {
            menuOverlay.classList.remove("opacity-0");
        });

        menuButton.setAttribute("aria-expanded", "true");
        mobileMenu.setAttribute("aria-hidden", "false");

        document.body.classList.add("overflow-hidden");
    }

    function closeMenu() {
        mobileMenu.classList.add("translate-x-full");
        menuOverlay.classList.add("opacity-0");

        menuButton.setAttribute("aria-expanded", "false");
        mobileMenu.setAttribute("aria-hidden", "true");

        document.body.classList.remove("overflow-hidden");

        setTimeout(() => {
            menuOverlay.classList.add("hidden");
        }, 300);
    }

    menuButton.addEventListener("click", openMenu);

    menuCloseButton.addEventListener("click", closeMenu);

    menuOverlay.addEventListener("click", closeMenu);

    mobileMenu.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closeMenu();
        }
    });

});