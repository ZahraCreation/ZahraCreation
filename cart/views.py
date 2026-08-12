from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product


CART_SESSION_KEY = "cart"


def _get_cart(request):
    """
    Get the current shopping bag from the user's session.
    """
    return request.session.get(CART_SESSION_KEY, {})


def _save_cart(request, cart):
    """
    Save the shopping bag back into the session.
    """
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def _get_discounted_price(product):
    """
    Return the product price after applying its discount.
    """
    if product.discount_percentage > 0:
        discount = (
            product.price
            * product.discount_percentage
            / Decimal("100")
        )

        return product.price - discount

    return product.price


def _build_cart_items(request):
    """
    Build all valid cart items and calculate the subtotal.
    """

    cart = _get_cart(request)

    items = []
    subtotal = Decimal("0")

    if not cart:
        return items, subtotal

    products = Product.objects.filter(
        id__in=cart.keys(),
        is_active=True,
    ).select_related("category")

    product_map = {
        str(product.id): product
        for product in products
    }

    cleaned_cart = {}

    for product_id, quantity in cart.items():

        product = product_map.get(str(product_id))

        if product is None:
            continue

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            quantity = 1

        if quantity < 1:
            continue

        # Never allow the cart quantity
        # to be greater than available stock.
        if quantity > product.stock:
            quantity = product.stock

        # Product is out of stock.
        if quantity <= 0:
            continue

        unit_price = _get_discounted_price(product)

        item_total = unit_price * quantity

        subtotal += item_total

        cleaned_cart[str(product.id)] = quantity

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "price": unit_price,
                "unit_price": unit_price,
                "total": item_total,
            }
        )

    # Keep the session cart clean.
    if cleaned_cart != cart:
        _save_cart(request, cleaned_cart)

    return items, subtotal


def cart_detail(request):
    """
    Display the shopping bag.
    """

    items, subtotal = _build_cart_items(request)

    cart_count = sum(
        item["quantity"]
        for item in items
    )

    context = {
        "cart_items": items,
        "subtotal": subtotal,
        "total": subtotal,
        "cart_count": cart_count,
    }

    return render(
        request,
        "cart/cart.html",
        context,
    )


def add_to_cart(request, product_id):
    """
    Add a product to the shopping bag.
    """

    if request.method != "POST":
        return redirect("products:shop")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    # Check stock first.
    if product.stock <= 0:
        messages.error(
            request,
            f"{product.name} is currently out of stock.",
        )

        return redirect(
            "products:product_detail",
            slug=product.slug,
        )

    # Get requested quantity.
    try:
        quantity = int(
            request.POST.get(
                "quantity",
                1,
            )
        )
    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    cart = _get_cart(request)

    product_key = str(product.id)

    try:
        current_quantity = int(
            cart.get(
                product_key,
                0,
            )
        )
    except (TypeError, ValueError):
        current_quantity = 0

    new_quantity = current_quantity + quantity

    # Do not allow more than available stock.
    if new_quantity > product.stock:
        new_quantity = product.stock

        messages.warning(
            request,
            f"Only {product.stock} of "
            f"{product.name} are available.",
        )
    else:
        messages.success(
            request,
            f"{product.name} was added to your bag.",
        )

    cart[product_key] = new_quantity

    _save_cart(
        request,
        cart,
    )

    return redirect("cart:detail")


def increase_quantity(request, product_id):
    """
    Increase a product quantity by one.
    """

    if request.method != "POST":
        return redirect("cart:detail")

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
    )

    cart = _get_cart(request)

    product_key = str(product.id)

    try:
        current_quantity = int(
            cart.get(
                product_key,
                0,
            )
        )
    except (TypeError, ValueError):
        current_quantity = 0

    # Product is no longer available.
    if product.stock <= 0:

        cart.pop(
            product_key,
            None,
        )

        _save_cart(
            request,
            cart,
        )

        messages.error(
            request,
            f"{product.name} is currently out of stock.",
        )

        return redirect("cart:detail")

    # Already at maximum stock.
    if current_quantity >= product.stock:

        messages.warning(
            request,
            f"Only {product.stock} of "
            f"{product.name} are available.",
        )

        return redirect("cart:detail")

    cart[product_key] = current_quantity + 1

    _save_cart(
        request,
        cart,
    )

    return redirect("cart:detail")


def decrease_quantity(request, product_id):
    """
    Decrease a product quantity by one.
    """

    if request.method != "POST":
        return redirect("cart:detail")

    product_key = str(product_id)

    cart = _get_cart(request)

    try:
        current_quantity = int(
            cart.get(
                product_key,
                0,
            )
        )
    except (TypeError, ValueError):
        current_quantity = 0

    if current_quantity <= 1:

        cart.pop(
            product_key,
            None,
        )

    else:

        cart[product_key] = current_quantity - 1

    _save_cart(
        request,
        cart,
    )

    return redirect("cart:detail")


def remove_from_cart(request, product_id):
    """
    Completely remove a product from the shopping bag.
    """

    if request.method != "POST":
        return redirect("cart:detail")

    cart = _get_cart(request)

    product_key = str(product_id)

    was_removed = product_key in cart

    cart.pop(
        product_key,
        None,
    )

    _save_cart(
        request,
        cart,
    )

    if was_removed:
        messages.success(
            request,
            "Product removed from your bag.",
        )

    return redirect("cart:detail")


def checkout(request):
    """
    Display the checkout page.

    At this stage the checkout form collects
    customer information. Order creation and
    payment processing can be connected later.
    """

    items, subtotal = _build_cart_items(request)

    # Do not allow checkout with an empty bag.
    if not items:

        messages.info(
            request,
            "Your shopping bag is empty.",
        )

        return redirect("cart:detail")

    cart_count = sum(
        item["quantity"]
        for item in items
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        address = request.POST.get(
            "address",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        # Basic validation.
        if not name:
            messages.error(
                request,
                "Please enter your full name.",
            )

            return redirect("cart:checkout")

        if not email:
            messages.error(
                request,
                "Please enter your email address.",
            )

            return redirect("cart:checkout")

        if not phone:
            messages.error(
                request,
                "Please enter your phone number.",
            )

            return redirect("cart:checkout")

        if not address:
            messages.error(
                request,
                "Please enter your delivery address.",
            )

            return redirect("cart:checkout")

        if not city:
            messages.error(
                request,
                "Please enter your city.",
            )

            return redirect("cart:checkout")

        if not pincode:
            messages.error(
                request,
                "Please enter your PIN code.",
            )

            return redirect("cart:checkout")

        # -------------------------------------------------
        # IMPORTANT:
        # We are NOT creating an Order yet.
        #
        # The next step is to create Order and OrderItem
        # models and connect payment processing.
        # -------------------------------------------------

        messages.success(
            request,
            "Your details were received. "
            "Order processing will be connected next.",
        )

        return redirect("cart:checkout")

    context = {
        "cart_items": items,
        "subtotal": subtotal,
        "total": subtotal,
        "cart_count": cart_count,
    }

    return render(
        request,
        "cart/checkout.html",
        context,
    )