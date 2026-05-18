from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from apps.pages.models import *
from apps.dashboard.models import *


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user.user_type == 1:
                return redirect("dashboard:home")

            return redirect("pages:home")

        messages.error(request, "Invalid email or password")

    return render(request, "pages/login.html")


def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name") or request.POST.get("name") or ""
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("pages:signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("pages:signup")

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            user_type=2
        )

        login(request, user)
        return redirect("pages:home")

    return render(request, "pages/signup.html")

@login_required
def profile_view(request):

    if request.user.user_type != 2:
        return redirect("dashboard:home")

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        request.user.first_name = request.POST.get(
            "first_name",
            ""
        )

        request.user.last_name = request.POST.get(
            "last_name",
            ""
        )

        request.user.save()

        profile.phone = request.POST.get(
            "phone",
            ""
        )

        profile.alternate_phone = request.POST.get(
            "alternate_phone",
            ""
        )

        profile.gender = request.POST.get(
            "gender"
        ) or None

        profile.date_of_birth = request.POST.get(
            "date_of_birth"
        ) or None

        profile.address = request.POST.get(
            "address",
            ""
        )

        profile.city = request.POST.get(
            "city",
            ""
        )

        profile.area = request.POST.get(
            "area",
            ""
        )

        profile.zip_code = request.POST.get(
            "zip_code",
            ""
        )

        profile.bio = request.POST.get(
            "bio",
            ""
        )

        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES.get(
                "profile_image"
            )

        profile.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("pages:profile")

    return render(request, "pages/profile.html", {
        "profile": profile
    })


@login_required
def order_view(request):

    if request.user.user_type != 2:
        return redirect("dashboard:home")

    orders = Order.objects.prefetch_related(
        "items"
    ).filter(
        user=request.user
    ).order_by("-id")

    return render(request, "pages/order.html", {
        "orders": orders
    })


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Profile


@login_required
def settings_view(request):

    if request.user.user_type != 2:
        return redirect("dashboard:home")

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("pages:settings")

        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect("pages:settings")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("pages:settings")

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        messages.success(request, "Password updated successfully.")
        return redirect("pages:settings")

    return render(request, "pages/settings.html", {
        "profile": profile
    })


def home(request):
    if request.user.is_authenticated and request.user.user_type == 1:
        return redirect("dashboard:home")

    categories = Category.objects.all().order_by("order")
    sub_categories = SubCategory.objects.all().order_by("order")

    products = Product.objects.select_related(
        "menue", "category", "subcategory"
    ).order_by("order")[:20]

    featured_products = Product.objects.select_related(
        "menue", "category", "subcategory"
    ).filter(is_featured=True).order_by("order")[:20]

    sale_products = Product.objects.select_related(
        "menue", "category", "subcategory"
    ).order_by("order")[:24]

    return render(request, "pages/home.html", {
        "categories": categories,
        "sub_categories": sub_categories,
        "products": products,
        "featured_products": featured_products,
        "sale_products": sale_products,
    })


def menue_products(request, slug):
    menue = get_object_or_404(Menue, slug=slug)

    categories = Category.objects.filter(menue=menue).order_by("order")
    sub_categories = SubCategory.objects.all().order_by("order")

    products = Product.objects.select_related(
        "menue", "category", "subcategory"
    ).filter(menue=menue).order_by("order")

    return render(request, "pages/menue_products.html", {
        "menue": menue,
        "categories": categories,
        "sub_categories": sub_categories,
        "products": products,
        "featured_products": products.filter(is_featured=True)[:20],
        "sale_products": products[:24],
    })


def category_products(request, menue_slug, category_slug):
    menue = get_object_or_404(Menue, slug=menue_slug)

    category = get_object_or_404(
        Category,
        menue=menue,
        slug=category_slug
    )

    categories = Category.objects.filter(menue=menue).order_by("order")
    sub_categories = SubCategory.objects.all().order_by("order")

    products = Product.objects.select_related(
        "menue", "category", "subcategory"
    ).filter(menue=menue, category=category).order_by("order")

    return render(request, "pages/category_products.html", {
        "menue": menue,
        "category": category,
        "categories": categories,
        "sub_categories": sub_categories,
        "products": products,
    })


def subcategory_products(request, subcategory_slug):
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug)

    products = Product.objects.select_related(
        "menue", "category", "subcategory"
    ).filter(subcategory=subcategory).order_by("order")

    return render(request, "pages/products.html", {
        "subcategory": subcategory,
        "sub_categories": SubCategory.objects.all().order_by("order"),
        "products": products,
    })


@login_required
def cart_page(request):
    cart_items = Cart.objects.select_related(
        "product",
        "product__menue",
        "product__category",
        "product__subcategory"
    ).filter(user=request.user)

    subtotal = Decimal("0")
    total_items = 0

    for item in cart_items:
        subtotal += item.item_total
        total_items += item.quantity

    delivery_charge = Decimal("80") if subtotal > 0 else Decimal("0")
    discount_total = Decimal("0")
    total = subtotal + delivery_charge - discount_total

    return render(request, "pages/cart.html", {
        "cart_items": cart_items,
        "cart_count": total_items,
        "subtotal": subtotal,
        "discount_total": discount_total,
        "delivery_charge": delivery_charge,
        "total": total,
    })


def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "login_required",
            "success": False,
            "message": "Please login first to add product to cart.",
            "login_url": "/login/"
        })

    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={"quantity": 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = sum(
        item.quantity for item in Cart.objects.filter(user=request.user)
    )

    return JsonResponse({
        "status": "success",
        "success": True,
        "cart_count": cart_count,
        "message": "Product added to cart successfully."
    })


@login_required
def update_cart(request, product_id):
    cart_item = get_object_or_404(
        Cart,
        user=request.user,
        product_id=product_id
    )

    action = request.POST.get("action")

    if action == "increase":
        cart_item.quantity += 1
        cart_item.save()

    elif action == "decrease":
        cart_item.quantity -= 1

        if cart_item.quantity <= 0:
            cart_item.delete()
        else:
            cart_item.save()

    return redirect("pages:cart")


@login_required
def remove_cart_item(request, product_id):
    Cart.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    return redirect("pages:cart")


@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect("pages:cart")


@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.select_related(
        "product",
        "product__menue",
        "product__category",
        "product__subcategory"
    ).filter(user=request.user)

    return render(request, "pages/wishlist.html", {
        "wishlist_items": wishlist_items
    })

def add_to_wishlist(request, product_id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "status": "login_required",
            "success": False,
            "message": "Please login first to add product to wishlist.",
            "login_url": "/login/"
        })

    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse({
        "status": "success",
        "success": True,
        "in_wishlist": True,
        "wishlist_count": wishlist_count,
        "message": "Product added to wishlist."
    })


@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return JsonResponse({
        "status": "success",
        "success": True,
        "in_wishlist": False,
        "wishlist_count": wishlist_count,
        "message": "Removed from wishlist."
    })


@login_required
def clear_wishlist(request):
    Wishlist.objects.filter(user=request.user).delete()

    return JsonResponse({
        "status": "success",
        "success": True,
        "wishlist_count": 0
    })


def quick_view_product(request, slug):
    product = get_object_or_404(Product, slug=slug)

    return render(request, "pages/quick_view.html", {
        "id": product.id,
        "sku": product.sku or "",
        "name": product.name,
        "description": product.short_description or "",
        "image": product.image.url if product.image else "",
        "price": f"{product.final_price:.2f}",
        "old_price": f"{product.regular_price:.2f}",
        "metal": product.menue.get_name_display() if product.menue else "",
        "weight": product.weight,
        "stock": product.stock,
        "category": product.category.get_name_display() if product.category else "",
        "subcategory": product.subcategory.name if product.subcategory else "",
        "price_per_gram": f"{product.price_per_gram:.2f}",
        "add_cart_url": f"/add-to-cart/{product.id}/",
        "wishlist_url": f"/wishlist/add/{product.id}/",
        "checkout_url": "/checkout/",
        "next_url": request.GET.get("next", "/"),
    })



@login_required
def checkout_view(request):

    cart_items = Cart.objects.select_related(
        "product",
        "product__category",
        "product__subcategory",
        "product__menue"
    ).filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("pages:cart")

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    subtotal = Decimal("0")
    total_items = 0

    for item in cart_items:
        subtotal += item.item_total
        total_items += item.quantity

    delivery_charge = Decimal("80")
    discount = Decimal("0")
    total = subtotal + delivery_charge - discount

    if request.method == "POST":

        payment_method = request.POST.get("payment_method")

        payment_method_map = {
            "cod": 1,
            "bkash": 2,
            "nagad": 3,
            "card": 4,
        }

        # save latest address into profile
        profile.phone = request.POST.get("phone", "")
        profile.city = request.POST.get("city", "")
        profile.area = request.POST.get("area", "")
        profile.zip_code = request.POST.get("zip_code", "")
        profile.address = request.POST.get("address", "")
        profile.save()

        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email"),
            city=request.POST.get("city"),
            area=request.POST.get("area"),
            zip_code=request.POST.get("zip_code"),
            address=request.POST.get("address"),
            delivery_note=request.POST.get("delivery_note"),
            payment_method=payment_method_map.get(payment_method, 1),
            subtotal=subtotal,
            delivery_charge=delivery_charge,
            discount_amount=discount,
            total_amount=total,
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_sku=item.product.sku or "",
                product_image=item.product.image,
                quantity=item.quantity,
                weight=item.product.weight or 0,
                price=item.product.final_price,
                total_price=item.item_total,
            )

        cart_items.delete()

        messages.success(request, "Order placed successfully.")
        return redirect("pages:orders")

    return render(request, "pages/checkout.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "delivery_charge": delivery_charge,
        "discount": discount,
        "total": total,
        "total_items": total_items,
        "profile": profile,
    })