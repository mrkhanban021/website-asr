from website.models import (
    Product
)


#اضافه کردن لایک به محصول
def like_product(*, product_id: str, user) -> bool:
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return False
    if product.like.filter(pk=user.id).exists():
        product.like.remove(user)
        return False
    product.like.add(user)
    return True