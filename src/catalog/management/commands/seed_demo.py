from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts.models import User
from catalog.models import Category, Product
from stores.models import Store


class Command(BaseCommand):
    help = "Cria lojas, categorias e produtos de demonstração para o Marketplace Angola."

    def handle(self, *args, **options):
        demo_password = "DemoAngola2026!"
        stores_data = [
            {
                "username": "demo-cidade-china",
                "email": "cidade.china.demo@marketplace.test",
                "name": "Cidade da China Eletrónica",
                "slug": "cidade-da-china-eletronica",
                "description": "Tecnologia e acessórios para o dia a dia em Luanda.",
                "province": "Luanda",
                "municipality": "Viana",
                "featured": True,
            },
            {
                "username": "demo-novo-sao-paulo",
                "email": "novo.sao.paulo.demo@marketplace.test",
                "name": "Novo São Paulo Fashion",
                "slug": "novo-sao-paulo-fashion",
                "description": "Moda, calçado e acessórios com tendências atuais.",
                "province": "Luanda",
                "municipality": "Cazenga",
                "featured": True,
            },
            {
                "username": "demo-nova-era",
                "email": "nova.era.demo@marketplace.test",
                "name": "Nova Era Casa & Acessórios",
                "slug": "nova-era-casa-acessorios",
                "description": "Produtos práticos para casa, cozinha e organização.",
                "province": "Luanda",
                "municipality": "Kilamba Kiaxi",
                "featured": False,
            },
        ]
        stores = {}
        for data in stores_data:
            user, created = User.objects.get_or_create(
                username=data["username"],
                defaults={
                    "email": data["email"],
                    "role": User.Role.STORE_OWNER,
                    "first_name": data["name"].split()[0],
                },
            )
            if created:
                user.set_password(demo_password)
            user.email = data["email"]
            user.role = User.Role.STORE_OWNER
            user.save(update_fields=["email", "role", "password"] if created else ["email", "role"])
            store, _ = Store.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "owner": user,
                    "name": data["name"],
                    "description": data["description"],
                    "province": data["province"],
                    "municipality": data["municipality"],
                    "status": Store.Status.APPROVED,
                    "featured": data["featured"],
                },
            )
            stores[data["slug"]] = store

        categories_data = [
            ("Eletrónica", "electronica", "category/1.png"),
            ("Moda e Vestuário", "moda-vestuario", "category/10.png"),
            ("Casa e Cozinha", "casa-cozinha", "category/20.png"),
            ("Acessórios", "acessorios", "category/30.png"),
        ]
        categories = {}
        for name, slug, image_source in categories_data:
            category, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "is_active": True},
            )
            self._copy_asset(image_source, category.image, f"catalog/categories/{slug}.png")
            if not category.image:
                category.image = f"catalog/categories/{slug}.png"
                category.save(update_fields=["image"])
            categories[slug] = category

        products_data = [
            ("cidade-da-china-eletronica", "electronica", "Smartphone Android Pro 128GB", "smartphone-android-pro-128gb", "CC-ELE-001", "185000.00", "210000.00", 18, 1, True),
            ("cidade-da-china-eletronica", "electronica", "Auscultadores Bluetooth Premium", "auscultadores-bluetooth-premium", "CC-ELE-002", "28500.00", "35000.00", 32, 2, True),
            ("cidade-da-china-eletronica", "electronica", "Relógio Inteligente Series X3", "relogio-inteligente-series-x3", "CC-ELE-003", "42000.00", "50000.00", 14, 3, False),
            ("cidade-da-china-eletronica", "electronica", "Coluna Portátil Bluetooth", "coluna-portatil-bluetooth", "CC-ELE-004", "19800.00", "24000.00", 25, 4, False),
            ("novo-sao-paulo-fashion", "moda-vestuario", "T-shirt Premium Algodão", "t-shirt-premium-algodao", "NSP-MOD-001", "12500.00", "16000.00", 40, 5, True),
            ("novo-sao-paulo-fashion", "moda-vestuario", "Vestido Casual Elegante", "vestido-casual-elegante", "NSP-MOD-002", "32000.00", "40000.00", 12, 6, True),
            ("novo-sao-paulo-fashion", "moda-vestuario", "Ténis Urban Street", "tenis-urban-street", "NSP-MOD-003", "45000.00", "55000.00", 20, 7, False),
            ("cidade-da-china-eletronica", "moda-vestuario", "Ténis Urban Street", "tenis-urban-street-cidade-china", "CC-MOD-001", "42000.00", "50000.00", 10, 7, False),
            ("novo-sao-paulo-fashion", "moda-vestuario", "Mala Feminina Clássica", "mala-feminina-classica", "NSP-MOD-004", "27500.00", "33000.00", 16, 8, False),
            ("nova-era-casa-acessorios", "casa-cozinha", "Organizador Multiusos para Casa", "organizador-multiusos-casa", "NE-CAS-001", "8500.00", "11000.00", 35, 9, True),
            ("nova-era-casa-acessorios", "casa-cozinha", "Conjunto de Utensílios de Cozinha", "conjunto-utensilios-cozinha", "NE-CAS-002", "18500.00", "23000.00", 22, 10, False),
            ("nova-era-casa-acessorios", "acessorios", "Candeeiro LED Decorativo", "candeeiro-led-decorativo", "NE-ACE-001", "14500.00", "18000.00", 19, 11, True),
            ("nova-era-casa-acessorios", "acessorios", "Mochila Casual Resistente", "mochila-casual-resistente", "NE-ACE-002", "22000.00", "28000.00", 27, 12, False),
        ]
        image_count = 0
        for store_slug, category_slug, name, product_slug, sku, price, compare_at_price, stock, image_number, featured in products_data:
            store = stores[store_slug]
            category = categories[category_slug]
            product, _ = Product.objects.update_or_create(
                store=store,
                sku=sku,
                defaults={
                    "category": category,
                    "name": name,
                    "slug": product_slug,
                    "short_description": f"{name} disponível em {store.name}.",
                    "description": f"Produto de demonstração do Marketplace Angola, vendido pela loja {store.name}.",
                    "price": price,
                    "compare_at_price": compare_at_price,
                    "stock": stock,
                    "status": Product.Status.ACTIVE,
                    "featured": featured,
                    "is_new": True,
                    "rating": "4.50",
                    "review_count": 8,
                },
            )
            target_name = f"catalog/products/demo/{image_number}.png"
            source = settings.BASE_DIR / "assets" / "images" / "product" / f"{image_number}.png"
            target = settings.MEDIA_ROOT / target_name
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.exists():
                shutil.copy2(source, target)
                image_count += 1
            if product.image.name != target_name:
                product.image = target_name
                product.save(update_fields=["image"])

        self.stdout.write(self.style.SUCCESS(
            f"Dados de demonstração prontos: {len(stores)} lojas, {len(categories)} categorias, {len(products_data)} produtos e {image_count} imagens copiadas."
        ))
        self.stdout.write(f"Palavra-passe dos utilizadores demo: {demo_password}")

    @staticmethod
    def _copy_asset(source_name, current_image, target_name):
        source = settings.BASE_DIR / "assets" / "images" / source_name
        target = settings.MEDIA_ROOT / target_name
        if source.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
