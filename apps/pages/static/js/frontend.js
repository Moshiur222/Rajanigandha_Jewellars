// ============================
// PRODUCT DATA
// ============================

const categories = [
  "Diamond Jewellery", "Gold Jewellery", "Rings", "Earrings", "Nose Pins",
  "Necklaces", "Pendants", "Bracelets", "Bangles", "Wedding Collection",
  "Men’s Jewellery", "Kids Jewellery", "Gemstones", "Gifts"
];

const products = [
  {
    id: 1,
    code: "RA-1001",
    title: "Elegant Diamond Ring",
    category: "Rings",
    subcategory: "Diamond Jewellery",
    metal: "Diamond",
    gender: "Women",
    occasion: "Wedding",
    stock: "In Stock",
    oldPrice: 98000,
    price: 84500,
    popular: 95,
    weight: "4.2 gm",
    stone: "Natural Diamond",
    desc: "A premium diamond ring designed for elegant celebrations.",
    img: "https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=900",
      "https://images.unsplash.com/photo-1589674781759-c21c37956a44?q=80&w=900"
    ]
  },
  {
    id: 2,
    code: "RA-1002",
    title: "Royal Gold Necklace",
    category: "Necklaces",
    subcategory: "Gold Jewellery",
    metal: "Gold",
    gender: "Women",
    occasion: "Party",
    stock: "In Stock",
    oldPrice: 152000,
    price: 132000,
    popular: 88,
    weight: "18.5 gm",
    stone: "None",
    desc: "A luxurious gold necklace with timeless royal finishing.",
    img: "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=900",
      "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=900"
    ]
  },
  {
    id: 3,
    code: "RA-1003",
    title: "Pearl Drop Earrings",
    category: "Earrings",
    subcategory: "Gifts",
    metal: "Pearl",
    gender: "Women",
    occasion: "Gift",
    stock: "In Stock",
    oldPrice: 42000,
    price: 35000,
    popular: 72,
    weight: "3.1 gm",
    stone: "Pearl",
    desc: "Soft, elegant pearl earrings for everyday luxury.",
    img: "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=900",
      "https://images.unsplash.com/photo-1617038220319-276d3cfab638?q=80&w=900"
    ]
  },
  {
    id: 4,
    code: "RA-1004",
    title: "Classic Men’s Gold Ring",
    category: "Men’s Jewellery",
    subcategory: "Rings",
    metal: "Gold",
    gender: "Men",
    occasion: "Daily Wear",
    stock: "In Stock",
    oldPrice: 68000,
    price: 59900,
    popular: 80,
    weight: "7.8 gm",
    stone: "None",
    desc: "A strong and minimal gold ring for men.",
    img: "https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1602751584552-8ba73aad10e1?q=80&w=900",
      "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=900"
    ]
  },
  {
    id: 5,
    code: "RA-1005",
    title: "Wedding Diamond Bangles",
    category: "Bangles",
    subcategory: "Wedding Collection",
    metal: "Diamond",
    gender: "Women",
    occasion: "Wedding",
    stock: "Out of Stock",
    oldPrice: 185000,
    price: 165000,
    popular: 91,
    weight: "22 gm",
    stone: "Diamond",
    desc: "Luxury wedding bangles crafted for special moments.",
    img: "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=900",
      "https://images.unsplash.com/photo-1605100804763-247f67b3557e?q=80&w=900"
    ]
  },
  {
    id: 6,
    code: "RA-1006",
    title: "Emerald Gemstone Pendant",
    category: "Pendants",
    subcategory: "Gemstones",
    metal: "Gemstone",
    gender: "Women",
    occasion: "Gift",
    stock: "In Stock",
    oldPrice: 76000,
    price: 64000,
    popular: 67,
    weight: "5.4 gm",
    stone: "Emerald",
    desc: "A gemstone pendant with graceful green emerald shine.",
    img: "https://images.unsplash.com/photo-1611652022419-a9419f74343d?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1611652022419-a9419f74343d?q=80&w=900",
      "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=900"
    ]
  },
  {
    id: 7,
    code: "RA-1007",
    title: "Kids Gold Bracelet",
    category: "Kids Jewellery",
    subcategory: "Bracelets",
    metal: "Gold",
    gender: "Kids",
    occasion: "Gift",
    stock: "In Stock",
    oldPrice: 36000,
    price: 31500,
    popular: 62,
    weight: "4.9 gm",
    stone: "None",
    desc: "A cute gold bracelet designed for kids.",
    img: "https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1506630448388-4e683c67ddb0?q=80&w=900",
      "https://images.unsplash.com/photo-1611591437281-460bfbe1220a?q=80&w=900"
    ]
  },
  {
    id: 8,
    code: "RA-1008",
    title: "Gold Nose Pin",
    category: "Nose Pins",
    subcategory: "Gold Jewellery",
    metal: "Gold",
    gender: "Women",
    occasion: "Daily Wear",
    stock: "In Stock",
    oldPrice: 17000,
    price: 14500,
    popular: 58,
    weight: "1.1 gm",
    stone: "Tiny Diamond",
    desc: "A minimalist gold nose pin for daily wear.",
    img: "https://images.unsplash.com/photo-1617038220319-276d3cfab638?q=80&w=900",
    gallery: [
      "https://images.unsplash.com/photo-1617038220319-276d3cfab638?q=80&w=900",
      "https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?q=80&w=900"
    ]
  }
];

// ============================
// STATE
// ============================

let cart = JSON.parse(localStorage.getItem("cart")) || [];
let wishlist = JSON.parse(localStorage.getItem("wishlist")) || [];
let currentModalProduct = null;
let currentCurrency = localStorage.getItem("currency") || "BDT";

// ============================
// ELEMENTS
// ============================

const productGrid = document.getElementById("productGrid");
const saleGrid = document.getElementById("saleGrid");
const featuredTrack = document.getElementById("featuredTrack");
const categoryGrid = document.getElementById("categoryGrid");
const categoryFilter = document.getElementById("categoryFilter");
const metalFilter = document.getElementById("metalFilter");
const genderFilter = document.getElementById("genderFilter");
const occasionFilter = document.getElementById("occasionFilter");
const stockFilter = document.getElementById("stockFilter");
const priceFilter = document.getElementById("priceFilter");
const priceValue = document.getElementById("priceValue");
const sortFilter = document.getElementById("sortFilter");
const productSearch = document.getElementById("productSearch");
const resultCount = document.getElementById("resultCount");
const cartCount = document.getElementById("cartCount");
const wishlistCount = document.getElementById("wishlistCount");
const cartItems = document.getElementById("cartItems");
const wishlistItems = document.getElementById("wishlistItems");
const overlay = document.getElementById("overlay");
const toast = document.getElementById("toast");

// ============================
// HELPERS
// ============================

function formatPrice(amount) {
  if (currentCurrency === "USD") {
    return "$" + Math.round(amount / 110);
  }

  return "৳" + amount.toLocaleString("en-BD");
}

function discountPercent(oldPrice, price) {
  return Math.round(((oldPrice - price) / oldPrice) * 100);
}

function saveState() {
  localStorage.setItem("cart", JSON.stringify(cart));
  localStorage.setItem("wishlist", JSON.stringify(wishlist));
}

function showToast(message) {
  if (!toast) return;

  toast.textContent = message;
  toast.classList.add("show");

  setTimeout(() => {
    toast.classList.remove("show");
  }, 2200);
}

function getProduct(id) {
  return products.find(p => p.id === Number(id));
}

// ============================
// PRODUCT RENDER
// ============================

function productCard(product) {
  const isWish = wishlist.includes(product.id);
  const discount = discountPercent(product.oldPrice, product.price);

  return `
    <article class="product-card">
      <span class="badge">Save ${discount}%</span>
      <span class="stock">${product.stock}</span>

      <button class="wish-btn ${isWish ? "active" : ""}" onclick="toggleWishlist(${product.id})">
        <i class="fa-${isWish ? "solid" : "regular"} fa-heart"></i>
      </button>

      <div class="product-image">
        <img src="${product.img}" alt="${product.title}">
      </div>

      <div class="product-info">
        <span class="product-meta">${product.category} / ${product.metal}</span>
        <h3>${product.title}</h3>

        <div class="price-row">
          <span class="old-price">${formatPrice(product.oldPrice)}</span>
          <span class="new-price">${formatPrice(product.price)}</span>
          <span class="save">${discount}% OFF</span>
        </div>

        <div class="product-actions">
          <button class="gold-btn" onclick="addToCart(${product.id})">Add Cart</button>
          <button class="outline-btn" onclick="openQuickView(${product.id})">Quick View</button>
          <button class="dark-btn" onclick="buyNow(${product.id})">Buy Now</button>
        </div>
      </div>
    </article>
  `;
}

function getFilteredProducts() {
  const cat = categoryFilter.value;
  const metal = metalFilter.value;
  const gender = genderFilter.value;
  const occasion = occasionFilter.value;
  const stock = stockFilter.value;
  const maxPrice = Number(priceFilter.value);
  const search = productSearch.value.toLowerCase().trim();

  let filtered = products.filter(p => {
    const matchCat = cat === "all" || p.category === cat || p.subcategory === cat;
    const matchMetal = metal === "all" || p.metal === metal;
    const matchGender = gender === "all" || p.gender === gender;
    const matchOccasion = occasion === "all" || p.occasion === occasion;
    const matchStock = stock === "all" || p.stock === stock;
    const matchPrice = p.price <= maxPrice;

    const matchSearch =
      p.title.toLowerCase().includes(search) ||
      p.category.toLowerCase().includes(search) ||
      p.subcategory.toLowerCase().includes(search) ||
      p.code.toLowerCase().includes(search);

    return (
      matchCat &&
      matchMetal &&
      matchGender &&
      matchOccasion &&
      matchStock &&
      matchPrice &&
      matchSearch
    );
  });

  if (sortFilter.value === "low") filtered.sort((a, b) => a.price - b.price);
  if (sortFilter.value === "high") filtered.sort((a, b) => b.price - a.price);
  if (sortFilter.value === "popular") filtered.sort((a, b) => b.popular - a.popular);
  if (sortFilter.value === "latest") filtered.sort((a, b) => b.id - a.id);

  return filtered;
}

function renderProducts() {
  const filtered = getFilteredProducts();

  productGrid.innerHTML =
    filtered.map(productCard).join("") ||
    `<p class="muted">No products found.</p>`;

  resultCount.textContent = `Showing ${filtered.length} of ${products.length} products`;
}

function renderSale() {
  saleGrid.innerHTML = products
    .filter(p => discountPercent(p.oldPrice, p.price) >= 10)
    .slice(0, 4)
    .map(productCard)
    .join("");
}

function renderFeatured() {
  featuredTrack.innerHTML = products
    .slice(0, 6)
    .map(productCard)
    .join("");
}

function renderCategories() {
  categoryGrid.innerHTML = categories.map(cat => `
    <button class="category-card" onclick="filterByCategory('${cat}')">
      <span>${cat}</span>
    </button>
  `).join("");

  categoryFilter.innerHTML =
    `<option value="all">All Categories</option>` +
    categories.map(cat => `<option value="${cat}">${cat}</option>`).join("");
}

function filterByCategory(cat) {
  categoryFilter.value = cat;
  document.getElementById("products").scrollIntoView({ behavior: "smooth" });
  renderProducts();
}

// ============================
// CART
// ============================

function addToCart(id) {
  const existing = cart.find(item => item.id === id);

  if (existing) {
    existing.qty++;
  } else {
    cart.push({ id, qty: 1 });
  }

  saveState();
  renderCart();
  showToast("Product added to cart");
}

function buyNow(id) {
  addToCart(id);
  openPanel("cartPanel");
}

function updateQty(id, change) {
  const item = cart.find(i => i.id === id);
  if (!item) return;

  item.qty += change;

  if (item.qty <= 0) {
    cart = cart.filter(i => i.id !== id);
  }

  saveState();
  renderCart();
}

function removeCart(id) {
  cart = cart.filter(i => i.id !== id);
  saveState();
  renderCart();
}

function renderCart() {
  cartCount.textContent = cart.reduce((sum, item) => sum + item.qty, 0);

  if (!cart.length) {
    cartItems.innerHTML = `<p class="muted">Your cart is empty.</p>`;
  } else {
    cartItems.innerHTML = cart.map(item => {
      const product = getProduct(item.id);
      if (!product) return "";

      return `
        <div class="cart-item">
          <img src="${product.img}" alt="${product.title}" onclick="openQuickView(${product.id})">

          <div class="cart-info">
            <strong>${product.title}</strong>
            <p>${formatPrice(product.price)}</p>

            <div class="qty-row">
              <button onclick="updateQty(${item.id}, -1)">-</button>
              <span>${item.qty}</span>
              <button onclick="updateQty(${item.id}, 1)">+</button>

              <button onclick="openQuickView(${product.id})" title="Details">
                <i class="fa-regular fa-eye"></i>
              </button>

              <button onclick="removeCart(${item.id})" title="Remove">
                <i class="fa-solid fa-trash"></i>
              </button>
            </div>

            <button class="outline-btn cart-details-btn" onclick="openQuickView(${product.id})">
              Details
            </button>
          </div>
        </div>
      `;
    }).join("");
  }

  const subtotal = cart.reduce((sum, item) => {
    const product = getProduct(item.id);
    return product ? sum + product.price * item.qty : sum;
  }, 0);

  const delivery = subtotal > 0 ? 80 : 0;
  const total = subtotal + delivery;

  document.getElementById("subtotalAmount").textContent = formatPrice(subtotal);
  document.getElementById("deliveryAmount").textContent = formatPrice(delivery);
  document.getElementById("totalAmount").textContent = formatPrice(total);

  renderCheckoutSummary();
}

function renderCheckoutSummary() {
  const checkoutSummary = document.getElementById("checkoutSummary");
  const checkoutTotal = document.getElementById("checkoutTotal");

  if (!checkoutSummary || !checkoutTotal) return;

  if (!cart.length) {
    checkoutSummary.innerHTML = `<p class="muted">No items selected.</p>`;
    checkoutTotal.textContent = "";
    return;
  }

  checkoutSummary.innerHTML = cart.map(item => {
    const product = getProduct(item.id);
    if (!product) return "";

    return `
      <p>
        ${product.title} × ${item.qty} - ${formatPrice(product.price * item.qty)}
      </p>
    `;
  }).join("");

  const subtotal = cart.reduce((sum, item) => {
    const product = getProduct(item.id);
    return product ? sum + product.price * item.qty : sum;
  }, 0);

  checkoutTotal.textContent = `Total: ${formatPrice(subtotal + 80)}`;
}

// ============================
// WISHLIST
// ============================

function toggleWishlist(id) {
  if (wishlist.includes(id)) {
    wishlist = wishlist.filter(item => item !== id);
    showToast("Removed from wishlist");
  } else {
    wishlist.push(id);
    showToast("Added to wishlist");
  }

  saveState();
  renderWishlist();
  renderProducts();
  renderSale();
  renderFeatured();
}

function renderWishlist() {
  wishlistCount.textContent = wishlist.length;

  if (!wishlist.length) {
    wishlistItems.innerHTML = `<p class="muted">Your wishlist is empty.</p>`;
    return;
  }

  wishlistItems.innerHTML = wishlist.map(id => {
    const product = getProduct(id);
    if (!product) return "";

    return `
      <div class="wishlist-item">
        <img src="${product.img}" alt="${product.title}" onclick="openQuickView(${product.id})">

        <div>
          <strong>${product.title}</strong>
          <p>${formatPrice(product.price)}</p>

          <button class="outline-btn" onclick="openQuickView(${product.id})">
            Details
          </button>

          <button class="outline-btn" onclick="toggleWishlist(${id})">
            Remove
          </button>
        </div>
      </div>
    `;
  }).join("");
}

// ============================
// MODAL
// ============================

function openQuickView(id) {
  const product = getProduct(id);
  if (!product) return;

  currentModalProduct = product;

  document.getElementById("modalCode").textContent = product.code;
  document.getElementById("modalTitle").textContent = product.title;
  document.getElementById("modalDesc").textContent = product.desc;
  document.getElementById("modalOld").textContent = formatPrice(product.oldPrice);
  document.getElementById("modalPrice").textContent = formatPrice(product.price);
  document.getElementById("modalDiscount").textContent =
    `${discountPercent(product.oldPrice, product.price)}% OFF`;
  document.getElementById("modalMetal").textContent = product.metal;
  document.getElementById("modalWeight").textContent = product.weight;
  document.getElementById("modalStone").textContent = product.stone;
  document.getElementById("modalStock").textContent = product.stock;
  document.getElementById("modalMainImg").src = product.img;

  document.getElementById("modalThumbs").innerHTML = product.gallery.map((img, index) => `
    <img 
      src="${img}" 
      class="${index === 0 ? "active" : ""}" 
      onclick="changeModalImage('${img}', this)"
      alt="${product.title}"
    >
  `).join("");

  openModal("quickModal");
}

function changeModalImage(src, element) {
  document.getElementById("modalMainImg").src = src;

  document.querySelectorAll("#modalThumbs img").forEach(img => {
    img.classList.remove("active");
  });

  element.classList.add("active");
}

document.getElementById("modalAddCart").addEventListener("click", () => {
  if (currentModalProduct) {
    addToCart(currentModalProduct.id);
  }
});

document.getElementById("modalWishlist").addEventListener("click", () => {
  if (currentModalProduct) {
    toggleWishlist(currentModalProduct.id);
  }
});

// ============================
// PANELS / MODALS
// ============================

function openPanel(id) {
  document.getElementById(id).classList.add("active");
  overlay.classList.add("active");
}

function closePanels() {
  document.querySelectorAll(".mobile-sidebar, .side-panel").forEach(panel => {
    panel.classList.remove("active");
  });

  overlay.classList.remove("active");
}

function openModal(id) {
  document.getElementById(id).classList.add("active");
}

function closeModal(id) {
  document.getElementById(id).classList.remove("active");
}

document.getElementById("menuOpen").addEventListener("click", () => {
  document.getElementById("mobileSidebar").classList.add("active");
  overlay.classList.add("active");
});

document.getElementById("menuClose").addEventListener("click", closePanels);

document.getElementById("cartToggle").addEventListener("click", () => {
  openPanel("cartPanel");
});

document.getElementById("wishlistToggle").addEventListener("click", () => {
  openPanel("wishlistPanel");
});

document.getElementById("accountToggle").addEventListener("click", () => {
  openModal("accountModal");
});

document.getElementById("checkoutOpen").addEventListener("click", () => {
  openModal("checkoutModal");
});

overlay.addEventListener("click", closePanels);

document.querySelectorAll("[data-close]").forEach(btn => {
  btn.addEventListener("click", () => {
    const type = btn.dataset.close;

    if (type === "cart" || type === "wishlist") closePanels();
    if (type === "quick") closeModal("quickModal");
    if (type === "account") closeModal("accountModal");
    if (type === "checkout") closeModal("checkoutModal");
  });
});

document.querySelectorAll(".modal").forEach(modal => {
  modal.addEventListener("click", e => {
    if (e.target === modal) {
      modal.classList.remove("active");
    }
  });
});

// ============================
// SEARCH
// ============================

document.getElementById("searchToggle").addEventListener("click", () => {
  document.getElementById("searchPanel").classList.toggle("active");
});

document.getElementById("searchInput").addEventListener("input", e => {
  const value = e.target.value.toLowerCase().trim();
  const box = document.getElementById("searchSuggestions");

  if (!value) {
    box.style.display = "none";
    return;
  }

  const matched = products.filter(p =>
    p.title.toLowerCase().includes(value) ||
    p.category.toLowerCase().includes(value) ||
    p.subcategory.toLowerCase().includes(value) ||
    p.code.toLowerCase().includes(value)
  ).slice(0, 5);

  box.innerHTML = matched.map(p => `
    <div class="suggestion-item" onclick="openQuickView(${p.id})">
      ${p.title} - ${formatPrice(p.price)}
    </div>
  `).join("");

  box.style.display = matched.length ? "block" : "none";
});

// ============================
// THEME / CURRENCY
// ============================

function setTheme(theme) {
  if (theme === "dark") {
    document.body.classList.add("dark");
  } else {
    document.body.classList.remove("dark");
  }

  localStorage.setItem("theme", theme);
}

function toggleTheme() {
  const isDark = document.body.classList.contains("dark");
  setTheme(isDark ? "light" : "dark");
}

document.getElementById("themeToggle").addEventListener("click", toggleTheme);
document.getElementById("mobileThemeToggle").addEventListener("click", toggleTheme);

if (localStorage.getItem("theme") === "dark") {
  setTheme("dark");
}

document.getElementById("currencySelect").value = currentCurrency;

document.getElementById("currencySelect").addEventListener("change", e => {
  currentCurrency = e.target.value;
  localStorage.setItem("currency", currentCurrency);

  renderProducts();
  renderSale();
  renderFeatured();
  renderCart();
  renderWishlist();
});

// ============================
// FILTER EVENTS
// ============================

[
  categoryFilter,
  metalFilter,
  genderFilter,
  occasionFilter,
  stockFilter,
  sortFilter,
  productSearch
].forEach(el => {
  el.addEventListener("input", renderProducts);
});

priceFilter.addEventListener("input", () => {
  priceValue.textContent = Number(priceFilter.value).toLocaleString("en-BD");
  renderProducts();
});

document.getElementById("resetFilters").addEventListener("click", () => {
  categoryFilter.value = "all";
  metalFilter.value = "all";
  genderFilter.value = "all";
  occasionFilter.value = "all";
  stockFilter.value = "all";
  sortFilter.value = "latest";
  productSearch.value = "";
  priceFilter.value = 200000;
  priceValue.textContent = "200000";

  renderProducts();
});

// ============================
// TRACK ORDER
// ============================

document.getElementById("trackBtn").addEventListener("click", () => {
  const value = document.getElementById("trackInput").value.trim();
  const steps = document.querySelectorAll(".step");

  if (!value) {
    showToast("Please enter an order ID");
    return;
  }

  steps.forEach(step => step.classList.remove("active"));

  let activeCount = 2;

  if (value.toUpperCase().includes("1001")) activeCount = 4;
  if (value.toUpperCase().includes("1002")) activeCount = 3;

  steps.forEach((step, index) => {
    if (index < activeCount) {
      step.classList.add("active");
    }
  });

  showToast("Order status updated");
});

// ============================
// ACCOUNT TABS / CHECKOUT
// ============================

document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => {
      t.classList.remove("active");
    });

    document.querySelectorAll(".auth-form").forEach(f => {
      f.classList.remove("active");
    });

    tab.classList.add("active");
    document.getElementById(tab.dataset.tab + "Form").classList.add("active");
  });
});

document.getElementById("placeOrder").addEventListener("click", () => {
  if (!cart.length) {
    showToast("Your cart is empty");
    return;
  }

  cart = [];
  saveState();
  renderCart();
  closeModal("checkoutModal");
  closePanels();
  showToast("Order placed successfully");
});

// ============================
// SCROLL EFFECTS
// ============================

const navbar = document.getElementById("navbar");
const backTop = document.getElementById("backTop");

window.addEventListener("scroll", () => {
  navbar.classList.toggle("scrolled", window.scrollY > 40);
  backTop.classList.toggle("show", window.scrollY > 500);
});

backTop.addEventListener("click", () => {
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});

const revealObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("active");
    }
  });
}, {
  threshold: 0.15
});

document.querySelectorAll(".reveal").forEach(el => {
  revealObserver.observe(el);
});

// ============================
// FEATURED SCROLL
// ============================

document.getElementById("prevFeatured").addEventListener("click", () => {
  featuredTrack.scrollBy({
    left: -300,
    behavior: "smooth"
  });
});

document.getElementById("nextFeatured").addEventListener("click", () => {
  featuredTrack.scrollBy({
    left: 300,
    behavior: "smooth"
  });
});

// ============================
// INIT
// ============================

renderCategories();
renderProducts();
renderSale();
renderFeatured();
renderCart();
renderWishlist();