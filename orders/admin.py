from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    readonly_fields = (
        "product_name",
        "price",
        "quantity",
        "total",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    # -----------------------------
    # ORDER LIST
    # -----------------------------

    list_display = (
        "order_id",
        "customer_name",
        "phone",
        "total",
        "payment_method",
        "payment_status",
        "order_status",
        "tracking_number",
        "created_at",
    )

    list_filter = (
        "order_status",
        "payment_status",
        "payment_method",
        "created_at",
    )

    search_fields = (
        "order_id",
        "customer_name",
        "email",
        "phone",
        "tracking_number",
        "courier_name",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    # -----------------------------
    # READ ONLY FIELDS
    # -----------------------------

    readonly_fields = (
        "order_id",
        "created_at",
        "updated_at",
    )

    # -----------------------------
    # ORDER FORM SECTIONS
    # -----------------------------

    fieldsets = (

        (
            "Order Information",
            {
                "fields": (
                    "order_id",
                    "user",
                    "customer_name",
                    "email",
                    "phone",
                )
            },
        ),

        (
            "Delivery Address",
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "pincode",
                )
            },
        ),

        (
            "Payment",
            {
                "fields": (
                    "payment_method",
                    "payment_status",
                )
            },
        ),

        (
            "Order Status",
            {
                "fields": (
                    "order_status",
                )
            },
        ),

        (
            "Shipping & Tracking",
            {
                "fields": (
                    "courier_name",
                    "tracking_number",
                    "shipped_at",
                    "delivered_at",
                )
            },
        ),

        (
            "Price",
            {
                "fields": (
                    "subtotal",
                    "shipping",
                    "total",
                )
            },
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    # -----------------------------
    # ORDER ITEMS
    # -----------------------------

    inlines = [
        OrderItemInline,
    ]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "product_name",
        "order",
        "price",
        "quantity",
        "total",
    )

    search_fields = (
        "product_name",
        "order__order_id",
    )

    list_filter = (
        "order__order_status",
    )

    ordering = (
        "-order__created_at",
    )