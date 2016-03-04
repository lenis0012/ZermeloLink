# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('pub_date', models.DateTimeField(verbose_name=b'date added')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=64)),
                ('first_name', models.CharField(max_length=128)),
                ('middle_name', models.CharField(default=b'', max_length=128)),
                ('last_name', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=128)),
                ('subjects', models.ManyToManyField(to='moodle.Subject')),
            ],
        ),
        migrations.AddField(
            model_name='cohort',
            name='subject',
            field=models.ForeignKey(to='moodle.Subject'),
        ),
    ]
