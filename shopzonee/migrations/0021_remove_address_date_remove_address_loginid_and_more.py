# Generated by Django 5.1.1 on 2024-11-06 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopzonee', '0020_alter_address_loginid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='date',
        ),
        migrations.RemoveField(
            model_name='address',
            name='loginId',
        ),
        migrations.AddField(
            model_name='address',
            name='userid',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='shopzonee.login'),
            preserve_default=False,
        ),
    ]
