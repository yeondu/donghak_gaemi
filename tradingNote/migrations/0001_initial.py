# Generated by Django 3.2.6 on 2021-08-08 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tradingNoteModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trading_note_id', models.IntegerField()),
                ('stock_id', models.IntegerField()),
                ('trading_category', models.CharField(max_length=20)),
                ('buying_date', models.DateField()),
                ('sell_date', models.DateField()),
                ('stop_loss', models.IntegerField()),
                ('holding_period', models.IntegerField()),
                ('profit', models.IntegerField()),
                ('contract_price', models.IntegerField()),
                ('contract_amount', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('trading_comment', models.CharField(max_length=2000)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.usermodel')),
            ],
            options={
                'db_table': 'tradingNote',
            },
        ),
    ]