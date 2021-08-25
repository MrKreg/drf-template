from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedIndexModel(models.Model):
    created = models.DateTimeField(_('created'), editable=False, auto_now_add=True, db_index=True)
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        get_latest_by = 'created'
        ordering = ('-created', '-modified',)
        abstract = True
