# Generated by Django 5.1.1 on 2024-11-06 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopzonee', '0014_alter_address_loginid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='loginid',
        ),
    ]
