import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from homepage.models import HomepageBanner, HomepageLink, HomepageTextBlock, SiteSettings


class Command(BaseCommand):
    help = "Cria ou atualiza o conteúdo configurável inicial da homepage."

    def handle(self, *args, **options):
        SiteSettings.objects.update_or_create(
            key="default",
            defaults={
                "site_name": "Marketplace Angola",
                "tagline": "Produtos de várias lojas num único espaço.",
                "shipping_message": "Entrega em Angola. Preços e stock atualizados.",
                "support_phone": "+244 923 000 000",
                "support_email": "suporte@marketplace.ao",
                "contact_address": "Luanda, Angola",
                "newsletter_title": "Receba as novidades do marketplace",
                "newsletter_description": "Conheça novas lojas, promoções e produtos em destaque.",
                "currency_code": "AOA",
                "currency_symbol": "Kz",
            },
        )
        source_dir = Path(settings.BASE_DIR) / "assets" / "images" / "banner"
        media_dir = Path(settings.MEDIA_ROOT) / "homepage" / "banners"
        media_dir.mkdir(parents=True, exist_ok=True)
        for number in range(1, 17):
            source = source_dir / f"{number}.{'png' if number >= 13 else 'jpg'}"
            if source.exists():
                shutil.copy2(source, media_dir / source.name)
                HomepageBanner.objects.update_or_create(
                    placement=HomepageBanner.Placement.PROMOTION,
                    sort_order=number,
                    defaults={
                        "title": f"Destaque Marketplace Angola {number}",
                        "subtitle": "Produtos e ofertas de lojas aprovadas.",
                        "button_label": "Ver produtos",
                        "button_url": "/catalog/",
                        "image": f"homepage/banners/{source.name}",
                        "is_active": True,
                    },
                )

        text_blocks = {
            "shipping-message": {
                "title": "Entrega em Angola",
                "subtitle": "Compras simples e seguras",
                "body": "Encontre produtos de lojas aprovadas e acompanhe os seus pedidos.",
            },
            "newsletter": {
                "title": "Receba as novidades do marketplace",
                "subtitle": "Promoções e produtos em destaque",
                "body": "Subscreva para receber as principais novidades.",
            },
            "flash-sale": {
                "title": "Ofertas relâmpago",
                "subtitle": "Produtos selecionados com preços especiais.",
                "body": "Stock limitado e oportunidades atualizadas diariamente.",
            },
            "categories": {
                "title": "Compre por categorias",
                "subtitle": "Encontre rapidamente o que procura.",
                "body": "Explore produtos de lojas aprovadas em Angola.",
            },
            "recommendations": {
                "title": "Recomendações",
                "subtitle": "Produtos em destaque no marketplace.",
                "body": "Compare lojas, preços e disponibilidade antes de comprar.",
            },
            "trending": {
                "title": "Tendências",
                "subtitle": "Escolhas populares entre os clientes.",
                "body": "",
            },
            "hot-deals": {
                "title": "Oferta do dia",
                "subtitle": "Uma seleção especial das nossas lojas.",
                "body": "",
            },
            "hot-tags": {
                "title": "Categorias populares",
                "subtitle": "Pesquise por temas e encontre novos produtos.",
                "body": "",
            },
            "offers": {
                "title": "Não perca estas ofertas",
                "subtitle": "Promoções de lojas aprovadas em Angola.",
                "body": "",
            },
        }
        for key, values in text_blocks.items():
            HomepageTextBlock.objects.update_or_create(
                key=key,
                defaults={"is_active": True, **values},
            )

        links = [
            (HomepageLink.Placement.TOP, "Início", "/", 10),
            (HomepageLink.Placement.TOP, "Catálogo", "/catalog/", 20),
            (HomepageLink.Placement.TOP, "Contactos", "/#contactos", 30),
            (HomepageLink.Placement.HEADER, "Produtos", "/catalog/", 10),
            (HomepageLink.Placement.HEADER, "Lojas", "/stores/", 20),
            (HomepageLink.Placement.HEADER, "Promoções", "/catalog/?promotions=1", 30),
            (HomepageLink.Placement.HEADER, "Categorias", "/catalog/", 40),
            (HomepageLink.Placement.HEADER, "Vendedor", "/stores/apply/", 50),
            (HomepageLink.Placement.HEADER, "Minha conta", "/account/profile/", 60),
            (HomepageLink.Placement.HEADER, "Ajuda", "/#contactos", 70),
            (HomepageLink.Placement.FOOTER, "Início", "/", 10),
            (HomepageLink.Placement.FOOTER, "Catálogo", "/catalog/", 20),
            (HomepageLink.Placement.FOOTER, "Minha conta", "/account/profile/", 30),
            (HomepageLink.Placement.FOOTER, "Pedidos", "/account/orders/", 40),
        ]
        for placement, label, url, sort_order in links:
            HomepageLink.objects.update_or_create(
                placement=placement,
                label=label,
                defaults={"url": url, "sort_order": sort_order, "is_active": True},
            )
        self.stdout.write(self.style.SUCCESS("Conteúdo inicial da homepage criado/atualizado."))
