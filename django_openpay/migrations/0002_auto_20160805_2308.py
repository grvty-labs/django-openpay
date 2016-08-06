# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 23:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_openpay', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='recovered',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='trial_days',
        ),
        migrations.AddField(
            model_name='charge',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Amount'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='charge',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='charge',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='charge',
            name='method',
            field=models.CharField(blank=True, max_length=30, verbose_name='Method'),
        ),
        migrations.AddField(
            model_name='customer',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Creation date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='trial_end_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Trial days'),
            preserve_default=False,
        ),
    ]