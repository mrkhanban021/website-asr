from website.models import SiteSetting
import jdatetime

# دریافت اطلاعات اصلی سایت

def get_data_site_settings() -> object:
    data = {
        'data': SiteSetting.objects.first(),
        'date': jdatetime.datetime.now().year
    }
    if not data:
        pass
    return data

