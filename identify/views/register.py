from django.shortcuts import (
    render,
    redirect
)
from  identify.forms import (
    RegisterOnSite
)


def register_form(request):
    if request.method == 'POST':
        pass
    else:
        form = RegisterOnSite()
        context = {
            'form': form
        }
    
    return render(request , 'identify/register.html')