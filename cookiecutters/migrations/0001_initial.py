# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CookieCutter'
        db.create_table(u'cookiecutters_cookiecutter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tags', self.gf('djorm_pgarray.fields.ArrayField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'cookiecutters', ['CookieCutter'])


    def backwards(self, orm):
        # Deleting model 'CookieCutter'
        db.delete_table(u'cookiecutters_cookiecutter')


    models = {
        u'cookiecutters.cookiecutter': {
            'Meta': {'object_name': 'CookieCutter'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tags': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['cookiecutters']