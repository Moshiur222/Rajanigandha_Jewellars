from django.db import models
from decimal import Decimal
from .utils import *


class Menue(models.Model):

    MENU_TYPES = (
        (1, "Gold"),
        (2, "Diamond"),
        (3, "Silver"),
        (4, "Platinum"),
        (5, "Pearl"),
        (6, "Gemstone"),
    )

    name = models.PositiveIntegerField(
        choices=MENU_TYPES,
        unique=True
    )
    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True, blank=True, max_length=255)
    order = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-id"]

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = generate_order(self)

        if not self.slug:
            self.slug = generate_unique_slug(self, self.get_name_display())

        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_name_display()


class Category(models.Model):

    CATEGORY_TYPES = (

        # Gold/ Silver
        (1, "22K"),
        (2, "21K"),
        (3, "18K"),
        (4, "Traditional"),

        # Diamond
        (5, "Natural Diamond"),
        (6, "Lab Grown Diamond"),
        (7, "Polki Diamond"),
        (8, "American Diamond"),
        (9, "Bridal Diamond"),

        # Platinum
        (10, "950 Platinum"),
        (11, "900 Platinum"),
        (12, "Platinum Bridal"),
        (13, "Couple Band Platinum"),

        # Pearl
        (14, "Freshwater Pearl"),
        (15, "Natural Pearl"),
        (16, "Cultured Pearl"),
        (17, "South Sea Pearl"),

        # Gemstone
        (18, "Ruby"),
        (19, "Emerald"),
        (20, "Sapphire"),
        (21, "Topaz"),
        (22, "Opal"),
        (23, "Amethyst"),
    )

    menue = models.ForeignKey(Menue,on_delete=models.CASCADE,related_name="categories", null=True)

    name = models.PositiveIntegerField(choices=CATEGORY_TYPES)
    is_visible = models.BooleanField(default=True)

    slug = models.SlugField(unique=True,blank=True,max_length=255)

    order = models.PositiveIntegerField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    price_per_gram = models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)

    class Meta:
        ordering = ["order", "-id"]
        unique_together = ("menue", "name")

    def save(self, *args, **kwargs):

        if self.order is None:
            self.order = generate_order(self)

        if not self.slug:
            self.slug = generate_unique_slug(
                self,
                f"{self.menue.get_name_display()}-{self.get_name_display()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.menue.get_name_display()} - {self.get_name_display()}"


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=255)
    order = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-id"]

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = generate_order(self)

        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    menue = models.ForeignKey(
        Menue,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True
    )

    slug = models.SlugField(unique=True, blank=True, max_length=255)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="products"
    )

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to="products/")

    manual_price_per_gram = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    is_auto_update_price = models.BooleanField(default=True)

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Weight in gram",
        null=True,
        blank=True
    )

    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    short_description = models.TextField(blank=True)

    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    order = models.PositiveIntegerField(blank=True, null=True)

    making_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-id"]

    @property
    def price_per_gram(self):
        if self.is_auto_update_price:
            if self.category and self.category.price_per_gram:
                return self.category.price_per_gram

        if self.manual_price_per_gram:
            return self.manual_price_per_gram

        return Decimal("0")

    @property
    def regular_price(self):
        if self.weight:
            return self.weight * self.price_per_gram
        return Decimal("0")

    @property
    def discount_amount(self):
        return Decimal("0")

    @property
    def final_price(self):
        return self.regular_price + self.making_charges + self.vat - self.discount_amount

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = generate_order(self)

        if not self.slug:
            self.slug = generate_unique_slug(self, self.name)

        if not self.sku:
            self.sku = generate_sku(self, prefix="RA", start=1000)

        if self.image:
            self.image = compress_image(self.image)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    @property
    def item_total(self):
        return self.product.final_price * self.quantity

    def __str__(self):
        return f"{self.user} - {self.product.name}"


class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} - {self.product.name}"
    



class Order(models.Model):

    ORDER_STATUS = (
        (1, "Pending"),
        (2, "Confirmed"),
        (3, "Processing"),
        (4, "Shipped"),
        (5, "Delivered"),
        (6, "Cancelled"),
    )

    PAYMENT_METHODS = (
        (1, "Cash On Delivery"),
        (2, "bKash"),
        (3, "Nagad"),
        (4, "Card"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    order_id = models.CharField(
        max_length=50,
        unique=True,
        blank=True
    )

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, blank=True)

    address = models.TextField()
    delivery_note = models.TextField(blank=True)

    payment_method = models.PositiveIntegerField(
        choices=PAYMENT_METHODS,
        default=1
    )

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.PositiveIntegerField(
        choices=ORDER_STATUS,
        default=1
    )

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.order_id:
            last_order = Order.objects.order_by("-id").first()

            if last_order:
                next_number = last_order.id + 1001
            else:
                next_number = 1001

            self.order_id = f"ORD{next_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items"
    )

    product_name = models.CharField(max_length=255)

    product_sku = models.CharField(
        max_length=100,
        blank=True
    )

    product_image = models.ImageField(
        upload_to="orders/products/",
        blank=True,
        null=True
    )

    quantity = models.PositiveIntegerField(default=1)

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.order_id} - {self.product_name}"


class Profile(models.Model):

    GENDER_CHOICES = (
        (1, "Male"),
        (2, "Female"),
        (3, "Other"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    alternate_phone = models.CharField(
        max_length=20,
        blank=True
    )

    gender = models.PositiveIntegerField(
        choices=GENDER_CHOICES,
        blank=True,
        null=True
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    area = models.CharField(
        max_length=100,
        blank=True
    )

    zip_code = models.CharField(
        max_length=20,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.user.email
    



class Vision(models.Model):

    title = models.CharField(max_length=50)

    image = models.ImageField(
        upload_to="media/",
        null=True,
        blank=True
    )

    descriptions = models.TextField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if self.image:

            img = Image.open(self.image)

            # RGBA FIX
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output = BytesIO()

            quality = 95

            # KEEP ORIGINAL RESOLUTION
            width, height = img.size

            while quality >= 20:

                output.seek(0)
                output.truncate()

                img.save(
                    output,
                    format="WEBP",
                    quality=quality,
                    method=6
                )

                size_kb = output.tell() / 1024

                if size_kb <= 30:
                    break

                quality -= 5

            output.seek(0)

            file_name = (
                self.image.name.split(".")[0]
                + ".webp"
            )

            self.image = ContentFile(
                output.read(),
                name=file_name
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Mission(models.Model):

    title = models.CharField(max_length=50)

    image = models.ImageField(
        upload_to="media/",
        null=True,
        blank=True
    )

    descriptions = models.TextField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if self.image:

            img = Image.open(self.image)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            output = BytesIO()

            quality = 95

            while quality >= 20:

                output.seek(0)
                output.truncate()

                img.save(
                    output,
                    format="WEBP",
                    quality=quality,
                    method=6
                )

                size_kb = output.tell() / 1024

                if size_kb <= 30:
                    break

                quality -= 5

            output.seek(0)

            file_name = (
                self.image.name.split(".")[0]
                + ".webp"
            )

            self.image = ContentFile(
                output.read(),
                name=file_name
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    


# =========================
# ALBUM
# =========================
from django.db import models
from django.utils.text import slugify

class PhotoAlbum(models.Model):
    title = models.CharField(max_length=120)

    cover_image = models.ImageField(upload_to="albums/")

    slug = models.SlugField(unique=True, blank=True)

    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while PhotoAlbum.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if self.cover_image:
            self.cover_image = optimize_image(self.cover_image)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# =========================
# GALLERY
# =========================

from django.db import models
from django.utils.text import slugify


class PhotoGallery(models.Model):

    album = models.ForeignKey(
        PhotoAlbum,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    title = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    image = models.ImageField(
        upload_to="gallery/"
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order", "-id"]

    def save(self, *args, **kwargs):

        if not self.slug:

            if self.title:
                base_slug = slugify(self.title)
            else:
                base_slug = slugify(self.album.title)

            slug = base_slug
            counter = 1

            while PhotoGallery.objects.filter(
                slug=slug
            ).exclude(
                pk=self.pk
            ).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if self.image:

            self.image = optimize_image(
                self.image
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.album.title


# =========================
# IMAGE OPTIMIZER
# =========================

def optimize_image(image_field):

    img = Image.open(image_field)

    # RGBA FIX
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # KEEP ORIGINAL SIZE
    width, height = img.size

    output = BytesIO()

    quality = 95

    while quality >= 20:

        output.seek(0)
        output.truncate()

        img.save(
            output,
            format="WEBP",
            quality=quality,
            method=6,
            optimize=True
        )

        size_kb = output.tell() / 1024

        if size_kb <= 50:
            break

        quality -= 5

    output.seek(0)

    file_name = (
        image_field.name.split(".")[0]
        + ".webp"
    )

    return ContentFile(
        output.read(),
        name=file_name
    )


from urllib.parse import urlparse, parse_qs


class VideoGallery(models.Model):
    """Model for storing YouTube video references"""
    
    title = models.CharField(max_length=200)
    youtube_url = models.URLField(max_length=500, unique=True)
    youtube_id = models.CharField(max_length=20, blank=True, editable=False)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Video"
        verbose_name_plural = "Videos"
    
    def save(self, *args, **kwargs):
        # Extract YouTube video ID from URL
        self.youtube_id = self.extract_youtube_id()
        
        # Auto-set order if not specified
        if not self.order:
            last_order = VideoGallery.objects.aggregate(
                models.Max('order')
            )['order__max']
            self.order = (last_order or 0) + 1
        
        super().save(*args, **kwargs)
    
    def extract_youtube_id(self):
        """Extract YouTube video ID from various URL formats"""
        if not self.youtube_url:
            return ''
        
        url = self.youtube_url.strip()
        
        # Pattern 1: https://www.youtube.com/watch?v=VIDEO_ID
        # Pattern 2: https://youtu.be/VIDEO_ID
        # Pattern 3: https://www.youtube.com/embed/VIDEO_ID
        # Pattern 4: https://www.youtube.com/v/VIDEO_ID
        # Pattern 5: https://www.youtube.com/shorts/VIDEO_ID
        
        patterns = [
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?youtu\.be\/([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
            r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        # Try to parse as query parameter
        try:
            parsed = urlparse(url)
            if 'youtube.com' in parsed.netloc:
                params = parse_qs(parsed.query)
                if 'v' in params:
                    return params['v'][0]
        except:
            pass
        
        return ''
    
    @property
    def youtube_embed_url(self):
        """Generate embed URL for iframe"""
        if self.youtube_id:
            return f"https://www.youtube.com/embed/{self.youtube_id}"
        return ''
    
    @property
    def youtube_thumbnail_url(self):
        """Generate thumbnail URL"""
        if self.youtube_id:
            return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"
        return ''
    
    @property
    def youtube_watch_url(self):
        """Generate watch URL"""
        if self.youtube_id:
            return f"https://www.youtube.com/watch?v={self.youtube_id}"
        return self.youtube_url
    
    def __str__(self):
        return self.title