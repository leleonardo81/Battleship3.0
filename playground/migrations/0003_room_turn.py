# Generated by Django 2.2 on 2019-04-07 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_auto_20190407_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='turn',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
