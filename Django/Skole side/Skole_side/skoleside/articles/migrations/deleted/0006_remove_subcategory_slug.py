# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20151202_0623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='slug',
        ),
    ]
