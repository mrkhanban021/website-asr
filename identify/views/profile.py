from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth import get_user_model

User = get_user_model()

def get_profile(request):
    if request.method == 'POST':
        pass
    else:
        pass
    
    return render(request, 'identify/panel.html')