# Generated by Django 3.1.7 on 2021-03-05 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='price',
            field=models.DecimalField(decimal_places=4, max_digits=20, null=True),
        ),
    ]