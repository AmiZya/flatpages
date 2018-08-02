# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'flatpages_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=100, db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name=u'children', null=True,
                                                             to=orm['flatpages.Page'])),
            ('status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=70, blank=True)),
            ('registration_required', self.gf('django.db.models.fields.BooleanField')()),
            ('ordering', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            (
                'navigation_placement',
                self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'flatpages', ['Page'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'flatpages_page')


    models = {
        u'flatpages.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'navigation_placement': (
                'django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parent': ('mptt.fields.TreeForeignKey', [],
                       {'blank': 'True', 'related_name': "u'children'", 'null': 'True',
                        'to': u"orm['flatpages.Page']"}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['flatpages']