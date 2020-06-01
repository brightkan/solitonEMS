# Generated by Django 3.0 on 2020-06-01 13:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organisation_details', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holidays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_date', models.DateField()),
                ('holiday_name', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Leave_Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(max_length=45)),
                ('leave_days', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LeaveApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apply_date', models.DateField(default=django.utils.timezone.now)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('no_of_days', models.IntegerField(default=1)),
                ('supervisor_status', models.CharField(default='Pending', max_length=15)),
                ('hod_status', models.CharField(default='Pending', max_length=15)),
                ('hr_status', models.CharField(default='Pending', max_length=15)),
                ('overall_status', models.CharField(default='Pending', max_length=10)),
                ('remarks', models.TextField()),
                ('balance', models.IntegerField(default=0)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation_details.Department')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Employees', to='employees.Employee')),
                ('hod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hod', to='employees.Employee')),
                ('hr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hr', to='employees.Employee')),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.Leave_Types')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Supervisor', to='employees.Employee')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation_details.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Leave_Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_year', models.IntegerField()),
                ('entitlement', models.IntegerField(default=21)),
                ('residue', models.IntegerField(default=0)),
                ('leave_applied', models.IntegerField(default=0)),
                ('total_taken', models.IntegerField(default=0)),
                ('balance', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='annual_planner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_year', models.CharField(max_length=5)),
                ('leave_month', models.CharField(default='Jan', max_length=4)),
                ('date_from', models.DateField()),
                ('date_to', models.DateField()),
                ('no_of_days', models.IntegerField(default=0)),
                ('status', models.CharField(default='Pending', max_length=15)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
                ('leave', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='leave.Leave_Types')),
            ],
        ),
    ]
