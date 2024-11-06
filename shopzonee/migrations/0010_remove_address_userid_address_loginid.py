# Generated by Django 5.1.1 on 2024-11-06 09:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopzonee', '0009_alter_cart_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='userid',
        ),
        migrations.AddField(
            model_name='address',
            name='loginId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopzonee.login'),
        ),
    ]
