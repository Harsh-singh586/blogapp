# Generated by Django 3.1.1 on 2021-07-15 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20210515_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='page',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='page',
            name='likes',
        ),
        migrations.AddField(
            model_name='page',
            name='reactions',
            field=models.IntegerField(default=0),
        ),
    ]
