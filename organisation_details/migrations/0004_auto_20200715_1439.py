# Generated by Django 3.0.6 on 2020-07-15 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation_details', '0003_auto_20200715_1232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='position',
            old_name='salary',
            new_name='salary_scale',
        ),
    ]