from django.core.management.base import BaseCommand
from website.models import SiteSetting


class Command(BaseCommand):
    help = "ایجاد تنظیمات سایت در صورت عدم وجود"

    def handle(self, *args, **options):
        if SiteSetting.objects.exists():
            self.stdout.write(self.style.WARNING(
                "تنظیمات سایت قبلاً ایجاد شده"))
            return

        SiteSetting.objects.create(
            site_name="نام پیش‌فرض سایت",
            copyright_text="© تمامی حقوق محفوظ است",
            main_color="#0d6efd",
            secondary_color="#6c757d",
        )
        
        self.stdout.write(self.style.SUCCESS("تنظیمات سایت با موفقیت ساخته شد"))