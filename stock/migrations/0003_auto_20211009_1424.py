# Generated by Django 3.2 on 2021-10-09 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_remove_pricemodel_adj_close'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricemodel',
            name='close',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pricemodel',
            name='high',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pricemodel',
            name='low',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='pricemodel',
            name='open',
            field=models.IntegerField(),
        ),
    ]