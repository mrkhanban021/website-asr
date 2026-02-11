from django.urls import path
from website.views import (
    get_Categories,
    get_product
)

app_name = 'product'

urlpatterns = [
    path('', get_Categories, name='cat'),
    path('product/<uuid:pk>/', get_product, name='get_product')
]