# Generated by Django 3.2 on 2022-10-22 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_alter_messages_post_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='post_id',
            field=models.IntegerField(default=1, max_length=200),
        ),
        migrations.AddField(
            model_name='messages',
            name='post_url',
            field=models.TextField(default=''),
        ),
    ]
