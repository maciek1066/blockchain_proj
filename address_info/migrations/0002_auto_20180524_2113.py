# Generated by Django 2.0.5 on 2018-05-24 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address_info', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='no_transaction',
            new_name='no_transactions',
        ),
    ]
