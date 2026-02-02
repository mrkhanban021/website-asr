from website.models import SiteSetting

# دریافت اطلاعات اصلی سایت

def get_data_site_settings() -> object:
    data = SiteSetting.objects.first()
    if not data:
        pass
    return data

