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
