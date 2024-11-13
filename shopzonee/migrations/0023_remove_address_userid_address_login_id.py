# Generated by Django 5.1.1 on 2024-11-06 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopzonee', '0022_alter_address_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='userid',
        ),
        migrations.AddField(
            model_name='address',
            name='login_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopzonee.registration'),
        ),
    ]