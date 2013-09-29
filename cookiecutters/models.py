import os
import json

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from djorm_pgarray.fields import ArrayField
from djorm_expressions.models import ExpressionManager
from djorm_expressions.base import SqlExpression

from json_field import JSONField

from cookiecutters import tasks, forms


class Question(object):
    def __init__(self, name, default):
        self.name = name
        self.default = default

    def __unicode__(self):
        return self.name.replace('_', ' ').title()

    def __str__(self):
        return self.name.replace('_', ' ').title()


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
    #options = models.TextField(editable=False)
    options = JSONField(editable=False)

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

    def form(self, *args, **kwargs):
        return forms.CookieCutterForm(self, *args, **kwargs)

    @cached_property
    def questions(self):
        questions = []

        path = self.repo_path

        json_file = os.path.join(path, 'cookiecutter.json')

        with open(json_file) as f:
            j = json.load(f)

            for name, default in j.iteritems():
                q = Question(name, default)

                questions.append(q)

        return questions


    def __unicode__(self):
        return u"%s/%s" % (self.user.username, self.name)



def cookie_post_save(sender, instance, created, **kwargs):
    if created:
        tasks.update_repo.delay(instance)


post_save.connect(cookie_post_save, sender=CookieCutter)
