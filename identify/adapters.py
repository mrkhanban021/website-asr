# identify/adapters.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from identify.models import CustomUser

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        اینجا قبل از ساخت user:
        - اگر ایمیل از قبل موجود باشه
        - SocialAccount رو به کاربر موجود وصل می‌کنه
        - صفحه signup نمایش داده نمیشه
        """
        if sociallogin.is_existing:
            return

        email = sociallogin.account.extra_data.get('email')
        if email:
            try:
                user = CustomUser.objects.get(email=email)
                # وصل کردن SocialAccount به کاربر موجود
                sociallogin.connect(request, user)
            except CustomUser.DoesNotExist:
                pass  # کاربر جدید → خودش ساخته میشه
