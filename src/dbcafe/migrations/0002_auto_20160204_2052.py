# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-04 20:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dbcafe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='uniqname',
            new_name='name',
        ),
    ]
