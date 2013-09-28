from django.db import models
from django.utils.translation import ugettext_lazy as _

from djorm_pgarray.fields import ArrayField
from djorm_expressions.models import ExpressionManager
from djorm_expressions.base import SqlExpression

class ArrayExpression(object):
    def __init__(self, field):
        self.field = field

    def contains(self, value):
        return SqlExpression(self.field, "@>", value)

    def overlap(self, value):
        return SqlExpression(self.field, "&&", value)


class CookieCutter(models.Model):
    title = models.CharField(_('Title'), max_length=100)
    description = models.TextField(_('Description'))
    url = models.URLField(_('URL'))

    language = models.CharField(_('Language'), max_length=50)
    tags = ArrayField(_('Tags'), dbtype='text')

    objects = ExpressionManager()

    class Meta(object):
        verbose_name = _('Cookie Cutter')
        verbose_name_plural = _('Cookie Cutters')

    def __unicode__(self):
        return self.title
