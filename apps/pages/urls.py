from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
     path('', views.home, name='home'),
     path("login/", views.login_view, name="login"),
     path("profile/", views.profile_view, name="profile"),
     path("profile/orders/", views.order_view, name="orders"),
     path("settings/", views.settings_view, name="settings"),
     path("signup/", views.signup_view, name="signup"),
     path("verify-otp/", views.verify_otp_view, name="verify_otp"),
     path("resend-otp/", views.resend_otp_view, name="resend_otp"),
     path("change-email/", views.change_email_view, name="change_email"),
     path("cart/", views.cart_page, name="cart"),
     path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
     path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
     path("cart/remove/<int:product_id>/", views.remove_cart_item, name="remove_cart_item"),
     path("cart/clear/", views.clear_cart, name="clear_cart"),
     path("checkout/", views.checkout_view, name="checkout"),
     path("wishlist/",views.wishlist_page,name="wishlist"),
     path("wishlist/add/<int:product_id>/",views.add_to_wishlist,name="add_to_wishlist"),
     path("wishlist/remove/<int:product_id>/",views.remove_from_wishlist,name="remove_from_wishlist"),
     path("wishlist/clear/",views.clear_wishlist,name="clear_wishlist"),
     path("Jewllery/<slug:slug>/",views.menue_products,name="menue_products"),
     path("jewellery/<slug:menue_slug>/<slug:category_slug>/",views.category_products,name="category_products"),
     path("jewellery/<slug:subcategory_slug>/",views.subcategory_products,name="subcategory_products"),
     path("quick-view/<slug:slug>/",views.quick_view_product,name="quick_view_product"),
     path("contact/",views.contact,name="contact"),
]