from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from identify.forms import (
    ProfileForm
)
from identify.models import Profile
from django.contrib import messages

User = get_user_model()




@login_required
def get_profile(request):
    profile = Profile.objects.get(user=request.user)
    context = {
        'profile': profile
    }
    return render(request, 'identify/profile.html', context)


@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما بروزرسانی شد')
            return redirect('identify:endpoint:profile')
            
    else:
        form = ProfileForm(instance=profile)
    context = {
        'form': form
    }

    return render(request, 'identify/profile_update.html', context)
