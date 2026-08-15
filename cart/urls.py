from django.urls import path

from . import views


app_name = "cart"


urlpatterns = [
    path(
        "",
        views.cart_detail,
        name="detail",
    ),

    path(
        "add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),

    path(
        "increase/<int:product_id>/",
        views.increase_quantity,
        name="increase",
    ),

    path(
        "decrease/<int:product_id>/",
        views.decrease_quantity,
        name="decrease",
    ),

    path(
        "remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove",
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),
]