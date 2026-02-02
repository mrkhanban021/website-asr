from django.urls import path

from website.views import (
    get_home_page
)

app_name = 'home'

urlpatterns = [
    path('', get_home_page, name='home_page'),
]