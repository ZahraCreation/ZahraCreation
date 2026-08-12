from django.urls import path

from . import views


app_name = "orders"


urlpatterns = [
    path(
        "",
        views.my_orders,
        name="my_orders",
    ),

    path(
        "<str:order_id>/",
        views.order_detail,
        name="order_detail",
    ),

    path(
        "<str:order_id>/track/",
        views.track_order,
        name="track_order",
    ),
]