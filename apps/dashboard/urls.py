from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path("logout/",views.logout_view,name="logout"),
    path('products/', views.admin_products, name='products'),
    path('products/add/', views.admin_product_form, name='product_add'),
    path('products/update/<int:id>/', views.admin_product_form, name='product_update'),
    path("products/update-order/",views.update_product_order,name="update_product_order"),
    path('category/', views.admin_category, name='category'),
    path("category/update-order/", views.update_category_order, name="update_category_order"),
    path('sub-category/', views.admin_sub_category, name='sub_category'),
    path("sub-category/update-order/", views.update_sub_category_order, name="update_sub_category_order"),
    path('orders/', views.admin_orders, name='orders'),
    path("orders/update-status/<int:order_id>/",views.update_order_status,name="update_order_status"),
    path('customers/', views.admin_customers, name='customers'),
    path('offers/', views.admin_offers, name='offers'),
    path('stores/', views.admin_stores, name='stores'),
    path("menue/", views.admin_menue, name="menue"),
    path("menue/order/", views.update_menue_order, name="menue_order"),
    path("profile/", views.admin_profile, name="profile"),
    path("settings/", views.admin_settings, name="settings"),
]
