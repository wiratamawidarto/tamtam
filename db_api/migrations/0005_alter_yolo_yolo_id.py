# Generated by Django 3.2.6 on 2021-08-26 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db_api', '0004_auto_20210826_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yolo',
            name='yolo_id',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
