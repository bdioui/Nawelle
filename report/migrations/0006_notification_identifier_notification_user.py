# Generated by Django 4.1.3 on 2023-01-07 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_notification_todo_identifier'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='identifier',
            field=models.TextField(default='_', max_length=1500),
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.TextField(default='_', max_length=1500),
        ),
    ]
