# Generated by Django 4.2.1 on 2023-08-16 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_rename_cart_cartitem_crt_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='prdt',
            new_name='product',
        ),
    ]
