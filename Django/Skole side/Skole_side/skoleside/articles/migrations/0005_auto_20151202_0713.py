# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_markdown.models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20151125_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='body',
            field=django_markdown.models.MarkdownField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(default=b'slug', unique=True),
        ),
    ]
