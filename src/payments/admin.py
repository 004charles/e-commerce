from django.contrib import admin

from .models import PaymentAttempt


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = ("order", "method", "status", "provider_reference", "created_at")
    list_filter = ("method", "status", "created_at")
    search_fields = ("order__order_number", "provider_reference", "message")
    readonly_fields = ("created_at", "updated_at")
