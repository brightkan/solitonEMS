# Generated by Django 2.2.2 on 2019-09-29 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('overtime', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='overtimeapplication',
            old_name='supervisee',
            new_name='applicant',
        ),
    ]