# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebhookLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('url', models.URLField(verbose_name='URL')),
                ('status', models.IntegerField(verbose_name='Status code')),
                ('data', models.TextField(verbose_name='Response data')),
                ('webhook', models.ForeignKey(related_name='logs', to='webhooks.Webhook')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
