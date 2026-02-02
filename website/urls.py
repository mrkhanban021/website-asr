from django.urls import path, include

app_name = 'website'

urlpatterns = [
    path('', include('website.api.home_url', namespace='website'))
]