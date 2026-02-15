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
    get_product_comments,
    get_comment
)

from website.services import (
    like_product
)

from website.forms import (
    ProductCommentForms,
    ProductCommentReplyForm
)

# بر گرداندن دسته بندی ها


def get_Categories(request):
    data = selector_categories(is_active=True)

    context = {
        'categories': data
    }
    return render(request, 'website/product/categories.html', context)


# برگرداندن محصولات دسته بندی
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
    if request.method == 'POST':
        parent_id = request.POST.get("parent_id")
        parent_comment = None
        if parent_id:
            parent_comment = get_comment(product_comment_id=parent_id)

        form = ProductCommentReplyForm(request.POST, user=request.user, product=product_det, parent=parent_comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'بعد از تایید ادمین نمایش داده میشود')
            return redirect('website:product:product_detail', pk=pk)
    else:
        form = ProductCommentForms()
        if not product_det:
            messages.warning(request, 'جزیات محصول یافت نشد')
            return redirect('website:product:cat')
    
    context = {
        'product_det': product_det, # type: ignore
        'comments': product_comment, # type: ignore
        'form': form
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