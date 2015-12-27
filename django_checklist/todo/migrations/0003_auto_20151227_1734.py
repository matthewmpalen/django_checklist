# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_checklist_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='checklist', to='common.Tag'),
        ),
    ]
