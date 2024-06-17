# Generated by Django 5.0.3 on 2024-06-16 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0014_alter_event_options_remove_event_date_event_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='email',
            field=models.CharField(default='placeholder@example.com', max_length=100),
        ),
        migrations.AddField(
            model_name='table',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='table',
            name='reserved_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='table',
            name='table_group',
            field=models.CharField(choices=[('bar', 'Bar'), ('lounge', 'Lounge'), ('outdoor', 'Outdoor')], default='bar', max_length=20),
        ),
    ]