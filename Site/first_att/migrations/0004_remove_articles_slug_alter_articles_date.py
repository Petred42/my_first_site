# Generated by Django 4.0.5 on 2022-12-14 17:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('first_att', '0003_alter_articles_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articles',
            name='slug',
        ),
        migrations.AlterField(
            model_name='articles',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 12, 14, 17, 47, 2, 513749, tzinfo=utc)),
        ),
    ]
