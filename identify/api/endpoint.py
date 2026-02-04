from django.urls import path
from identify.views import (
    register_form,
    login_form,
    logout_func,
    get_profile
)

app_name = 'endpoint'

urlpatterns = [
    path('register/', register_form, name='register_form'),
    path('login/', login_form, name='login_form'),
    path('logout/', logout_func, name='logout_func'),
    path('my-profile/', get_profile, name='my_profile')
    
]