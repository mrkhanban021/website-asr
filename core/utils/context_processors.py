from django.conf import settings
from website.selectors import get_data_site_settings
from meta.views import Meta
from django.core.cache import cache

def default_meta(request):
    return {
        'meta': Meta(
            title=settings.META_DEFAULT_TITLE,
            description=settings.META_DEFAULT_DESCRIPTION,
            url=request.build_absolute_uri(),
            type=settings.META_SITE_TYPE,
            image=settings.META_DEFAULT_IMAGE,
            meta_site_protocol=settings.META_SITE_PROTOCOL,
            meta_site_domain=settings.META_SITE_DOMAIN,
            meta_site_name=settings.META_SITE_NAME,
            meta_default_keywords=settings.META_DEFAULT_KEYWORDS
            
        )
    }
    
def get_global_data(request):
    data = cache.get("global_site_data")
    
    if not data:
        data = {
            "site": get_data_site_settings(),
        }
        cache.set("global_site_data", data, 60 * 60)
    return data