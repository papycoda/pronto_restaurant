# Generated by Django 5.0.3 on 2024-06-06 13:03

import imagekit.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0012_alter_category_default_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='Static/images/'),
        ),
    ]
