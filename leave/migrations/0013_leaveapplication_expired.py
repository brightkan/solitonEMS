# Generated by Django 3.1.5 on 2021-02-23 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0012_leaveapplication_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaveapplication',
            name='expired',
            field=models.BooleanField(default=False),
        ),
    ]
