from django.contrib import admin

from .models import HomepageBanner, HomepageLink, HomepageTextBlock, SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "currency_code", "support_phone", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(HomepageBanner)
class HomepageBannerAdmin(admin.ModelAdmin):
    list_display = ("title", "placement", "sort_order", "is_active", "starts_at", "ends_at")
    list_filter = ("placement", "is_active")
    search_fields = ("title", "subtitle", "description")
    list_editable = ("sort_order", "is_active")


@admin.register(HomepageTextBlock)
class HomepageTextBlockAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("key", "title", "body")
    prepopulated_fields = {"key": ("title",)}


@admin.register(HomepageLink)
class HomepageLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "placement", "sort_order", "is_active")
    list_filter = ("placement", "is_active")
    search_fields = ("label", "url")
    list_editable = ("sort_order", "is_active")
