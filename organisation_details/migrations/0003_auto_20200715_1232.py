# Generated by Django 3.0.6 on 2020-07-15 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation_details', '0002_salaryscale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='salary',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='organisation_details.SalaryScale'),
        ),
    ]