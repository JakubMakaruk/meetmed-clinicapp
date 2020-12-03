# Generated by Django 3.1.2 on 2020-11-24 20:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import meetmedaccount.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default=meetmedaccount.models.defaultTitle, max_length=100)),
                ('description', models.CharField(blank=True, max_length=480, null=True)),
                ('start_date', models.DateTimeField(blank=True, default=datetime.date.today, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=datetime.date.today, null=True)),
                ('date_reserved', models.DateTimeField(blank=True, null=True)),
                ('done', models.CharField(default=meetmedaccount.models.defaultDoneClass, max_length=30)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
