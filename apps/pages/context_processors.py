from django.db.models import Prefetch, Sum
from .models import Menue, Category, Cart, Wishlist


def nav_item(request):
    menues = Menue.objects.filter(is_visible=True).prefetch_related(
        Prefetch(
            "categories",
            queryset=Category.objects.filter(is_visible=True).order_by("order"),
            to_attr="visible_categories"
        )
    )

    return {
        "menues": menues,
    }


def cart_context(request):
    cart_count = 0

    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(
            user=request.user
        ).aggregate(
            total=Sum("quantity")
        )["total"] or 0

    return {
        "cart_count": cart_count,
    }


def wishlist_context(request):
    wishlist_count = 0

    if request.user.is_authenticated:
        wishlist_count = Wishlist.objects.filter(
            user=request.user
        ).count()

    return {
        "wishlist_count": wishlist_count,
    }