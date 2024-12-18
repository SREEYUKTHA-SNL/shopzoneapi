# Generated by Django 5.1.1 on 2024-11-06 10:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopzonee', '0015_remove_address_loginid'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='loginId',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to='shopzonee.login'),
        ),
    ]
