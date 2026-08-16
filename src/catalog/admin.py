from django.contrib import admin

from .models import Category, Product, Promotion, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "store",
        "category",
        "price",
        "stock",
        "status",
        "featured",
    )
    list_filter = ("status", "featured", "is_new", "category", "store")
    search_fields = ("name", "sku", "slug", "store__name")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("status", "featured")


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("name", "discount_percent", "product", "category", "starts_at", "ends_at", "is_active")
    list_filter = ("is_active", "starts_at", "ends_at", "category")
    search_fields = ("name", "product__name", "category__name")
    autocomplete_fields = ("product", "category")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username", "user__email", "comment")
    readonly_fields = ("created_at", "updated_at")
