# Generated by Django 3.2.9 on 2022-01-08 17:26

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_alter_comment_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 8, 17, 26, 1, 687154, tzinfo=utc)),
        ),
    ]