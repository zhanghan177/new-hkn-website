# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-05 04:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dbcafe', '0004_transaction'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drawer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=999)),
            ],
        ),
    ]
