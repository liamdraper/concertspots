# Generated by Django 4.1.7 on 2023-03-06 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_remove_ticket_concert'),
    ]

    operations = [
        migrations.AddField(
            model_name='concert',
            name='api_id',
            field=models.IntegerField(default=5783573),
            preserve_default=False,
        ),
    ]