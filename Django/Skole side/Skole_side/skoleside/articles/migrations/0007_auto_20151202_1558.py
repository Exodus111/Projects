# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20151202_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(default=None, upload_to=b''),
        ),
        migrations.AddField(
            model_name='article',
            name='teaser',
            field=models.CharField(default=None, max_length=500),
        ),
    ]
