from django.shortcuts import (
    render,
    redirect
)
from django.contrib import messages

from website.selectors import (
    selector_categories,
    select_products,
    get_product_details,
    get_data_site_settings,
    get_product_comments
)

from website.services import (
    like_product
)

#بر گرداندن دسته بندی ها
def get_Categories(request):
    data = selector_categories(is_active=True)

    context = {
        'categories': data
    }
    return render(request, 'website/product/categories.html', context)


#برگرداندن محصولات دسته بندی
def get_product(request, pk):
    
    data = select_products(category_id=pk, user=request.user)
    if not data:
        messages.warning(request, 'داده ای یافت نشد')
        return redirect('website:product:cat')

    context = {
        'products': data
    }

    return render(request, 'website/product/product_page.html', context)



# بر گرداندن جزیات یک محصول
def get_product_detail(request, pk):
    page_number = request.GET.get('page', 1)
    product_det = get_product_details(product_id=pk)
    product_comment = get_product_comments(product_id=pk, page_number=page_number)

    if not product_det:
        messages.warning(request, 'جزیات محصول یافت نشد')
        return redirect('website:product:cat')
    
    context = {
        'product_det': product_det,
        'comments': product_comment
    }

    return render(request, 'website/product/product_details.html', context)


def like_or_dislike_post(request, pk):
    url = request.META.get('HTTP_REFERER')
    like = like_product(product_id=pk, user=request.user)
    if like:
        messages.success(request, 'شما این محصول را پسندیدید')
        return redirect(url)
    messages.success(request, 'لایک شما برداشته شد')
    return redirect(url)