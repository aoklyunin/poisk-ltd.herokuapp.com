# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-24 12:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workReport', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workreport',
            name='flgCalculateEquipment',
        ),
        migrations.AlterField(
            model_name='equipment',
            name='code',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='material',
            name='code',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='workpart',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='VIKer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='VIKER_name', to='workReport.Worker', verbose_name='ВИК'),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='noPlanHardware',
            field=models.ManyToManyField(blank=True, null=True, related_name='no_PlanHardware_name', to='workReport.HardwareEquipment', verbose_name='Внеплановая'),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='note',
            field=models.CharField(blank=True, default='', max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='planHardware',
            field=models.ManyToManyField(blank=True, null=True, related_name='planHardware_name', to='workReport.HardwareEquipment', verbose_name='Плановая'),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='reportChecker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportChecker_name', to='workReport.Worker', verbose_name='Проверяющий отчёт'),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='reportMaker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reportMaker_name', to='workReport.Worker', verbose_name='Cоставитель отчёта'),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='stockMan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stockMan_name', to='workReport.Worker', verbose_name='Кладовщик'),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='supervisor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_name', to='workReport.Worker', verbose_name='Руководитель'),
        ),
        migrations.AlterField(
            model_name='workreport',
            name='worker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_name', to='workReport.Worker', verbose_name='Иcполнитель'),
        ),
    ]