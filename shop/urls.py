from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("promotions/halloween", views.halloween, name="halloween"),
    path("promotions/ceramic", views.ceramic, name="halloween"),
    path("promotions/sweets", views.sweets, name="halloween"),
    path("promotions/free-present", views.free_present, name="halloween"),
    path("categories/<slug:category_slug>", views.category, name="products_by_category"),
    path("<slug:category_slug>/<slug:product_slug>", views.product_description, name="product_description"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>", views.add_cart, name="add_cart"),
    path("cart/remove/<int:product_id>", views.cart_remove, name="cart_remove"),
    path("cart/delete/<int:product_id>", views.cart_delete, name="cart_delete"),
]
