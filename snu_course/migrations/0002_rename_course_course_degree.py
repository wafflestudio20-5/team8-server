# Generated by Django 4.1.4 on 2023-01-02 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snu_course', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='course',
            new_name='degree',
        ),
    ]