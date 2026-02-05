from django.shortcuts import (
    render,
    redirect
)
from django.contrib import messages
from identify.forms import (
    RegisterOnSite
)
from django.contrib.auth import get_user_model

User = get_user_model()


def register_form(request):
    if request.method == 'POST':
        form = RegisterOnSite(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                email=data.get('email'),
                password=data.get('password_2')
            ) # type: ignore
            if user:
                messages.success(request, 'ثبت نام شما با موفقیت انجام شد.')
            return redirect('identify:endpoint:login_form')
    else:
        form = RegisterOnSite()
    context = {
        'form': form  # type: ignore
    }

    return render(request, 'identify/register.html', context)
