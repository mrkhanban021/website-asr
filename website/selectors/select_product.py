from website.models import (
    Categories,
    Product,
    Door,
    SparePart,
    ProductImages,
    ProductComment,
    CatalogProduct,

)
from django.db.models import QuerySet, Prefetch
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

User = get_user_model()


# نمایش دسته بندی ها
def selector_categories(*, is_active: bool) -> QuerySet:
    if is_active is None:
        is_active = True
    categories = Categories.objects.filter(is_active=is_active)
    return categories


# نمایش جزیات دسته بندی
def select_products(*, category_id: str, user=None) -> QuerySet:
    if not category_id:
        return Product.objects.none()

    category_qs = Categories.objects.filter(pk=category_id)

    if category_qs.exists():
        product = Product.objects.filter(category__in=category_qs).prefetch_related(
            Prefetch(
                'images',
                queryset=ProductImages.objects.filter(
                    is_primary=True, is_active=True),
                to_attr='primary_images'
            ),
            Prefetch(
                'details',
                queryset=Door.objects.select_related('color', 'size').prefetch_related('usage'),
                to_attr='product_details'
            ),
            Prefetch(
                'spare_parts',
                queryset=SparePart.objects.filter(is_active=True)
            ),
            Prefetch(
                'like',
                queryset=User.objects.filter(id=user.id) if user and user.is_authenticated else User.objects.none(),
                to_attr='liked_by_current_user'
            )
        )
        return product
    else:
        return Product.objects.none()


# دریافت جزیات یک محصول
def get_product_details(*, product_id: str):
    if not product_id:
        return Product.objects.none()
    return (
        Product.objects
        .filter(pk=product_id)
        .prefetch_related(
            Prefetch(
                'details',
                queryset=Door.objects
                .select_related('color', 'size')
                .prefetch_related('usage'),
                to_attr='product_details'
            ),
            Prefetch(
                'spare_parts',
                queryset=SparePart.objects.filter(is_active=True),
                to_attr='active_spare_parts'
            ),
            Prefetch(
                'images',
                queryset=ProductImages.objects.filter(is_active=True),
                to_attr='product_images'
            ),
            Prefetch(
                'catalog_files',
                queryset=CatalogProduct.objects.filter(is_active=True),
                to_attr='active_catalogs'
            ),
        )
        .first()
    )

# دریافت کامنت های یک محصول


def get_product_comments(*, product_id: str, page_number: int = 1):
    comments_qs = (
        ProductComment.objects
        .filter(
            product_id=product_id,
            is_approved=True,
            parent__isnull=True
        )
        .select_related('user')
        .prefetch_related('replies')
        .order_by('-created_time')
    )

    paginator = Paginator(comments_qs, 2)
    return paginator.get_page(page_number)
