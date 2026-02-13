from identify.manager import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
import jdatetime
from django.utils import timezone


def save_document(instanse, filename):
    today = jdatetime.datetime.now().strftime("%Y-%m-%d")
    code = uuid.uuid4().hex[:8].upper()

    return f"document/{today}_{code}/{filename}"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='ایدی کاربر', editable=False)
    email = models.EmailField(unique=True, help_text='ایمیل کاربر')
    is_active = models.BooleanField(default=True, help_text='فعال بودن اکامت')
    is_staff = models.BooleanField(
        default=False, help_text='دسترسی به پنل ادمین')
    is_superuser = models.BooleanField(
        default=False, help_text='دسترسی به همه سوپر ادمین')

    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('-is_superuser', '-is_active', '-created_time')
        indexes = [
            models.Index(fields=['is_active', 'email'],
                         name='user_active_role_idx'),
        ]


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, help_text='ایدی')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created_time']),
            models.Index(fields=['updated_time']),
        ]
    @property
    def created_time_jalali(self):
        if not self.created_time:
            return ""
        
        local_dt = timezone.localtime(self.created_time)
        return jdatetime.datetime.fromgregorian(datetime=local_dt).strftime("%Y-%m-%d %H:%M")
    @property
    def updated_time_jalali(self):
        if not self.created_time:
            return ""
        
        local_dt = timezone.localtime(self.updated_time)
        return jdatetime.datetime.fromgregorian(datetime=local_dt).strftime("%Y-%m-%d %H:%M")


class Profile(BaseModel):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(
        max_length=15, null=True, blank=True, help_text='موبایل کاربر')
    first_name = models.CharField(
        max_length=50, null=True, blank=True, help_text='نام کاربر')
    last_name = models.CharField(
        max_length=50, null=True, blank=True, help_text='نام خانوادگی')
    display_name = models.CharField(
        max_length=10, null=True, blank=True, help_text='نام نمایشی')
    profile_images = models.ImageField(
        upload_to=save_document, null=True, blank=True)
        
    class Meta:
        ordering = ('user__is_active', '-created_time')

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_file = Profile.objects.get(pk=self.pk)
                if old_file.profile_images and old_file.profile_images != self.profile_images:
                    old_file.profile_images.delete(save=False)
            except Profile.DoesNotExist:
                pass
        super().save(*args, **kwargs)
