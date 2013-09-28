import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from djorm_pgarray.fields import ArrayField
from djorm_expressions.models import ExpressionManager
from djorm_expressions.base import SqlExpression

from cookiecutters import tasks


class ArrayExpression(object):
    def __init__(self, field):
        self.field = field

    def contains(self, value):
        return SqlExpression(self.field, "@>", value)

    def overlap(self, value):
        return SqlExpression(self.field, "&&", value)


class CookieCutter(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'))
    url = models.URLField(_('URL'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    options = models.TextField(editable=False)

    language = models.CharField(_('Language'), max_length=50)
    tags = ArrayField(_('Tags'), dbtype='text')

    objects = ExpressionManager()

    class Meta(object):
        verbose_name = _('Cookie Cutter')
        verbose_name_plural = _('Cookie Cutters')
        unique_together = (('name', 'user'),)

    @cached_property
    def repo_path(self):
        return os.path.join(settings.COOKIECUTTERS_DIR,
                self.user.username, self.name)


    def __unicode__(self):
        return u"%s/%s" % (self.user.username, self.name)



def cookie_post_save(sender, instance, created, **kwargs):
    if created:
        tasks.update_repo.delay(instance)
    

post_save.connect(cookie_post_save, sender=CookieCutter)
