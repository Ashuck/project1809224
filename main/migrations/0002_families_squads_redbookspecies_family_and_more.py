# Generated by Django 5.1.1 on 2024-09-18 12:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Families',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Семейство',
                'verbose_name_plural': 'Семейства',
            },
        ),
        migrations.CreateModel(
            name='Squads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Отряд/отдел/порядок',
                'verbose_name_plural': 'Отряд/отдел/порядок',
            },
        ),
        migrations.AddField(
            model_name='redbookspecies',
            name='family',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.families', verbose_name='Семейство'),
        ),
        migrations.AddField(
            model_name='redbookspecies',
            name='squad',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.squads', verbose_name='Отряд/отдел/порядок'),
        ),
    ]
