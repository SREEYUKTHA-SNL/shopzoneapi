# Generated by Django 5.1.1 on 2024-11-02 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopzonee', '0008_alter_wishlist_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='image',
            field=models.URLField(),
        ),
    ]