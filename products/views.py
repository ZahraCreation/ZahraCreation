from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def home(request):
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True,
    ).select_related("category")

    new_arrivals = Product.objects.filter(
        is_active=True,
    ).select_related("category").order_by("-created_at")[:8]

    best_sellers = Product.objects.filter(
        is_active=True,
    ).select_related("category").order_by("-sales_count")[:8]

    categories = Category.objects.filter(
        is_active=True,
    )

    context = {
        "featured_products": featured_products,
        "new_arrivals": new_arrivals,
        "best_sellers": best_sellers,
        "categories": categories,
    }

    return render(request, "home.html", context)


def shop(request):
    products = Product.objects.filter(
        is_active=True,
    ).select_related("category")

    categories = Category.objects.filter(
        is_active=True,
    )

    search_query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "").strip()

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(sku__icontains=search_query)
        )

    if category_slug:
        products = products.filter(
            category__slug=category_slug
        )

    if sort == "price_low":
        products = products.order_by("price")

    elif sort == "price_high":
        products = products.order_by("-price")

    elif sort == "best_selling":
        products = products.order_by("-sales_count")

    else:
        products = products.order_by("-created_at")

    context = {
        "products": products,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_slug,
        "selected_sort": sort,
    }

    return render(request, "products/shop.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
    )

    product_images = product.images.all()

    related_products = Product.objects.filter(
        is_active=True,
        category=product.category,
    ).exclude(
        pk=product.pk,
    ).select_related(
        "category",
    ).order_by(
        "-created_at",
    )[:4]

    context = {
        "product": product,
        "product_images": product_images,
        "related_products": related_products,
    }

    return render(request, "products/product_detail.html", context)