from django.conf import settings
from django.contrib.sites.models import Site


def get_site_url():
    site = Site.objects.get_current()
    protocol = getattr(settings, 'SITE_PROTOCOL', 'http')
    return '{0}://{1}'.format(protocol, site.domain)


def build_abs_url(url):
    site_url = get_site_url()
    return '{0}/{1}'.format(site_url, url[1:] if url.startswith('/') else url)