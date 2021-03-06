# Generated by Django 4.0.2 on 2022-03-04 13:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_Name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='NameHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Information',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=0)),
                ('dept', models.FloatField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('interest', models.FloatField(default=0)),
                ('bool', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.date(2022, 3, 4))),
                ('birthday', models.DateTimeField(default=datetime.date(2004, 5, 11))),
                ('interest_bool', models.BooleanField(default=True)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.name')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=0)),
                ('dept', models.FloatField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('interest', models.FloatField(default=0)),
                ('bool', models.BooleanField(default=False)),
                ('current_balance', models.FloatField(default=0)),
                ('payment', models.FloatField(default=0)),
                ('date', models.DateTimeField()),
                ('birthday', models.DateTimeField(default=datetime.date(2004, 5, 11))),
                ('total', models.FloatField(default=0)),
                ('paid_count', models.IntegerField(default=0)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.namehistory')),
            ],
        ),
    ]
