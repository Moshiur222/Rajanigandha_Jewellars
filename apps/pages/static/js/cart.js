document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".add-cart-btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const url = btn.dataset.url;
            if (!url) return;

            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "login_required") {
                    showToast(data.message || "Please login first");

                    setTimeout(function () {
                        window.location.href = data.login_url;
                    }, 1200);

                    return;
                }

                if (data.status === "success") {
                    updateCount("cartCount", data.cart_count);
                    showToast(data.message || "Product added to cart");

                    btn.innerHTML = '<i class="fa-solid fa-check"></i>';

                    setTimeout(function () {
                        btn.innerHTML = "Add Cart";
                        btn.disabled = false;
                    }, 1000);
                } else {
                    btn.innerHTML = "Add Cart";
                    btn.disabled = false;
                    showToast(data.message || "Something went wrong");
                }
            })
            .catch(function () {
                btn.innerHTML = "Add Cart";
                btn.disabled = false;
                showToast("Something went wrong");
            });
        });
    });


    document.querySelectorAll(".buy-now-btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const url = btn.dataset.url;
            const checkoutUrl = btn.dataset.checkout;

            if (!url) return;

            btn.disabled = true;
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "login_required") {
                    showToast(data.message || "Please login first");

                    setTimeout(function () {
                        window.location.href = data.login_url;
                    }, 1200);

                    return;
                }

                if (data.status === "success") {
                    window.location.href = checkoutUrl || "/checkout/";
                } else {
                    btn.disabled = false;
                    btn.innerHTML = "Buy Now";
                    showToast(data.message || "Something went wrong");
                }
            })
            .catch(function () {
                btn.disabled = false;
                btn.innerHTML = "Buy Now";
                showToast("Something went wrong");
            });
        });
    });


    document.querySelectorAll(".add-wishlist-btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const url = btn.dataset.url;
            const icon = btn.querySelector("i");

            if (!url) return;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "login_required") {
                    showToast(data.message || "Please login first");

                    setTimeout(function () {
                        window.location.href = data.login_url;
                    }, 1200);

                    return;
                }

                if (data.status === "success") {
                    updateCount("wishlistCount", data.wishlist_count);

                    btn.classList.add("active");

                    if (icon) {
                        icon.classList.remove("fa-regular");
                        icon.classList.add("fa-solid");
                    }

                    showToast(data.message || "Product added to wishlist");
                }
            })
            .catch(function () {
                showToast("Something went wrong");
            });
        });
    });


    document.querySelectorAll(".remove-wishlist-btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const url = btn.dataset.url;
            const card = btn.closest(".product-card");

            if (!url) return;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    updateCount("wishlistCount", data.wishlist_count);
                    updateCount("wishlistItemCount", data.wishlist_count);

                    if (card) {
                        card.classList.add("removing");

                        setTimeout(function () {
                            card.remove();

                            const remaining = document.querySelectorAll("#wishlistGrid .product-card").length;

                            if (remaining === 0) {
                                location.reload();
                            }
                        }, 300);
                    }

                    showToast(data.message || "Removed from wishlist");
                }
            })
            .catch(function () {
                showToast("Something went wrong");
            });
        });
    });


    document.querySelectorAll(".wishlist-add-cart-btn").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const cartUrl = btn.dataset.url;
            const card = btn.closest(".product-card");
            const removeBtn = card ? card.querySelector(".remove-wishlist-btn") : null;
            const removeUrl = removeBtn ? removeBtn.getAttribute("data-url") : "";

            if (!cartUrl) return;

            btn.disabled = true;

            fetch(cartUrl, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "login_required") {
                    showToast(data.message || "Please login first");

                    setTimeout(function () {
                        window.location.href = data.login_url;
                    }, 1200);

                    return;
                }

                if (data.status === "success") {
                    updateCount("cartCount", data.cart_count);
                    showToast("Added to cart");

                    if (!removeUrl) {
                        btn.disabled = false;
                        return;
                    }

                    fetch(removeUrl, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken"),
                            "X-Requested-With": "XMLHttpRequest"
                        }
                    })
                    .then(response => response.json())
                    .then(removeData => {
                        updateCount("wishlistCount", removeData.wishlist_count);
                        updateCount("wishlistItemCount", removeData.wishlist_count);

                        if (card) {
                            card.classList.add("removing");

                            setTimeout(function () {
                                card.remove();

                                const remaining = document.querySelectorAll("#wishlistGrid .product-card").length;

                                if (remaining === 0) {
                                    location.reload();
                                }
                            }, 300);
                        }
                    });
                }

                btn.disabled = false;
            })
            .catch(function () {
                btn.disabled = false;
                showToast("Something went wrong");
            });
        });
    });


    const clearWishlistBtn = document.getElementById("clearWishlistBtn");

    if (clearWishlistBtn) {
        clearWishlistBtn.addEventListener("click", function (e) {
            e.preventDefault();

            const url = clearWishlistBtn.dataset.url;
            if (!url) return;

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    updateCount("wishlistCount", 0);
                    updateCount("wishlistItemCount", 0);
                    location.reload();
                }
            })
            .catch(function () {
                showToast("Something went wrong");
            });
        });
    }


    document.querySelectorAll(".quick-view-btn, .quick-view-trigger").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            e.preventDefault();

            const url = btn.dataset.url || btn.getAttribute("href");

            if (url) {
                window.location.href = url;
            }
        });
    });


    document.querySelectorAll(".cart-login-check, .wishlist-login-check").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
            const href = btn.getAttribute("href");

            if (href === "javascript:void(0)") {
                e.preventDefault();

                showToast("Please login first");

                setTimeout(function () {
                    window.location.href = btn.dataset.login;
                }, 1200);
            }
        });
    });

});


function updateCount(id, value) {
    const el = document.getElementById(id);

    if (el) {
        el.innerText = value || 0;
    }
}


function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");

        for (let cookie of cookies) {
            cookie = cookie.trim();

            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}


function showToast(message) {
    const oldToast = document.querySelector(".custom-toast");

    if (oldToast) {
        oldToast.remove();
    }

    const toast = document.createElement("div");
    toast.className = "custom-toast";
    toast.innerText = message;

    document.body.appendChild(toast);

    setTimeout(function () {
        toast.classList.add("show");
    }, 100);

    setTimeout(function () {
        toast.classList.remove("show");

        setTimeout(function () {
            toast.remove();
        }, 300);
    }, 2200);
}