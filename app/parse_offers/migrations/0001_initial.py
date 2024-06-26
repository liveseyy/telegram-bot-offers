# Generated by Django 4.2.1 on 2023-05-28 17:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvitoCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('date_of_update', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', models.CharField(max_length=150, null=True, unique=True, verbose_name='Часть url категории')),
                ('filter_form', models.CharField(choices=[('Общая', 'Общая'), ('Транспорт', 'Транспорт')], default='Общая', verbose_name='Форма фильтров для парсинга')),
                ('parent_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='parse_offers.avitocategory', verbose_name='Родительская категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AvitoUserOfferWatcherFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('date_of_update', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('specific_filter', models.JSONField(help_text='Фильтры индивидуальные для какой-либо категории, например, пробег авто или кол-во комнат в квартире', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AvitoUserOfferWatcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_creation', models.DateTimeField(default=django.utils.timezone.localtime)),
                ('date_of_update', models.DateTimeField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('last_checked_offer_datetime', models.DateTimeField(default=django.utils.timezone.localtime, help_text='Пользователю отправляются объявления выложенные после этого времени')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parse_offers.avitocategory', verbose_name='Наблюдаемая категория')),
                ('filter', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='parse_offers.avitouserofferwatcherfilter')),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot.telegramuser', verbose_name='Владец вотчера')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
