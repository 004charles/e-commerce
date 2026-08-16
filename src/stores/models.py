from django.conf import settings
from django.db import models
from django.urls import reverse


class Store(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        APPROVED = "approved", "Aprovada"
        SUSPENDED = "suspended", "Suspensa"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="stores",
        verbose_name="proprietário",
    )
    name = models.CharField("nome", max_length=160)
    slug = models.SlugField("slug", unique=True)
    description = models.TextField("descrição", blank=True)
    logo = models.ImageField("logótipo", upload_to="stores/logos/", blank=True)
    phone = models.CharField("telefone", max_length=30, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=30, blank=True)
    province = models.CharField("província", max_length=80, blank=True)
    municipality = models.CharField("município", max_length=100, blank=True)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    featured = models.BooleanField("em destaque", default=False)
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        ordering = ["-featured", "name"]
        verbose_name = "loja"
        verbose_name_plural = "lojas"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("stores:detail", kwargs={"slug": self.slug})


class StoreApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pendente"
        APPROVED = "approved", "Aprovada"
        REJECTED = "rejected", "Rejeitada"

    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="store_applications",
        verbose_name="candidato",
    )
    proposed_name = models.CharField("nome proposto", max_length=160)
    description = models.TextField("descrição", blank=True)
    phone = models.CharField("telefone", max_length=30)
    whatsapp = models.CharField("WhatsApp", max_length=30, blank=True)
    province = models.CharField("província", max_length=80)
    municipality = models.CharField("município", max_length=100)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    review_note = models.TextField("nota de análise", blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_store_applications",
        verbose_name="analisada por",
    )
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    reviewed_at = models.DateTimeField("analisada em", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "candidatura de loja"
        verbose_name_plural = "candidaturas de lojas"

    def __str__(self):
        return f"{self.proposed_name} — {self.get_status_display()}"
