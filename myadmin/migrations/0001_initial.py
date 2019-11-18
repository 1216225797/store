# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('add_date', models.DateField(auto_created=True, auto_now_add=True)),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('describe', models.TextField(blank=True, null=True)),
                ('state', models.IntegerField(default=0)),
                ('stock', models.IntegerField(default=0)),
                ('picture', models.CharField(max_length=255, blank=True, null=True)),
                ('company', models.CharField(max_length=255, blank=True, null=True)),
            ],
            options={
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='Order_detail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('order_id', models.IntegerField()),
                ('goods_id', models.IntegerField()),
                ('goods_num', models.IntegerField()),
            ],
            options={
                'db_table': 'order_detail',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('linkman', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=6, blank=True, null=True)),
                ('phone', models.CharField(max_length=11)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('price', models.FloatField()),
                ('status', models.CharField(max_length=1, default=0)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('pid', models.IntegerField(default=0)),
                ('path', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'type',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=16, unique=True)),
                ('name', models.CharField(max_length=8)),
                ('password', models.CharField(max_length=32)),
                ('gender', models.IntegerField(default=0)),
                ('mobile', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=255)),
                ('state', models.IntegerField(default=0)),
                ('status', models.IntegerField(default=0)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'user_info',
                'ordering': ['-create_date'],
            },
        ),
        migrations.AddField(
            model_name='orders',
            name='uid',
            field=models.ForeignKey(to='myadmin.Users'),
        ),
        migrations.AddField(
            model_name='goods',
            name='type_id',
            field=models.ForeignKey(to='myadmin.Types'),
        ),
    ]
