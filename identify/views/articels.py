from django.shortcuts import (
    render,
    redirect
)
from django.contrib.auth.decorators import login_required

from django.contrib.auth import get_user_model

User = get_user_model()

def get_articels(request):
    if request.method == 'POST':
        pass
    else:
        pass
    
    return render(request, 'identify/articels.html')