from pathlib import Path
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from accounts.models import User
from catalog.models import Category, Product
from stores.models import Store


class Command(BaseCommand):
    help = "Cria 10 lojas aprovadas e 100 produtos de demonstração para o Marketplace Angola."

    def handle(self, *args, **options):
        demo_password = "DemoAngola2026!"
        stores_data = [
            ("demo-cidade-china", "Cidade da China Eletrónica", "Tecnologia e acessórios para o dia a dia.", "Luanda", "Viana", True),
            ("demo-novo-sao-paulo", "Novo São Paulo Fashion", "Moda, calçado e acessórios com tendências atuais.", "Luanda", "Cazenga", True),
            ("demo-nova-era", "Nova Era Casa & Acessórios", "Produtos práticos para casa, cozinha e organização.", "Luanda", "Kilamba Kiaxi", True),
            ("demo-mercado-kilamba", "Mercado do Kilamba", "Produtos essenciais para famílias e pequenos negócios.", "Luanda", "Kilamba Kiaxi", False),
            ("demo-luanda-mobile", "Luanda Mobile Center", "Telemóveis, informática e acessórios tecnológicos.", "Luanda", "Ingombota", True),
            ("demo-viana-tech", "Viana Tech & Casa", "Eletrónica, utilidades e soluções para o lar.", "Luanda", "Viana", False),
            ("demo-maianga-beleza", "Maianga Beleza & Moda", "Cuidados pessoais, beleza e moda feminina.", "Luanda", "Maianga", False),
            ("demo-cazenga-desporto", "Cazenga Desporto", "Equipamentos para treino, lazer e vida ativa.", "Luanda", "Cazenga", False),
            ("demo-talatona-home", "Talatona Home Premium", "Casa, decoração e acessórios premium.", "Luanda", "Talatona", True),
            ("demo-benguela-ofertas", "Benguela Ofertas Online", "Seleção de produtos para todo o país.", "Benguela", "Benguela", False),
        ]
        stores = {}
        for index, (username, name, description, province, municipality, featured) in enumerate(stores_data, start=1):
            email = f"{username}@marketplace.test"
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "role": User.Role.STORE_OWNER,
                    "first_name": name.split()[0],
                    "last_name": "Demo",
                },
            )
            if created:
                user.set_password(demo_password)
            user.email = email
            user.role = User.Role.STORE_OWNER
            user.first_name = name.split()[0]
            user.last_name = "Demo"
            user.save(update_fields=["email", "role", "first_name", "last_name", "password"] if created else ["email", "role", "first_name", "last_name"])
            store, _ = Store.objects.update_or_create(
                slug=slugify(name),
                defaults={
                    "owner": user,
                    "name": name,
                    "description": description,
                    "phone": f"+244 923 000 {index:03d}",
                    "whatsapp": f"+244 923 000 {index:03d}",
                    "province": province,
                    "municipality": municipality,
                    "status": Store.Status.APPROVED,
                    "featured": featured,
                },
            )
            stores[store.slug] = store

        categories_data = [
            ("Eletrónica", "electronica"),
            ("Moda e Vestuário", "moda-vestuario"),
            ("Casa e Cozinha", "casa-cozinha"),
            ("Acessórios", "acessorios"),
            ("Telemóveis", "telemoveis"),
            ("Informática", "informatica"),
            ("Beleza e Cuidados", "beleza-cuidados"),
            ("Desporto e Fitness", "desporto-fitness"),
            ("Decoração", "decoracao"),
            ("Utilidades do Lar", "utilidades-lar"),
        ]
        categories = {}
        category_images = self._available_assets(settings.BASE_DIR / "assets" / "images" / "category")
        for index, (name, slug) in enumerate(categories_data):
            category, _ = Category.objects.update_or_create(
                slug=slug,
                defaults={"name": name, "is_active": True, "sort_order": index},
            )
            if category_images:
                source = category_images[index % len(category_images)]
                target_name = f"catalog/categories/{slug}{source.suffix.lower()}"
                self._copy_asset(source, settings.MEDIA_ROOT / target_name)
                category.image = target_name
                category.save(update_fields=["image"])
            categories[slug] = category

        # O seed controla exclusivamente os dados das lojas demo, evitando duplicados e garantindo 100 produtos.
        Product.objects.filter(store__in=stores.values()).delete()
        product_templates = [
            ("Smartphone Android Pro 128GB", "telemoveis", "185000.00"),
            ("Auscultadores Bluetooth Premium", "electronica", "28500.00"),
            ("Relógio Inteligente Series X3", "electronica", "42000.00"),
            ("T-shirt Premium Algodão", "moda-vestuario", "12500.00"),
            ("Ténis Urban Street", "moda-vestuario", "45000.00"),
            ("Mala Feminina Clássica", "moda-vestuario", "27500.00"),
            ("Organizador Multiusos para Casa", "utilidades-lar", "8500.00"),
            ("Conjunto de Utensílios de Cozinha", "casa-cozinha", "18500.00"),
            ("Candeeiro LED Decorativo", "decoracao", "14500.00"),
            ("Mochila Casual Resistente", "acessorios", "22000.00"),
        ]
        product_images = self._available_assets(settings.BASE_DIR / "assets" / "images" / "product")
        product_count = 0
        image_count = 0
        for store_index, store in enumerate(stores.values(), start=1):
            for product_index, (name, category_slug, base_price) in enumerate(product_templates, start=1):
                price = self._adjust_price(base_price, store_index, product_index)
                slug = slugify(f"{name}-{store.slug}")
                sku = f"{store_index:02d}-{product_index:02d}-{slugify(name)[:18].upper()}"
                product = Product.objects.create(
                    store=store,
                    category=categories[category_slug],
                    name=name,
                    slug=slug,
                    sku=sku,
                    short_description=f"{name} disponível na {store.name}.",
                    description=f"Produto de demonstração do Marketplace Angola, vendido pela loja {store.name}, em {store.municipality}, {store.province}.",
                    price=price,
                    compare_at_price=self._compare_price(price),
                    stock=5 + ((store_index * 7 + product_index * 3) % 46),
                    status=Product.Status.ACTIVE,
                    featured=product_index <= 2 or store_index in (1, 5, 9),
                    is_new=product_index >= 7,
                    rating="4.50",
                    review_count=8,
                )
                if product_images:
                    source = product_images[(product_count) % len(product_images)]
                    target_name = f"catalog/products/demo/{store.slug}-{product_index}{source.suffix.lower()}"
                    self._copy_asset(source, settings.MEDIA_ROOT / target_name)
                    product.image = target_name
                    product.save(update_fields=["image"])
                    image_count += 1
                product_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Dados prontos: {len(stores)} lojas, {len(categories)} categorias, {product_count} produtos e {image_count} imagens copiadas."
        ))
        self.stdout.write(f"Palavra-passe dos vendedores demo: {demo_password}")

    @staticmethod
    def _available_assets(directory):
        return sorted(
            [path for path in Path(directory).glob("*") if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}],
            key=lambda path: (0, int(path.stem)) if path.stem.isdigit() else (1, path.stem),
        )

    @staticmethod
    def _copy_asset(source, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copy2(source, target)

    @staticmethod
    def _adjust_price(base_price, store_index, product_index):
        from decimal import Decimal
        return (Decimal(base_price) + Decimal(store_index * 1250) + Decimal(product_index * 275)).quantize(Decimal("0.01"))

    @staticmethod
    def _compare_price(price):
        from decimal import Decimal
        return (price * Decimal("1.18")).quantize(Decimal("0.01"))
