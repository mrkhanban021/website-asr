from meta.views import Meta
from website.selectors import get_product_details


def product_detail_meta(request, *, product_data):
    product = product_data
    if not product:
        return None

    # توضیح خلاصه از اولین detail
    description = ''
    if hasattr(product, 'product_details') and product.product_details:
        description = product.product_details[0].description[:150] if product.product_details[0].description else ''

    primary_image = None

    if hasattr(product, 'product_images') and product.product_images:
        img_qs = [img for img in product.product_images if getattr(
            img, 'is_primary', False)]
        if img_qs:
            primary_image = img_qs[0].image.url

    meta = Meta(
        title=product.title,
        description=description,
        url=request.build_absolute_uri(),
        image=primary_image,
        object_type='website',
        use_og=True,
        use_twitter=True,
    )
    return meta
