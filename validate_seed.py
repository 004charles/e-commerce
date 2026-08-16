from catalog.models import Category, Product
from stores.models import Store

stores = Store.objects.filter(slug__in=[
    "cidade-da-china-eletronica",
    "novo-sao-paulo-fashion",
    "nova-era-casa-acessorios",
    "mercado-do-kilamba",
    "luanda-mobile-center",
    "viana-tech-casa",
    "maianga-beleza-moda",
    "cazenga-desporto",
    "talatona-home-premium",
    "benguela-ofertas-online",
])
print({
    "stores": stores.count(),
    "approved_stores": stores.filter(status=Store.Status.APPROVED).count(),
    "categories": Category.objects.filter(is_active=True).count(),
    "products": Product.objects.filter(store__in=stores).count(),
    "active_products": Product.objects.filter(store__in=stores, status=Product.Status.ACTIVE).count(),
    "products_with_images": Product.objects.filter(store__in=stores).exclude(image="").count(),
    "total_stock": sum(Product.objects.filter(store__in=stores).values_list("stock", flat=True)),
})
print({store.name: store.products.count() for store in stores})
