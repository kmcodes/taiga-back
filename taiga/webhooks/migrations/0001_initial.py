# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_auto_20141230_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('key', models.TextField(verbose_name='secret key')),
                ('project', models.ForeignKey(related_name='webhooks', to='projects.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
