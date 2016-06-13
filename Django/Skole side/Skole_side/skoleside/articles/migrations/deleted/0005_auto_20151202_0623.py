# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django_markdown.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20151125_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2015, 12, 2, 6, 23, 5, 386531, tzinfo=utc), unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='body',
            field=django_markdown.models.MarkdownField(),
        ),
    ]
