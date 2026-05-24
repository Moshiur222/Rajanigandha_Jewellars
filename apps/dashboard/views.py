import json
from functools import wraps
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import (render,redirect,get_object_or_404,)
from apps.pages.models import (Menue,Category,SubCategory,Product,Order)
from apps.dashboard.models import (User)
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.pages.models import *
from apps.pages.utils import *


# ======================================================
# ADMIN DECORATOR
# ======================================================



def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logout successful"
    )

    return redirect("pages:login")


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # LOGIN REQUIRED
        if not request.user.is_authenticated:

            messages.error(
                request,
                "Please login first"
            )

            return redirect("pages:login")

        # ONLY ADMIN
        if request.user.user_type != 1:

            messages.error(
                request,
                "Access denied"
            )

            return redirect("pages:home")

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper


# ======================================================
# AUTH
# ======================================================

def login_view(request):

    if request.user.is_authenticated:

        if request.user.user_type == 1:
            return redirect("dashboard:home")

        return redirect("pages:home")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            login(request, user)

            # ADMIN
            if user.user_type == 1:
                return redirect("dashboard:home")

            # MEMBER
            return redirect("pages:home")

        else:

            messages.error(
                request,
                "Invalid email or password"
            )

    return render(
        request,
        "pages/login.html"
    )


# ======================================================
# DASHBOARD HOME
# ======================================================


@admin_required
def dashboard_home(request):
    today = timezone.now().date()
    last_7_days = today - timedelta(days=6)

    total_users = User.objects.filter(user_type=2).count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status=5).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    pending_orders = Order.objects.filter(status=1).count()
    delivered_orders = Order.objects.filter(status=5).count()
    cancelled_orders = Order.objects.filter(status=6).count()

    recent_orders = Order.objects.prefetch_related("items").order_by("-id")[:5]

    top_products = OrderItem.objects.values(
        "product_id",
        "product_name"
    ).annotate(
        total_sales=Sum("quantity"),
        total_amount=Sum("total_price")
    ).order_by("-total_sales")[:5]

    chart_labels = []
    chart_sales = []

    for i in range(7):
        day = last_7_days + timedelta(days=i)

        daily_total = Order.objects.filter(
            created_at__date=day
        ).aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        chart_labels.append(day.strftime("%d %b"))
        chart_sales.append(float(daily_total))

    context = {
        "total_users": total_users,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
        "recent_orders": recent_orders,
        "top_products": top_products,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
        "chart_labels": chart_labels,
        "chart_sales": chart_sales,
    }

    return render(request, "admin/pages/dashboard.html", context)

# ======================================================
# PROFILE
# ======================================================

@admin_required
def admin_profile(request):

    if request.method == "POST":

        user = request.user

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")

        user.save()

        messages.success(
            request,
            "Profile updated successfully"
        )

        return redirect("dashboard:profile")

    return render(
        request,
        "admin/pages/profile.html"
    )


# ======================================================
# SETTINGS
# ======================================================

@admin_required
def admin_settings(request):

    if request.method == "POST":

        messages.success(
            request,
            "Settings updated successfully"
        )

        return redirect("dashboard:settings")

    return render(
        request,
        "admin/pages/settings.html"
    )


# ======================================================
# MENUE
# ======================================================

@admin_required
def admin_menue(request):

    edit_menue = None

    if request.GET.get("edit"):

        edit_menue = get_object_or_404(
            Menue,
            id=request.GET.get("edit")
        )

    if request.method == "POST":

        action = request.POST.get("action")
        menue_id = request.POST.get("menue_id")

        # CREATE
        if action == "create":

            name = request.POST.get("name")

            is_visible = (
                True
                if request.POST.get("is_visible")
                else False
            )

            if name:

                Menue.objects.create(
                    name=int(name),
                    is_visible=is_visible,
                )

        # UPDATE
        elif action == "update":

            menue = get_object_or_404(
                Menue,
                id=menue_id
            )

            menue.name = int(
                request.POST.get("name")
            )

            menue.is_visible = (
                True
                if request.POST.get("is_visible")
                else False
            )

            menue.save()

        # DELETE
        elif action == "delete":

            menue = get_object_or_404(
                Menue,
                id=menue_id
            )

            menue.delete()

        return redirect("dashboard:menue")

    menues = Menue.objects.all()

    return render(
        request,
        "admin/pages/menue.html",
        {
            "menues": menues,
            "edit_menue": edit_menue,
            "menu_types": Menue.MENU_TYPES,
        }
    )


@admin_required
def update_menue_order(request):

    if request.method == "POST":

        data = json.loads(request.body)

        for index, item in enumerate(data):

            Menue.objects.filter(
                id=item["id"]
            ).update(
                order=index + 1
            )

        return JsonResponse({
            "status": "success"
        })

    return JsonResponse({
        "status": "failed"
    })


# ======================================================
# CATEGORY
# ======================================================

@admin_required
def admin_category(request):

    edit_category = None

    if request.GET.get("edit"):

        edit_category = get_object_or_404(
            Category,
            id=request.GET.get("edit")
        )

    if request.method == "POST":

        action = request.POST.get("action")
        category_id = request.POST.get("category_id")

        # CREATE
        if action == "create":

            menue = get_object_or_404(
                Menue,
                id=request.POST.get("menue")
            )

            name = request.POST.get("name")

            is_visible = (
                True
                if request.POST.get("is_visible")
                else False
            )

            if name:

                category = Category.objects.create(
                    menue=menue,
                    name=int(name),
                    is_visible=is_visible,
                )

                # GOLD
                if menue.name == 1:
                    update_gold_prices()

                # SILVER
                elif menue.name == 3:
                    update_silver_prices()

        # UPDATE
        elif action == "update":

            category = get_object_or_404(
                Category,
                id=category_id
            )

            category.menue = get_object_or_404(
                Menue,
                id=request.POST.get("menue")
            )

            category.name = int(
                request.POST.get("name")
            )

            category.is_visible = (
                True
                if request.POST.get("is_visible")
                else False
            )

            category.save()

            # GOLD
            if category.menue.name == 1:
                update_gold_prices()

            # SILVER
            elif category.menue.name == 3:
                update_silver_prices()

        # DELETE
        elif action == "delete":

            category = get_object_or_404(
                Category,
                id=category_id
            )

            category.delete()

        return redirect("dashboard:category")

    categories = Category.objects.select_related(
        "menue"
    ).all()

    menues = Menue.objects.filter(
        is_visible=True
    )

    return render(
        request,
        "admin/pages/category.html",
        {
            "categories": categories,
            "menues": menues,
            "edit_category": edit_category,
            "category_types": Category.CATEGORY_TYPES,
        }
    )


@admin_required
def update_category_order(request):

    if request.method == "POST":

        data = json.loads(request.body)

        for index, item in enumerate(data):

            Category.objects.filter(
                id=item["id"]
            ).update(
                order=index
            )

        return JsonResponse({
            "status": "success"
        })

    return JsonResponse({
        "status": "failed"
    })


# ======================================================
# SUB CATEGORY
# ======================================================

@admin_required
def admin_sub_category(request):

    edit_sub_category = None

    if request.GET.get("edit"):

        edit_sub_category = get_object_or_404(
            SubCategory,
            id=request.GET.get("edit")
        )

    if request.method == "POST":

        action = request.POST.get("action")

        sub_category_id = request.POST.get(
            "sub_category_id"
        )

        name = request.POST.get("name")

        # CREATE
        if action == "create":

            if name:

                SubCategory.objects.create(
                    name=name
                )

        # UPDATE
        elif action == "update":

            sub_category = get_object_or_404(
                SubCategory,
                id=sub_category_id
            )

            sub_category.name = name

            sub_category.save()

        # DELETE
        elif action == "delete":

            sub_category = get_object_or_404(
                SubCategory,
                id=sub_category_id
            )

            sub_category.delete()

        return redirect(
            "dashboard:sub_category"
        )

    sub_categories = SubCategory.objects.all().order_by(
        "order"
    )

    return render(
        request,
        "admin/pages/sub_category.html",
        {
            "sub_categories": sub_categories,
            "edit_sub_category": edit_sub_category,
        }
    )


@admin_required
def update_sub_category_order(request):

    if request.method == "POST":

        data = json.loads(request.body)

        for index, item in enumerate(data):

            SubCategory.objects.filter(
                id=item["id"]
            ).update(
                order=index
            )

        return JsonResponse({
            "status": "success"
        })

    return JsonResponse({
        "status": "failed"
    })


# ======================================================
# PRODUCTS
# ======================================================

@admin_required
def admin_products(request):

    products = Product.objects.select_related(
        "menue",
        "category",
        "subcategory"
    ).all().order_by(
        "order",
        "-id"
    )

    if request.method == "POST":

        product_id = request.POST.get(
            "product_id"
        )

        product = get_object_or_404(
            Product,
            id=product_id
        )

        product.delete()

        messages.success(
            request,
            "Product deleted successfully."
        )

        return redirect(
            "dashboard:products"
        )

    return render(
        request,
        "admin/pages/products.html",
        {
            "products": products,
        }
    )


@admin_required
def admin_product_form(request, id=None):

    product = None

    if id:

        product = get_object_or_404(
            Product,
            id=id
        )

    menues = Menue.objects.all().order_by(
        "order"
    )

    categories = Category.objects.all().order_by(
        "order"
    )

    sub_categories = SubCategory.objects.all().order_by(
        "order"
    )

    if request.method == "POST":

        if product is None:
            product = Product()

        product.name = request.POST.get("name")

        product.menue_id = request.POST.get(
            "menue"
        )

        product.category_id = request.POST.get(
            "category"
        )

        subcategory = request.POST.get(
            "subcategory"
        )

        product.subcategory_id = (
            subcategory
            if subcategory
            else None
        )

        product.weight = request.POST.get(
            "weight"
        )

        product.stock = (
            request.POST.get("stock")
            or 0
        )

        product.is_available = (
            request.POST.get("is_available") == "1"
        )

        product.is_auto_update_price = (
            request.POST.get("is_auto_update_price") == "on"
        )

        if product.is_auto_update_price:

            product.manual_price_per_gram = None

        else:

            product.manual_price_per_gram = (
                request.POST.get(
                    "manual_price_per_gram"
                ) or None
            )

        product.short_description = request.POST.get(
            "short_description"
        )

        product.is_featured = (
            request.POST.get("is_featured") == "on"
        )

        product.is_new_arrival = (
            request.POST.get("is_new_arrival") == "on"
        )

        product.is_best_seller = (
            request.POST.get("is_best_seller") == "on"
        )

        if request.FILES.get("image"):

            product.image = request.FILES.get(
                "image"
            )

        product.save()

        if id:

            messages.success(
                request,
                "Product updated successfully."
            )

        else:

            messages.success(
                request,
                "Product added successfully."
            )

        return redirect(
            "dashboard:products"
        )

    return render(
        request,
        "admin/pages/product_form.html",
        {
            "edit_product": product,
            "menues": menues,
            "categories": categories,
            "sub_categories": sub_categories,
        }
    )


@admin_required
def update_product_order(request):

    if request.method == "POST":

        data = json.loads(request.body)

        for index, item in enumerate(data):

            Product.objects.filter(
                id=item["id"]
            ).update(
                order=index
            )

        return JsonResponse({
            "status": "success"
        })

    return JsonResponse({
        "status": "failed"
    })


# ======================================================
# OTHERS
# ======================================================

@admin_required
def admin_orders(request):
    status = request.GET.get("status")
    search = request.GET.get("search")

    orders = Order.objects.prefetch_related(
        "items"
    ).select_related(
        "user"
    ).order_by("-id")

    if status:
        orders = orders.filter(status=status)

    if search:
        orders = orders.filter(order_id__icontains=search) | orders.filter(full_name__icontains=search) | orders.filter(phone__icontains=search)

    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status=1).count()
    delivered_orders = Order.objects.filter(status=5).count()
    cancelled_orders = Order.objects.filter(status=6).count()

    return render(request, "admin/pages/orders.html", {
        "orders": orders,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,
        "status": status,
        "search": search,
        "ORDER_STATUS": Order.ORDER_STATUS,
    })

@admin_required
def update_order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        status = request.POST.get("status")

        if status:
            order.status = int(status)
            order.save()

            messages.success(request, "Order status updated successfully.")

    return redirect("dashboard:orders")


@admin_required
def admin_customers(request):

    return render(
        request,
        "admin/pages/customers.html"
    )


@admin_required
def admin_offers(request):

    return render(
        request,
        "admin/pages/offers.html"
    )


@admin_required
def admin_stores(request):

    return render(
        request,
        "admin/pages/stores.html"
    )


# =========================
# MISSION
# =========================
@admin_required
def mission(request):

    return render(
        request,
        "admin/pages/mission.html"
    )


# =========================
# VISION
# =========================
@admin_required
def vision(request):

    return render(
        request,
        "admin/pages/vision.html"
    )


# =========================
# PHOTO ALBUM
# =========================
from django.contrib import messages
@admin_required
def photo_album(request):

    albums = PhotoAlbum.objects.all()

    return render(
        request,
        "admin/pages/photo_album.html",
        {
            "albums": albums
        }
    )

@admin_required
def photo_album_add(request):

    if request.method == "POST":

        title = request.POST.get("title")
        cover_image = request.FILES.get("cover_image")
        order = request.POST.get("order") or 0

        if not title or not cover_image:

            messages.error(
                request,
                "Title and Cover Image are required."
            )

            return redirect(
                "dashboard:photo_album_add"
            )

        PhotoAlbum.objects.create(
            title=title,
            cover_image=cover_image,
            order=order
        )

        messages.success(
            request,
            "Photo Album Added Successfully."
        )

        return redirect(
            "dashboard:photo_album"
        )

    return render(
        request,
        "admin/pages/album_form.html",
        {
            "album": None,
            "page_title": "Add Photo Album"
        }
    )

@admin_required
def photo_album_update(request, slug):

    album = get_object_or_404(
        PhotoAlbum,
        slug=slug
    )

    if request.method == "POST":

        album.title = request.POST.get("title")
        album.order = request.POST.get("order") or 0

        if request.FILES.get("cover_image"):

            album.cover_image = request.FILES.get(
                "cover_image"
            )

        album.slug = ""
        album.save()

        messages.success(
            request,
            "Photo Album Updated Successfully."
        )

        return redirect(
            "dashboard:photo_album"
        )

    return render(
        request,
        "admin/pages/album_form.html",
        {
            "album": album,
            "page_title": "Update Photo Album"
        }
    )

@admin_required
def photo_album_delete(request, slug):

    album = get_object_or_404(
        PhotoAlbum,
        slug=slug
    )

    album.delete()

    messages.success(
        request,
        "Photo Album Deleted Successfully."
    )

    return redirect(
        "dashboard:photo_album"
    )


# =========================
# PHOTO GALLERY
# =========================
@admin_required
def photo_gallery(request, slug):
    """Display photos in an album"""
    album = get_object_or_404(PhotoAlbum, slug=slug)
    photos = album.photos.all()
    
    context = {
        'album': album,
        'photos': photos,
    }
    
    return render(request, "admin/pages/photo_gallery.html", context)



from django.db.models import Max
@admin_required
def photo_gallery_add(request, slug):

    album = get_object_or_404(PhotoAlbum, slug=slug)

    if request.method == "POST":

        images = request.FILES.getlist("images")

        if not images:
            messages.error(request, "Please select at least one image.")
            return redirect("dashboard:photo_gallery", slug=album.slug)

        last_order = PhotoGallery.objects.filter(
            album=album
        ).aggregate(
            Max("order")
        )["order__max"] or 0

        success_count = 0

        for i, image in enumerate(images):

            PhotoGallery.objects.create(
                album=album,
                image=image,
                order=last_order + i + 1
            )

            success_count += 1

        messages.success(
            request,
            f'{success_count} photo{"s" if success_count > 1 else ""} added successfully!'
        )

        return redirect(
            "dashboard:photo_gallery",
            slug=album.slug
        )

    photos = album.photos.all()

    return render(
        request,
        "admin/pages/gallery_form.html",
        {
            "album": album,
            "photos": photos,
        }
    )

@admin_required
def photo_gallery_update(request, slug):
    """Update a photo's details"""
    photo = get_object_or_404(PhotoGallery, sluh=slug)
    album = photo.album
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        new_image = request.FILES.get("image")
        order = request.POST.get("order")
        
        if title:
            photo.title = title
        
        if new_image:
            # Delete old image
            if photo.image:
                photo.image.delete(save=False)
            photo.image = new_image
        
        if order:
            try:
                photo.order = int(order)
            except ValueError:
                pass
        
        photo.save()
        messages.success(request, "Photo updated successfully!")
        return redirect('dashboard:photo_gallery', slug=album.slug)
    
    context = {
        'photo': photo,
        'album': album,
    }
    
    return render(request, "admin/pages/photo_update.html", context)

@admin_required
def photo_gallery_delete(request, slug):

    photo = get_object_or_404(
        PhotoGallery,
        slug=slug
    )

    album = photo.album

    if photo.image:
        photo.image.delete(save=False)

    photo.delete()

    messages.success(
        request,
        "Photo deleted successfully!"
    )

    return redirect(
        "dashboard:photo_gallery",
        slug=album.slug
    )

# =========================
# VIDEO GALLERY
# =========================
@admin_required
def video_gallery(request):

    return render(
        request,
        "admin/pages/video_gallery.html"
    )




@admin_required
def video_gallery(request):
    """Display video gallery page with form and list"""
    videos = VideoGallery.objects.filter(is_active=True)
    
    context = {
        'videos': videos,
    }
    
    # If editing, include the video object
    video_id = request.GET.get('edit')
    if video_id:
        video = get_object_or_404(VideoGallery, pk=video_id)
        context['video'] = video
    
    return render(request, "admin/pages/video_gallery.html", context)


@admin_required
def video_add(request):
    """Add a new video"""
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        youtube_url = request.POST.get("youtube_url", "").strip()
        
        # Validation
        if not title:
            messages.error(request, "Please provide a video title.")
        elif not youtube_url:
            messages.error(request, "Please provide a YouTube URL.")
        elif VideoGallery.objects.filter(youtube_url=youtube_url).exists():
            messages.error(request, "This YouTube URL has already been added.")
        else:
            video = VideoGallery.objects.create(
                title=title,
                youtube_url=youtube_url
            )
            
            if video.youtube_id:
                messages.success(request, f'Video "{title}" added successfully!')
            else:
                messages.warning(
                    request, 
                    f'Video added, but the YouTube URL format may not be recognized. '
                )
            
            return redirect('dashboard:video_gallery')
    
    return  render(request, "admin/pages/video_gallery_form.html")


@admin_required
def video_update(request, pk):
    """Update an existing video"""
    video = get_object_or_404(VideoGallery, pk=pk)
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        youtube_url = request.POST.get("youtube_url", "").strip()
        
        if not title:
            messages.error(request, "Please provide a video title.")
        elif not youtube_url:
            messages.error(request, "Please provide a YouTube URL.")
        elif VideoGallery.objects.filter(youtube_url=youtube_url).exclude(pk=pk).exists():
            messages.error(request, "This YouTube URL has already been added.")
        else:
            video.title = title
            video.youtube_url = youtube_url
            video.save()
            
            if video.youtube_id:
                messages.success(request, f'Video "{title}" updated successfully!')
            else:
                messages.warning(request, 'Video updated, but the YouTube URL format may not be recognized.')
            
            return redirect('dashboard:video_gallery')
    
    # For GET request, redirect to gallery with edit parameter
    return  render(request, "admin/pages/video_gallery_form.html",{'video':video})


@admin_required
def video_delete(request, pk):
    """Delete a video"""
    video = get_object_or_404(VideoGallery, pk=pk)
    title = video.title
    
    video.delete()
    messages.success(request, f'Video "{title}" deleted successfully!')
    
    return redirect('dashboard:video_gallery')