from django.core.exceptions import ValidationError
from django.db import models


class SiteSettings(models.Model):
    key = models.CharField("chave", max_length=40, unique=True, default="default")
    site_name = models.CharField("nome do site", max_length=160, default="Marketplace Angola")
    tagline = models.CharField("frase principal", max_length=240, blank=True)
    shipping_message = models.CharField("mensagem de envio", max_length=240, blank=True)
    support_phone = models.CharField("telefone de suporte", max_length=80, blank=True)
    support_email = models.EmailField("email de suporte", blank=True)
    contact_address = models.CharField("morada", max_length=240, blank=True)
    facebook_url = models.URLField("Facebook", blank=True)
    instagram_url = models.URLField("Instagram", blank=True)
    twitter_url = models.URLField("Twitter", blank=True)
    whatsapp_url = models.URLField("WhatsApp", blank=True)
    newsletter_title = models.CharField("título da newsletter", max_length=160, blank=True)
    newsletter_description = models.CharField("descrição da newsletter", max_length=240, blank=True)
    currency_code = models.CharField("código da moeda", max_length=8, default="AOA")
    currency_symbol = models.CharField("símbolo da moeda", max_length=8, default="Kz")
    updated_at = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "configuração do site"
        verbose_name_plural = "configuração do site"

    def clean(self):
        if self.key != "default":
            raise ValidationError("A configuração principal deve usar a chave default.")

    def __str__(self):
        return self.site_name


class HomepageBanner(models.Model):
    class Placement(models.TextChoices):
        HERO = "hero", "Hero principal"
        PROMOTION = "promotion", "Promoção"
        SERVICE = "service", "Serviço"

    placement = models.CharField("posição", max_length=24, choices=Placement.choices)
    title = models.CharField("título", max_length=180)
    subtitle = models.CharField("subtítulo", max_length=240, blank=True)
    description = models.TextField("descrição", blank=True)
    button_label = models.CharField("texto do botão", max_length=80, blank=True)
    button_url = models.CharField("URL do botão", max_length=300, blank=True)
    image = models.ImageField("imagem", upload_to="homepage/banners/", blank=True)
    sort_order = models.PositiveIntegerField("ordem", default=0)
    is_active = models.BooleanField("ativo", default=True)
    starts_at = models.DateTimeField("início", null=True, blank=True)
    ends_at = models.DateTimeField("fim", null=True, blank=True)

    class Meta:
        ordering = ["placement", "sort_order", "id"]
        verbose_name = "banner da homepage"
        verbose_name_plural = "banners da homepage"

    def __str__(self):
        return f"{self.get_placement_display()} — {self.title}"


class HomepageTextBlock(models.Model):
    key = models.SlugField("chave", unique=True)
    title = models.CharField("título", max_length=180)
    subtitle = models.CharField("subtítulo", max_length=240, blank=True)
    body = models.TextField("conteúdo", blank=True)
    button_label = models.CharField("texto do botão", max_length=80, blank=True)
    button_url = models.CharField("URL do botão", max_length=300, blank=True)
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        ordering = ["key"]
        verbose_name = "bloco de texto da homepage"
        verbose_name_plural = "blocos de texto da homepage"

    def __str__(self):
        return self.title


class HomepageLink(models.Model):
    class Placement(models.TextChoices):
        TOP = "top", "Barra superior"
        HEADER = "header", "Cabeçalho"
        CATEGORY = "category", "Categorias"
        FOOTER = "footer", "Rodapé"

    placement = models.CharField("posição", max_length=24, choices=Placement.choices)
    label = models.CharField("texto", max_length=100)
    url = models.CharField("URL", max_length=300)
    icon = models.CharField("ícone", max_length=80, blank=True)
    sort_order = models.PositiveIntegerField("ordem", default=0)
    is_active = models.BooleanField("ativo", default=True)

    class Meta:
        ordering = ["placement", "sort_order", "id"]
        verbose_name = "link da homepage"
        verbose_name_plural = "links da homepage"

    def __str__(self):
        return f"{self.get_placement_display()} — {self.label}"
