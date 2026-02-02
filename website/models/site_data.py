from django.db import models
from identify.models import BaseModel
from django.core.exceptions import ValidationError


class SiteSetting(BaseModel):
    site_name = models.CharField(max_length=100, help_text="نام سایت")
    logo = models.ImageField(upload_to="site/logo/", help_text="لوگوی سایت")
    favicon = models.ImageField(
        upload_to="site/favicon/", help_text="آیکون سایت")
    phone = models.CharField(max_length=20, help_text="شماره تماس")
    email = models.EmailField(help_text="ایمیل پشتیبانی")
    address = models.TextField(help_text="آدرس دفتر")
    instagram = models.URLField(
        blank=True, null=True, help_text="لینک اینستاگرام")
    telegram = models.URLField(blank=True, null=True, help_text="لینک تلگرام")
    linkedin = models.URLField(blank=True, null=True, help_text="لینک لینکدین")
    copyright_text = models.CharField(max_length=200, help_text="متن کپی‌رایت")
    about_short = models.TextField(
        blank=True, null=True, help_text="توضیح کوتاه درباره سایت")
    main_color = models.CharField(
        max_length=7, default="#007bff", help_text="رنگ اصلی سایت")
    secondary_color = models.CharField(
        max_length=7, default="#6c757d", help_text="رنگ ثانویه سایت")

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSetting.objects.exists():
            raise ValidationError("فقط یک ردیف تنظیمات مجاز است")
        
        if self.pk:
            try:
                old_file = SiteSetting.objects.get(pk=self.pk)
                if old_file.logo and old_file.logo != self.logo:
                    old_file.logo.delete(save=False)
                    
                if old_file.favicon and old_file.favicon != self.favicon:
                    old_file.favicon.delete(save=False)
            except SiteSetting.DoesNotExist:
                pass
            
            

        super().save(*args, **kwargs)
