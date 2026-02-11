from django.shortcuts import (
    render,
    redirect
)
from django.contrib import messages

from website.selectors import (
    selector_categories,
    select_product
)

def get_Categories(request):
    data = selector_categories()

    context = {
        'categories': data
    }
    return render(request, 'website/product/categories.html', context)


def get_product(request, pk):
    
    data = select_product(category_id=pk)
    if not data:
        messages.warning(request, 'داده ای یافت نشد')
        return redirect('website:product:cat')

    context = {
        'products': data
    }

    return render(request, 'website/product/product_page.html', context)