# Generated by Django 2.2.1 on 2019-07-31 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='department',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='position',
        ),
        migrations.AddField(
            model_name='employee',
            name='leave_balance',
            field=models.IntegerField(default=21),
        ),
        migrations.AddField(
            model_name='employee',
            name='leave_status',
            field=models.CharField(default='At Work', max_length=45),
        ),
        migrations.AlterField(
            model_name='employee',
            name='team',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='employees.Teams'),
        ),
        migrations.CreateModel(
            name='OrganisationDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Departments')),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
                ('position', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='employees.Job_Titles')),
                ('team', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='employees.Teams')),
            ],
        ),
        migrations.CreateModel(
            name='BankDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_bank', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=20)),
                ('bank_account', models.CharField(max_length=20)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
            ],
        ),
    ]
