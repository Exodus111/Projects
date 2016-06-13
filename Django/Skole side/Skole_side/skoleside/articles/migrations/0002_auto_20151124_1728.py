# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='article',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 17, 28, 32, 578514, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 24, 17, 28, 54, 293570, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='publish',
            field=models.BooleanField(default=True),
        ),
    ]
