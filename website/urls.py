from django.urls import path, include

app_name = 'website'

urlpatterns = [
    path('', include('website.api.home_url', namespace='website')),
    path('categories/', include('website.api.product_urls', namespace='product'))
]