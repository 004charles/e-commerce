from django.contrib import admin, messages
from django.db import transaction
from django.utils.text import slugify
from django.utils import timezone

from .models import Store, StoreApplication


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "province", "featured", "created_at")
    list_filter = ("status", "featured", "province")
    search_fields = ("name", "slug", "owner__username", "owner__email")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(StoreApplication)
class StoreApplicationAdmin(admin.ModelAdmin):
    list_display = ("proposed_name", "applicant", "status", "province", "created_at")
    list_filter = ("status", "province")
    search_fields = ("proposed_name", "applicant__username", "applicant__email")
    readonly_fields = ("created_at", "reviewed_at")
    actions = ("approve_applications", "reject_applications")

    @admin.action(description="Aprovar candidaturas selecionadas")
    def approve_applications(self, request, queryset):
        approved = 0
        with transaction.atomic():
            for application in queryset.select_related("applicant"):
                if application.status != StoreApplication.Status.PENDING:
                    continue
                base_slug = slugify(application.proposed_name) or f"loja-{application.pk}"
                slug = base_slug
                if Store.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{application.pk}"
                Store.objects.create(
                    owner=application.applicant,
                    name=application.proposed_name,
                    slug=slug,
                    description=application.description,
                    phone=application.phone,
                    whatsapp=application.whatsapp,
                    province=application.province,
                    municipality=application.municipality,
                    status=Store.Status.APPROVED,
                )
                application.status = StoreApplication.Status.APPROVED
                application.reviewed_by = request.user
                application.reviewed_at = timezone.now()
                application.save(update_fields=("status", "reviewed_by", "reviewed_at"))
                application.applicant.role = application.applicant.Role.STORE_OWNER
                application.applicant.save(update_fields=("role",))
                approved += 1
        self.message_user(request, f"{approved} candidatura(s) aprovada(s).", messages.SUCCESS)

    @admin.action(description="Rejeitar candidaturas selecionadas")
    def reject_applications(self, request, queryset):
        updated = queryset.filter(status=StoreApplication.Status.PENDING).update(
            status=StoreApplication.Status.REJECTED,
            reviewed_by=request.user,
            reviewed_at=timezone.now(),
        )
        self.message_user(request, f"{updated} candidatura(s) rejeitada(s).", messages.WARNING)
