# Generated by Django 5.0.3 on 2024-06-05 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0010_alter_menuitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='default_image',
            field=models.ImageField(blank=True, null=True, upload_to='Static/images/'),
        ),
    ]
