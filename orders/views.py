from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Order


@login_required
def my_orders(request):
    """
    Show all orders belonging to the logged-in customer.
    """
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        "items"
    )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders,
        },
    )


@login_required
def order_detail(request, order_id):
    """
    Show complete details for one order.
    Customers can only access their own orders.
    """
    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        order_id=order_id,
        user=request.user,
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
        },
    )


@login_required
def track_order(request, order_id):
    """
    Show the delivery progress of an order.
    """
    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        order_id=order_id,
        user=request.user,
    )

    tracking_steps = [
        {
            "key": "pending",
            "label": "Order Placed",
            "description": "Your order has been received.",
        },
        {
            "key": "confirmed",
            "label": "Order Confirmed",
            "description": "Your order has been confirmed.",
        },
        {
            "key": "packed",
            "label": "Packed",
            "description": "Your order has been packed and is ready to ship.",
        },
        {
            "key": "shipped",
            "label": "Shipped",
            "description": "Your order is on its way.",
        },
        {
            "key": "delivered",
            "label": "Delivered",
            "description": "Your order has been delivered.",
        },
    ]

    status_order = [
        "pending",
        "confirmed",
        "packed",
        "shipped",
        "delivered",
    ]

    current_status = order.order_status

    if current_status == "cancelled":
        current_index = -1
    else:
        try:
            current_index = status_order.index(current_status)
        except ValueError:
            current_index = 0

    for index, step in enumerate(tracking_steps):

        step["completed"] = (
            current_status != "cancelled"
            and index <= current_index
        )

        step["current"] = (
            current_status != "cancelled"
            and index == current_index
        )

    return render(
        request,
        "orders/track_order.html",
        {
            "order": order,
            "tracking_steps": tracking_steps,
            "current_index": current_index,
        },
    )