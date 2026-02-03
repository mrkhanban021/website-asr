from django.urls import include, path

app_name = 'identify'

urlpatterns = [
    path('', include('identify.api.endpoint', namespace='endpoint')),
]