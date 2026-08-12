from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Products / Shop
    path("", include("products.urls")),

    # Shopping Cart
    path("cart/", include("cart.urls")),

    # Orders / Checkout
    path("orders/", include("orders.urls")),
]


# Serve uploaded media files while developing
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )