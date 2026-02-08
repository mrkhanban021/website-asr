from django import forms
from identify.models.user_manager import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'display_name', 'profile_images']
