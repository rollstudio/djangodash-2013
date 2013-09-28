# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CookieCutter.tags'
        db.alter_column(u'cookiecutters_cookiecutter', 'tags', self.gf('djorm_pgarray.fields.ArrayField')(dbtype='varchar(100)', null=True))

    def backwards(self, orm):

        # Changing field 'CookieCutter.tags'
        db.alter_column(u'cookiecutters_cookiecutter', 'tags', self.gf('djorm_pgarray.fields.ArrayField')(null=True))

    models = {
        u'cookiecutters.cookiecutter': {
            'Meta': {'object_name': 'CookieCutter'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tags': ('djorm_pgarray.fields.ArrayField', [], {'default': 'None', 'dbtype': "'varchar(100)'", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['cookiecutters']