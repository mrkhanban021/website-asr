from django.shortcuts import (
    render,
    redirect
)

from identify.forms import (
    LoginOnSite
)
from django.contrib.auth import authenticate, login, logout


def login_form(request):
    if request.method == "POST":
        form = LoginOnSite(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, email=data.get('email'), password=data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('website:home:home_page')
    else:
        form = LoginOnSite()
        
    context = {
        'form': form # type: ignore
    }
        
    return render(request, 'identify/login.html', context)


def logout_func(request):
    logout(request)
    return redirect('website:home:home_page')