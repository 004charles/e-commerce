from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.urls import reverse

from stores.models import Store


class Category(models.Model):
    name = models.CharField("nome", max_length=120)
    slug = models.SlugField("slug", unique=True)
    image = models.ImageField("imagem", upload_to="catalog/categories/", blank=True)
    is_active = models.BooleanField("ativa", default=True)
    sort_order = models.PositiveIntegerField("ordem", default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog", kwargs={"category_slug": self.slug})


class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        ACTIVE = "active", "Ativo"
        OUT_OF_STOCK = "out_of_stock", "Sem stock"
        SUSPENDED = "suspended", "Suspenso"

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="loja",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="categoria",
    )
    name = models.CharField("nome", max_length=180)
    slug = models.SlugField("slug")
    sku = models.CharField("SKU", max_length=80)
    short_description = models.CharField("descrição curta", max_length=240, blank=True)
    description = models.TextField("descrição", blank=True)
    image = models.ImageField("imagem", upload_to="catalog/products/", blank=True)
    price = models.DecimalField("preço", max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(
        "preço anterior", max_digits=12, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField("stock", default=0)
    status = models.CharField(
        "estado",
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    featured = models.BooleanField("em destaque", default=False)
    is_new = models.BooleanField("novidade", default=True)
    rating = models.DecimalField("avaliação", max_digits=3, decimal_places=2, default=0)
    review_count = models.PositiveIntegerField("número de avaliações", default=0)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["store", "sku"], name="unique_product_sku_per_store"
            ),
            models.UniqueConstraint(
                fields=["store", "slug"], name="unique_product_slug_per_store"
            ),
        ]
        ordering = ["-featured", "-created_at"]
        verbose_name = "produto"
        verbose_name_plural = "produtos"

    def __str__(self):
        return self.name

    @property
    def is_available(self):
        return self.status == self.Status.ACTIVE and self.stock > 0

    def get_absolute_url(self):
        return reverse(
            "catalog:detail", kwargs={"store_slug": self.store.slug, "slug": self.slug}
        )


class Promotion(models.Model):
    name = models.CharField("nome", max_length=160)
    discount_percent = models.DecimalField(
        "desconto percentual", max_digits=5, decimal_places=2
    )
    starts_at = models.DateTimeField("início")
    ends_at = models.DateTimeField("fim")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="promotions",
        null=True,
        blank=True,
        verbose_name="produto",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="promotions",
        null=True,
        blank=True,
        verbose_name="categoria",
    )
    is_active = models.BooleanField("ativa", default=True)
    created_at = models.DateTimeField("criada em", auto_now_add=True)

    class Meta:
        ordering = ["-discount_percent", "-starts_at"]
        verbose_name = "promoção"
        verbose_name_plural = "promoções"

    def clean(self):
        if not self.product and not self.category:
            raise ValidationError("Indique um produto ou uma categoria para a promoção.")
        if self.product and self.category:
            raise ValidationError("Uma promoção deve aplicar-se a um produto ou a uma categoria, não aos dois.")
        if self.discount_percent <= 0 or self.discount_percent > 100:
            raise ValidationError("O desconto deve estar entre 0,01% e 100%.")
        if self.ends_at <= self.starts_at:
            raise ValidationError("A data final deve ser posterior à data inicial.")

    @property
    def is_current(self):
        now = timezone.now()
        return self.is_active and self.starts_at <= now < self.ends_at


class Review(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="produto",
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="product_reviews",
        verbose_name="cliente",
    )
    rating = models.PositiveSmallIntegerField("classificação")
    comment = models.TextField("comentário", max_length=2000)
    created_at = models.DateTimeField("criada em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizada em", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["product", "user"], name="unique_review_per_product_user"
            )
        ]
        verbose_name = "avaliação"
        verbose_name_plural = "avaliações"

    def __str__(self):
        return f"{self.product.name} — {self.user} ({self.rating}/5)"
