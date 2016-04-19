# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='todo',
        ),
        migrations.AddField(
            model_name='todo',
            name='tags',
            field=models.ManyToManyField(to='todoapp.Tag'),
        ),
    ]
