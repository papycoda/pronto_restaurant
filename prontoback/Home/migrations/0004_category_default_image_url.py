# Generated by Django 5.0.3 on 2024-05-20 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0003_menuitem_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='default_image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]