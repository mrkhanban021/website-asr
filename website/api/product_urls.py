from django.urls import path
from website.views import (
    get_Categories,
    get_product,
    get_product_detail,
    like_or_dislike_post,
)

app_name = 'product'

urlpatterns = [
    path('', get_Categories, name='cat'),
    path('product/<uuid:pk>/', get_product, name='get_product'),
    path('product/details/<uuid:pk>/', get_product_detail, name='product_detail'),
    path('product/like/<uuid:pk>/', like_or_dislike_post, name='like_product')
]