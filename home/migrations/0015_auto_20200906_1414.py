# Generated by Django 3.1 on 2020-09-06 14:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20200906_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluating',
            name='dislike',
        ),
        migrations.RemoveField(
            model_name='evaluating',
            name='like',
        ),
        migrations.AddField(
            model_name='evaluating',
            name='state',
            field=models.IntegerField(default=0, max_length=1),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 6, 14, 14, 31, 791772), editable=False),
        ),
    ]
