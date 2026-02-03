from django.urls import path
from identify.views import (
    register_form
)

app_name = 'endpoint'

urlpatterns = [
    path('register/', register_form, name='register_form'),
    
]