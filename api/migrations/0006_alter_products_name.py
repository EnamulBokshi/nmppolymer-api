# Generated by Django 5.1.5 on 2025-02-14 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_slider_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.TextField(),
        ),
    ]
