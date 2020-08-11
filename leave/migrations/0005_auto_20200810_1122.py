# Generated by Django 3.0.7 on 2020-08-10 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_auto_20200810_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveplan',
            name='approval_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=8),
        ),
    ]
