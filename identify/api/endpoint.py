from django.urls import path
from identify.views import (
    register_form,
    login_form,
    logout_func,
    get_profile,
    get_articels,
    update_profile
)

app_name = 'endpoint'

urlpatterns = [
    path('register/', register_form, name='register_form'),
    path('login/', login_form, name='login_form'),
    path('logout/', logout_func, name='logout_func'),
    path('profile-user/', get_profile, name='profile'),
    path('articels/', get_articels, name='articels'),
    path('update-profile/', update_profile, name='update_profile')
    
]