from django.contrib import admin

from .models import Order, OrderItem, StoreOrder


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = [
        "product",
        "product_name",
        "sku",
        "store_name",
        "unit_price",
        "quantity",
        "line_total",
        "image",
    ]


class StoreOrderInline(admin.TabularInline):
    model = StoreOrder
    extra = 0
    readonly_fields = ["store", "subtotal", "shipping_total", "total", "created_at", "updated_at"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "order_number",
        "customer_name",
        "total",
        "currency",
        "status",
        "payment_status",
        "created_at",
    ]
    list_filter = ["status", "payment_status", "currency", "created_at"]
    search_fields = ["order_number", "customer_name", "customer_email", "customer_phone"]
    readonly_fields = ["order_number", "subtotal", "shipping_total", "total", "currency", "created_at", "updated_at"]
    inlines = [StoreOrderInline]


@admin.register(StoreOrder)
class StoreOrderAdmin(admin.ModelAdmin):
    list_display = ["order", "store", "subtotal", "total", "status", "created_at"]
    list_filter = ["status", "store"]
    search_fields = ["order__order_number", "store__name"]
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["product_name", "store_name", "unit_price", "quantity", "line_total"]
    search_fields = ["product_name", "sku", "store_name"]
    readonly_fields = [
        "store_order",
        "product",
        "product_name",
        "sku",
        "store_name",
        "unit_price",
        "quantity",
        "line_total",
        "image",
    ]
