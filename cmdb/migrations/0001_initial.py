# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-29 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.CharField(max_length=64, unique=True, verbose_name='主机名')),
                ('ip', models.GenericIPAddressField(verbose_name='Ip1')),
                ('cpu_mode', models.CharField(max_length=128, verbose_name='cpu')),
                ('platform', models.CharField(max_length=64, verbose_name='系统信息')),
                ('memory', models.CharField(max_length=32, verbose_name='内存信息')),
            ],
            options={
                'verbose_name_plural': '资产信息表',
            },
        ),
        migrations.CreateModel(
            name='AssetRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_number', models.IntegerField(default=1)),
                ('content', models.TextField(null=True)),
            ],
        ),
    ]
