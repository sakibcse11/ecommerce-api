from celery import shared_task
from django.core.cache import cache
from django.conf import settings

from .models import Product
from .serializers import ProductDetailSerializer


@shared_task
def update_product_cache():

    products = Product.objects.filter(active=True).select_related('vendor')[:100]

    serializer = ProductDetailSerializer(products, many=True)

    cache.set('popular_products', serializer.data, timeout=settings.PRODUCT_CACHE_TTL)

    return f"Updated cache for {len(products)} popular products"


@shared_task
def invalidate_product_cache(product_id):
    cache_key = f'product_{product_id}'
    cache.delete(cache_key)

    cache.delete('popular_products')

    return f"Invalidated cache for product {product_id}"