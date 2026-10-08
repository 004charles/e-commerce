from django.db.models import Sum


def admin_metrics(request):
    if not request.path.startswith("/admin/") or not request.user.is_staff:
        return {}

    from catalog.models import Product, Promotion, Review
    from orders.models import Order
    from payments.models import PaymentAttempt
    from stores.models import Store, StoreApplication

    paid_total = (
        Order.objects.filter(payment_status=Order.PaymentStatus.PAID)
        .aggregate(total=Sum("total"))
        .get("total")
        or 0
    )
    return {
        "admin_metrics": {
            "approved_stores": Store.objects.filter(status=Store.Status.APPROVED).count(),
            "pending_applications": StoreApplication.objects.filter(
                status=StoreApplication.Status.PENDING
            ).count(),
            "active_products": Product.objects.filter(status=Product.Status.ACTIVE).count(),
            "low_stock_products": Product.objects.filter(stock__lte=5, stock__gt=0).count(),
            "pending_orders": Order.objects.filter(
                status__in=[Order.Status.PENDING, Order.Status.AWAITING_PAYMENT]
            ).count(),
            "paid_revenue": paid_total,
            "active_promotions": Promotion.objects.filter(is_active=True).count(),
            "reviews": Review.objects.count(),
            "pending_payments": PaymentAttempt.objects.filter(
                status=PaymentAttempt.Status.PENDING
            ).count(),
            "recent_orders": Order.objects.select_related("user").order_by("-created_at")[:5],
        }
    }


def global_context(request):
    """Contexto global para todos os templates do frontend."""
    if request.path.startswith("/admin/"):
        return {}

    from catalog.models import Category
    from homepage.models import SiteSettings, HomepageLink
    from cart.services import get_cart_with_items

    settings = SiteSettings.objects.filter(key="default").first()
    categories = Category.objects.filter(is_active=True).order_by("sort_order", "name")
    
    cart_items = []
    cart_count = 0
    cart_subtotal = 0
    try:
        cart = get_cart_with_items(request)
        cart_items = list(cart.items.all())
        cart_count = cart.total_quantity
        cart_subtotal = cart.subtotal
    except Exception:
        pass

    return {
        "site_settings": settings,
        "global_categories": categories,
        "cart_items": cart_items,
        "cart_count": cart_count,
        "cart_subtotal": cart_subtotal,
        "top_links": HomepageLink.objects.filter(is_active=True, placement=HomepageLink.Placement.TOP),
        "header_links": HomepageLink.objects.filter(is_active=True, placement=HomepageLink.Placement.HEADER),
        "footer_links": HomepageLink.objects.filter(is_active=True, placement=HomepageLink.Placement.FOOTER),
    }
