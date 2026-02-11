from website.models import (
    Categories,
    Product,
    ProductImages
)
from django.db.models import QuerySet, Prefetch



def selector_categories(*, is_active: bool = None) -> QuerySet:
    if is_active is None:
        is_active = True
    categories = Categories.objects.filter(is_active=is_active)
    return categories





def select_product(*, category_id: str = None) -> QuerySet:
    if not category_id:
        return Product.objects.none()

    category_qs = Categories.objects.filter(pk=category_id)

    if category_qs.exists():
        product = Product.objects.filter(category__in=category_qs).prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImages.objects.filter(is_primary=True),
                to_attr='primary_images'
            )
        )
        return product
    else:
        return Product.objects.none()