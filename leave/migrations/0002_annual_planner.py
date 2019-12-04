# Generated by Django 2.2.1 on 2019-08-19 09:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0003_remove_employee_team'),
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='annual_planner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_year', models.CharField(max_length=5)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('status', models.CharField(default='Pending', max_length=15)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
            ],
        ),
    ]
