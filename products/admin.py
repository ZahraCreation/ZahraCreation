from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "slug",
    )

    prepopulated_fields = {
        "slug": ("name",),
    }

    ordering = (
        "name",
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

    fields = (
        "image",
        "preview",
        "alt_text",
        "is_primary",
    )

    readonly_fields = (
        "preview",
    )

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" '
                'style="object-fit:cover;border-radius:10px;" />',
                obj.image.url,
            )

        return "No image"

    preview.short_description = "Preview"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    # --------------------------------------------------
    # PRODUCT LIST
    # --------------------------------------------------

    list_display = (
        "product_preview",
        "name",
        "category",
        "price_display",
        "discount_display",
        "stock_display",
        "status_display",
        "is_featured",
        "is_active",
    )

    list_filter = (
        "category",
        "is_featured",
        "is_active",
    )

    search_fields = (
        "name",
        "sku",
        "slug",
    )

    ordering = (
        "-created_at",
    )

    # --------------------------------------------------
    # AUTOMATIC SLUG
    # --------------------------------------------------

    prepopulated_fields = {
        "slug": ("name",),
    }

    # --------------------------------------------------
    # PRODUCT FORM
    # --------------------------------------------------

    fieldsets = (
        (
            "👜 Product Information",
            {
                "fields": (
                    "name",
                    "category",
                    "sku",
                    "slug",
                )
            },
        ),

        (
            "🖼️ Product Image",
            {
                "fields": (
                    "main_image",
                )
            },
        ),

        (
            "💰 Price & Stock",
            {
                "fields": (
                    "price",
                    "discount_percentage",
                    "stock",
                )
            },
        ),

        (
            "✨ Product Description",
            {
                "fields": (
                    "short_description",
                    "description",
                )
            },
        ),

        (
            "⭐ Store Settings",
            {
                "fields": (
                    "is_featured",
                    "is_active",
                )
            },
        ),

        (
            "📊 Sales Information",
            {
                "fields": (
                    "sales_count",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
    )

    readonly_fields = (
        "sales_count",
    )

    inlines = (
        ProductImageInline,
    )

    # --------------------------------------------------
    # IMAGE PREVIEW
    # --------------------------------------------------

    @admin.display(
        description="Image"
    )
    def product_preview(self, obj):

        if obj.main_image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit:cover;border-radius:12px;" />',
                obj.main_image.url,
            )

        return format_html(
            '<span style="color:#999;">No image</span>'
        )

    # --------------------------------------------------
    # PRICE
    # --------------------------------------------------

    @admin.display(
        description="Price",
        ordering="price",
    )
    def price_display(self, obj):

        return format_html(
            '<strong>₹{}</strong>',
            obj.price,
        )

    # --------------------------------------------------
    # DISCOUNT
    # --------------------------------------------------

    @admin.display(
        description="Discount"
    )
    def discount_display(self, obj):

        if obj.discount_percentage > 0:
            return format_html(
                '<span style="color:#b76e79;font-weight:600;">'
                '{}% OFF'
                '</span>',
                obj.discount_percentage,
            )

        return format_html(
            '<span style="color:#999;">No discount</span>'
        )

    # --------------------------------------------------
    # STOCK
    # --------------------------------------------------

    @admin.display(
        description="Stock",
        ordering="stock",
    )
    def stock_display(self, obj):

        if obj.stock <= 0:
            return format_html(
                '<span style="color:#c0392b;font-weight:700;">'
                'OUT OF STOCK'
                '</span>'
            )

        if obj.stock <= 5:
            return format_html(
                '<span style="color:#d68910;font-weight:700;">'
                'LOW STOCK ({})'
                '</span>',
                obj.stock,
            )

        return format_html(
            '<span style="color:#2e7d32;font-weight:600;">'
            '{} in stock'
            '</span>',
            obj.stock,
        )

    # --------------------------------------------------
    # PRODUCT STATUS
    # --------------------------------------------------

    @admin.display(
        description="Status"
    )
    def status_display(self, obj):

        if not obj.is_active:
            return format_html(
                '<span style="color:#777;font-weight:600;">'
                'HIDDEN'
                '</span>'
            )

        if obj.stock <= 0:
            return format_html(
                '<span style="color:#c0392b;font-weight:700;">'
                'SOLD OUT'
                '</span>'
            )

        return format_html(
            '<span style="color:#2e7d32;font-weight:700;">'
            'AVAILABLE'
            '</span>'
        )