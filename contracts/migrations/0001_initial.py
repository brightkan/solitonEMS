# Generated by Django 2.2.1 on 2020-03-20 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0002_delete_department'),
        ('organisation_details', '0002_auto_20200320_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.IntegerField(unique=True)),
                ('effective_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('status', models.CharField(default='Active', max_length=10)),
                ('risk', models.CharField(max_length=10)),
                ('document', models.FileField(upload_to='contracts')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employees.Employee')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organisation_details.Position')),
            ],
        ),
    ]
