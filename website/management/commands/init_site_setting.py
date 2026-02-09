from django.core.management.base import BaseCommand
from website.models import SiteSetting


class Command(BaseCommand):
    help = "CREATED SITE SETTINGS"

    def handle(self, *args, **options):
        if SiteSetting.objects.exists():
            self.stdout.write(self.style.WARNING(
                "SITE SETTING ALLREADY EXISTS."))
            return

        SiteSetting.objects.create(
            site_name="نام پیش‌فرض سایت",
            phone_factory="02176218555",
            phone_sales="+989101017409",
            phone_support="+989101107033",
            email="roshd.agahi.danesh@gmail.com",
            address=(
                "تهران شهرستان پردیس شهرک صنعتی خرمدشت بلوار اصلی سوم شرقی پلاک 56",
            ),
            zip_code="1653372504",
            instagram="https://www.instagram.com/ariansystemro/",
            telegram="https://t.me/ariansystemro",
            linkedin="https://ir.linkedin.com/company/arian-system-ro-asr",
            about_short="آریان سیستم رو تولید کننده درب تمام اتو ماتیک آسانسور",
            economic_number="61189740279",
            standard_code="6628298905",
            copyright_text="© تمامی حقوق محفوظ است",
            main_color="#0d6efd",
            secondary_color="#6c757d",
        )

        self.stdout.write(self.style.SUCCESS(
            "SITE SETTING HAS BEN CREATED SUCSSESSFULY."))
