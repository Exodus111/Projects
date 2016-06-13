# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20151124_1728'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(max_length=200)),
                ('category', models.ForeignKey(to='articles.Category')),
            ],
            options={
                'verbose_name_plural': 'Sub-Categories',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(to='articles.SubCategory'),
        ),
    ]
