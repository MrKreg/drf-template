from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from app.pkg.common.emails.styles import COMMON_CSS_STYLES


class MessageNotification(object):
    template_name = NotImplemented
    subject = NotImplemented

    css_styles = COMMON_CSS_STYLES

    def __init__(self, **context_data):
        self.context_data = context_data

    def _get_context(self):
        site = Site.objects.get_current()
        protocol = getattr(settings, 'SITE_PROTOCOL', 'http')
        return {
            'css': self.css_styles,
            'domain': site.domain,
            'site_name': site.name,
            'protocol': protocol,
            'site_url': '{0}://{1}'.format(protocol, site.domain)
        }

    def get_context_data(self):
        data = self._get_context()
        data.update(self.context_data)
        return data

    def get_content(self):
        return render_to_string(self.template_name, self.get_context_data())

    def get_subject(self):
        try:
            return self.subject % self.get_context_data()
        except (KeyError, IndexError):
            return self.subject
